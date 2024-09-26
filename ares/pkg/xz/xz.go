package xz

import (
	"bytes"
	"io"

	"github.com/charmbracelet/log"
	"github.com/ulikunitz/xz"
)

func Compress(data []byte) []byte {
	var buf bytes.Buffer

	w, err := xz.NewWriter(&buf)
	if err != nil {
		log.Fatalf("xz.NewWriter error is %s", err)
	}
	if _, err := io.WriteString(w, string(data)); err != nil {
		log.Fatalf("WriteString error %s", err)
	}
	if err := w.Close(); err != nil {
		log.Fatalf("w.Close error %s", err)
	}
	return buf.Bytes()
}

func Decompress() {

}
