package main

import (
	"github.com/charmbracelet/log"
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

func main() {
	const CHUNK_SIZE = 3000
	log.Info(utils.GetLogo())
	log.Info("Starting Ares . . . ")
	log.Info("Ares is running in ", "mode", log.GetLevel())
	log.Info("Setting chunk size", "chunkSize", CHUNK_SIZE)
	data, err := utils.GetData()
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

	log.Info("Chunking the data into chunks of", "size", CHUNK_SIZE)
	chunks := shredder.Shred(CHUNK_SIZE, data.CompressedData)
	log.Info("Data split up into chunks", "numberOfChunks", len(chunks))

	if log.GetLevel() == log.DebugLevel {
		log.Debug("verifying chunking . . .")
		log.Debug("Size of last chunk", "lastChunkSize", len(chunks[len(chunks)-1]))
		formulaCalculation := CHUNK_SIZE*(len(chunks)-1) + len(chunks[len(chunks)-1])
		log.Debug("verifying ", "formula", "chunkSize * (numberOfChunks -1) + lastChunkSize == compressedDataSize")
		log.Debug("verifying", "formulaCalculation", formulaCalculation, "compressedDataSize", len(data.CompressedData))
		log.Debug("verifying", "verificationSuccessful", formulaCalculation == len(data.CompressedData))
	}

}
