package shredder

import "github.com/theredditbandit/stitch/ares/utils"

func Shred(dataStruct utils.Data) [][]byte {
	compressedBinaryData := dataStruct.CompressedData
	chunkSize := dataStruct.ChunkSize

	offset := 0
	dataSize := len(compressedBinaryData)
	chunks := [][]byte{}
	for {
		if offset+chunkSize > dataSize {
			piece := compressedBinaryData[offset:]
			chunks = append(chunks, piece)
			break
		}
		piece := compressedBinaryData[offset : offset+chunkSize]
		chunks = append(chunks, piece)
		offset += chunkSize
	}

	return chunks
}

func Unshred(data utils.Data) []byte {
	chunks := data.DataChunks
	unshreaded := []byte{}
	for _, chunk := range chunks {
		unshreaded = append(unshreaded, chunk...)
	}
	return unshreaded
}
