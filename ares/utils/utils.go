package utils

import (
	"fmt"
	"os"

	"github.com/charmbracelet/log"
)

type Data struct {
	Data             []byte
	CompressedData   []byte
	FileName         string
	InitialSize      string
	CompressedSize   string
	CompressionRatio int
}

func getBeeMovieScript() []byte {
	dat, err := os.ReadFile("tests/bee-movie-script.txt")
	if err != nil {
		log.Error(err)
	}
	log.Debug("Getting the bee movie script")
	return dat
}

func GetData() Data {
	d := Data{}
	d.Data = getBeeMovieScript()        // TODO : change this to actual data source later
	d.FileName = "bee-movie-script.txt" // TODO : Change this later to not hardcode filename
	log.Debug("File size using length of byte array", "size", len(d.Data))
	if log.GetLevel() == log.DebugLevel {
		fileInfo, err := os.Stat(fmt.Sprintf("tests/%s", d.FileName))
		if err != nil {
			log.Error(err)
		}
		log.Debug("Filesize using os.Stat method", "size", fileInfo.Size())
	}
	return d
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
