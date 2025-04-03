package shredder

import (
	"context"
	"time"

	"github.com/briandowns/spinner"
	"github.com/redis/go-redis/v9"
)

func Unshred(rdb *redis.Client, s *spinner.Spinner) ([]rune, error, *redis.StringCmd, *spinner.Spinner) {
	s.Start()
	ctx := context.Background()
	chunks := rdb.Get(ctx, "decodedChunks")
	decodedRedis := rdb.Get(ctx, "secretData")
	unshreaded := []rune{}
	strChunks := chunks.String()
	for _, chunk := range strChunks {
		unshreaded = append(unshreaded, chunk)
	}
	time.Sleep(time.Second * 5)
	return unshreaded, nil, decodedRedis, s
}
