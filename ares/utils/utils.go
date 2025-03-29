package utils

import (
	"context"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"math"
	"os"

	"github.com/charmbracelet/log"
	"github.com/redis/go-redis/v9"
)

type Data struct {
	Data                 []byte
	CompressedData       []byte
	FileName             string
	InitialSize          string
	CompressedSize       string
	CompressionRatio     float64
	OrignalDataSHA256    string
	CompressedDataSHA256 string
	ChunkSize            int
	DataChunks           [][]byte // this should be written to pubsub/list/queue/stream
	ChunkHashes          map[string]string
	TotalChunks          int
}

func (d *Data) WriteToRedis(rdb *redis.Client) {
	log.Info("Writing to redis")
	ctx := context.Background()
	id := d.FileName

	set := func(key string, val any) {
		log.Debug("redis-set", "key", key, "value", val)
		res, err := rdb.Set(ctx, key, val, 0).Result()
		if err != nil {
			log.Error("redis-set", "err", err, "result", res)
		} else {
			log.Debug("redis-set", "result", res)
		}
	}

	key := func(k string) string { return fmt.Sprintf("%s-%s", id, k) }

	set("FileName", d.FileName)
	set(key("InitialSize"), d.InitialSize)
	set(key("CompressedSize"), d.CompressedSize)
	set(key("CompressionRatio"), d.CompressionRatio)
	set(key("PreCompressionSHA"), d.OrignalDataSHA256)
	set(key("PostCompressionSHA"), d.CompressedDataSHA256)
	set(key("ChunkSize"), d.ChunkSize)
	set(key("TotalChunks"), d.TotalChunks)

	for k, v := range d.ChunkHashes {
		set(k, v)
		err := rdb.RPush(ctx, "chunkHashes", v).Err()
		if err != nil {
			log.Fatal("could not write chunk hashes to redis", err)
		}

	}

	for _, data := range d.DataChunks {
		b64Data := base64.StdEncoding.EncodeToString(data)
		err := rdb.RPush(ctx, "chunkdata", b64Data).Err()
		if err != nil {
			log.Fatal("Could not write data to redis", err)
		}
	}
	log.Infof("Written %d chunks to redis", len(d.ChunkHashes))
}

func getPayload() ([]byte, error) {
	cwd, err := os.Getwd()
	if err != nil {
		return nil, err
	}
	log.Debug("Current working directory", "cwd", cwd)
	dat, err := os.ReadFile("tests/payload.txt")
	// dat, err := os.ReadFile("tests/bee-movie-script.txt")
	if err != nil {
		return nil, err
	}
	log.Debug("Getting the bee movie script")
	return dat, nil
}

func GetData() (Data, error) {
	d := Data{}
	var err error
	d.Data, err = getPayload() // TODO : change this to actual data source later
	if err != nil {
		return d, err
	}
	d.FileName = "payload.txt" // TODO : Change this later to not hardcode filename
	log.Debug("File size using length of byte array", "size", len(d.Data))
	if log.GetLevel() == log.DebugLevel {
		fileInfo, err := os.Stat(fmt.Sprintf("tests/%s", d.FileName))
		if err != nil {
			return d, err
		}
		log.Debug("Filesize using os.Stat method", "size", fileInfo.Size())
	}
	log.Debug("Human readable filesize", "size", HumanFilesize(len(d.Data)))
	d.InitialSize = HumanFilesize(len(d.Data))
	return d, nil
}

func GetLogo() string {
	logo := `
                               ___
                              /   |  ________  _____
                             / /| | / ___/ _ \/ ___/
                            / ___ |/ /  /  __(__  )
                           /_/  |_/_/   \___/____/

    `
	return logo
}

func HumanFilesize(size int) string {
	if size < 1000 {
		return fmt.Sprintf("%d B", size)
	}
	suffixes := []string{"B", "KB", "MB", "GB", "TB"}
	base := math.Floor(math.Log(float64(size)) / math.Log(1000))
	newSize := float64(size) / math.Pow(1000, base)
	return fmt.Sprintf("%.1f %s", newSize, suffixes[int(base)])
}

func GetSHA256(data []byte) string {
	h := sha256.New()
	h.Write(data)
	return fmt.Sprintf("%x", h.Sum(nil))
}

func ConnectToRedis(done chan bool, rdbChan chan *redis.Client) {
	log.Info("Connecting to redis")
	var ctx = context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})
	pong, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.Warn("error connecting to redis instance", "err", err)
		done <- false
	} else {
		log.Info("Successfully connected to redis", "PING", pong)
		done <- true
		rdbChan <- rdb
	}
}
