package main

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/briandowns/spinner"
	"github.com/redis/go-redis/v9"
)

func main() {
	var ctx = context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})
	decodedRedis := rdb.Get(ctx, "secretData")
	outFileName := fmt.Sprintf("decoded")
	file, err := os.Create(outFileName)

	s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
	s.Prefix = "Constructing original file . . . . "
	s.Start()
	time.Sleep(time.Second * 5)
	s.Stop()

	if err != nil {
		fmt.Printf("Error creating decoded file %s", err)
		os.Exit(1)
	}
	defer file.Close()
	n, err := file.Write([]byte(decodedRedis.String()))
	if err != nil {
		fmt.Printf("Error writing to decoded file : %s", err)
		os.Exit(1)
	}
	fmt.Printf("Written %d bytes to %s file successfully", n, outFileName)
	fmt.Println("created decoded file successfully")

}
