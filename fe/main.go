package main

import (
	"os"

	"github.com/charmbracelet/log"
	"github.com/theredditbandit/stitch/fe/form"
	"github.com/theredditbandit/stitch/fe/utils"
)

func init() {
	log.SetReportCaller(true)
	log.SetReportTimestamp(true)
	log.SetTimeFormat("2006-01-02 15:04:02")
	log.SetPrefix("Ares")
	log.SetLevel(log.DebugLevel)
	log.SetFormatter(log.TextFormatter)
}
func main() {
	if len(os.Args) != 2 {
		log.Errorf("Got %d arguments", len(os.Args)-1)
		log.Fatal("Need exactly 1 file name as an argument")
	}
	fileExists, err := utils.IsFileExists(os.Args[1])
	if !fileExists && err == nil {
		log.Fatalf("File at %s does not exist", os.Args[1])
	} else if fileExists && err != nil {
		log.Error("Something went wrong", err)
	}
	_, err = utils.IsFileSupported(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}

	err = form.RunForm()
	if err != nil {
		log.Fatal(err)
	}
}
