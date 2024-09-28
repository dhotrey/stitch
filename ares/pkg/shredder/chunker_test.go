package shredder

import (
	"fmt"
	"os"
	"testing"

	"github.com/charmbracelet/log"
	"github.com/theredditbandit/stitch/ares/pkg/squish"
	"github.com/theredditbandit/stitch/ares/utils"
)

func TestUnshred(t *testing.T) {
	data, err := getData()
	if err != nil {
		t.Error("something went wrong while getting data")
	}
	data.CompressedData = squish.Squash(data.Data)
	data.ChunkSize = 3000
	data.CompressedDataSHA256 = utils.GetSHA256(data.CompressedData)
	data.DataChunks = Shred(data)
	unshreaded := Unshred(data)
	unshreadedSHA256 := utils.GetSHA256(unshreaded)

	t.Run("Test unshread integrity", func(t *testing.T) {
		if data.CompressedDataSHA256 != unshreadedSHA256 {
			t.Errorf("Data is inconsistent. Preshread sha %s, postshread sha %s", data.CompressedDataSHA256, unshreadedSHA256)
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
