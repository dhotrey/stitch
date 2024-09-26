package squish

import (
	"bytes"
	"io"

	"github.com/charmbracelet/log"
	"github.com/ulikunitz/xz"
)

func Squash(data []byte) []byte {
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

func UnSquish(data []byte) []byte {
	var buf bytes.Buffer
	var out bytes.Buffer
	buf.Write(data)
	r, err := xz.NewReader(&buf)
	if err != nil {
		log.Fatalf("NewReader error %s", err)
	}
	if _, err = io.Copy(&out, r); err != nil {
		log.Fatalf("io.Copy error %s", err)
	}
	return out.Bytes()
}
