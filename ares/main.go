package main

import (
	"context"
	"fmt"
	"strconv"

	"github.com/charmbracelet/log"
	"github.com/redis/go-redis/v9"
	"github.com/theredditbandit/stitch/ares/pkg/shredder"
	"github.com/theredditbandit/stitch/ares/pkg/squish"
	"github.com/theredditbandit/stitch/ares/utils"
)

func init() {
	log.SetReportCaller(true)
	log.SetReportTimestamp(true)
	log.SetTimeFormat("2006-01-02 15:04:02")
	log.SetPrefix("Ares")
	log.SetLevel(log.DebugLevel)        // TODO : make configurable
	log.SetFormatter(log.TextFormatter) // TODO : make configurable

}

// TODO : refactor util functions to take in a pointer to the data struct and pass that around
func main() {
	done := make(chan bool)
	rdbChan := make(chan *redis.Client)
	go utils.ConnectToRedis(done, rdbChan)
	var ctx = context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})
	// const CHUNK_SIZE = 3000 // TODO : make this configurable
	csize := rdb.Get(ctx, "ChunkingSize")
	CHUNK_SIZE := csize.Val()
	log.Info(utils.GetLogo())
	log.Info("Starting Ares . . . ")
	log.Info("Ares is running in ", "mode", log.GetLevel())
	log.Info("Setting chunk size", "chunkSize", CHUNK_SIZE)
	data, err := utils.GetData()
	CHUNK_SIZE_INT, err := strconv.Atoi(CHUNK_SIZE)
	if err != nil {
		log.Fatal("Failed to fetch chunk size from redis")
	}
	data.ChunkSize = CHUNK_SIZE_INT
	if err != nil {
		log.Error("Something went wrong fetching the data", "Error", err)
	}
	log.Info("Got file successfully", "filename", data.FileName)
	log.Info("initial file size", "initialFilesize", data.InitialSize)
	data.OrignalDataSHA256 = utils.GetSHA256(data.Data)
	log.Info("Calculating SHA256 of uncompressed data", "hash", data.OrignalDataSHA256)
	log.Info("Compressing data . . ")
	data.CompressedData = squish.Squash(data.Data)
	data.CompressedDataSHA256 = utils.GetSHA256(data.CompressedData)
	log.Debug("raw size of compressed data", "size", len(data.CompressedData))
	log.Info("Size of compressed data", "size", utils.HumanFilesize(len(data.CompressedData)))
	log.Info("SHA256 of compressed data", "compressedDataHash", data.CompressedDataSHA256)
	data.CompressionRatio = (float64(len(data.CompressedData)) / float64(len(data.Data))) * 100
	log.Info("Data size decreased by", "compressionRatio", data.CompressionRatio)
	log.Info("Chunking the data into chunks of", "size", CHUNK_SIZE_INT)
	data.DataChunks = shredder.Shred(data)
	chunks := data.DataChunks
	data.TotalChunks = len(chunks)
	log.Info("Data split up into chunks", "numberOfChunks", data.TotalChunks)

	if log.GetLevel() == log.DebugLevel {
		log.Debug("verifying chunking . . .")
		log.Debug("Size of last chunk", "lastChunkSize", len(chunks[len(chunks)-1]))
		formulaCalculation := CHUNK_SIZE_INT*(len(chunks)-1) + len(chunks[len(chunks)-1])
		log.Debug("verifying ", "formula", "chunkSize * (numberOfChunks -1) + lastChunkSize == compressedDataSize")
		log.Debug("verifying", "formulaCalculation", formulaCalculation, "compressedDataSize", len(data.CompressedData))
		log.Debug("verifying", "verificationSuccessful", formulaCalculation == len(data.CompressedData))
	}

	log.Info("Hashing individual chunks")
	data.ChunkHashes = make(map[string]string)
	for idx, chunk := range data.DataChunks {
		chunkHash := utils.GetSHA256(chunk)
		chunkName := fmt.Sprintf("%s-%d", data.FileName, idx)
		log.Debug("", "chunk", chunkName, "chunkHash", chunkHash)
		data.ChunkHashes[chunkName] = chunkHash
	}
	connected := <-done
	log.Debug("connection status", "connected", connected)
	if connected {
		log.Info("Connected to redis successfully")
		client := <-rdbChan
		data.WriteToRedis(client)
		log.Info("Successfully written data to redis")
	} else {
		log.Warn("could not connect to redis")
		log.Error("Cannot write data to redis instance")
	}
}
