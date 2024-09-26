package squish

import (
	"fmt"
	"github.com/charmbracelet/log"
	"os"
	"testing"

	"github.com/theredditbandit/stitch/ares/utils"
)

func TestDecompress(t *testing.T) {
	cwd, err := os.Getwd()
	if err != nil {
		t.Error("Error getting cwd", err)
	}
	t.Log("current working directory is ", cwd)

	t.Run("Test decompression", func(t *testing.T) {
		data, err := getData()
		if err != nil {
			t.Error("Error getting the data", err)
		}
		orignalHash := utils.GetSHA256(data.Data)
		t.Log("orignalHash", orignalHash)
		compressedData := Squash(data.Data)
		decomp := UnSquish(compressedData)
		decompHash := utils.GetSHA256(decomp)
		t.Log("Hash after decompressing", decompHash)
		if decompHash != orignalHash {
			t.Errorf("Decompress() = %v, want %v", decompHash, orignalHash)
		}
	})
}

func getBeeMovieScript() ([]byte, error) {
	cwd, err := os.Getwd()
	if err != nil {
		return nil, err
	}
	log.Debug("Current working directory", "cwd", cwd)
	dat, err := os.ReadFile("../../tests/bee-movie-script.txt")
	if err != nil {
		return nil, err
	}
	log.Debug("Getting the bee movie script")
	return dat, nil
}

func getData() (utils.Data, error) {
	d := utils.Data{}
	var err error
	d.Data, err = getBeeMovieScript()
	if err != nil {
		return d, err
	}
	d.FileName = "bee-movie-script.txt"
	log.Debug("File size using length of byte array", "size", len(d.Data))
	if log.GetLevel() == log.DebugLevel {
		fileInfo, err := os.Stat(fmt.Sprintf("tests/%s", d.FileName))
		if err != nil {
			return d, err
		}
		log.Debug("Filesize using os.Stat method", "size", fileInfo.Size())
	}
	log.Debug("Human readable filesize", "size", utils.HumanFilesize(len(d.Data)))
	d.InitialSize = utils.HumanFilesize(len(d.Data))
	return d, nil
}
