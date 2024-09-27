package shredder

func Shred(chunkSize int, data []byte) [][]byte {
	offset := 0
	dataSize := len(data)
	chunks := [][]byte{}
	for {
		if offset+chunkSize > dataSize {
			piece := data[offset:]
			chunks = append(chunks, piece)
			break
		}
		piece := data[0:chunkSize]
		chunks = append(chunks, piece)
		offset += chunkSize
	}

	return chunks
}

func Unshred(chunks [][]byte) []byte {
	return nil
}
