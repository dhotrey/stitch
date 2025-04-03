package pkg

import (
	"constructor/pkg/shredder"
	"time"

	"github.com/briandowns/spinner"
	"github.com/redis/go-redis/v9"
)

// ConstructData : fetches data from redis and joins all chunks to form the original file
func ConstructData() *redis.StringCmd {
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})

	s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
	s.Prefix = "Constructing original file . . . . "
	_, _, decodedRedis, s := shredder.Unshred(rdb, s)
	s.Stop()
	return decodedRedis
}
