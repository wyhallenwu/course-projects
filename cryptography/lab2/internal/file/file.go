package file

import (
	"bufio"
	"encoding/hex"
	"io"
	"os"
)

// ReadEncryptFile returns a []byte of the encrypted message
func ReadEncryptFile(filename string) ([][]byte, []byte) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	f := bufio.NewReader(file)
	var encryptMessage [][]byte
	var targetMessage []byte
	for {
		line, _, err := f.ReadLine()
		h, _ := hex.DecodeString(string(line))
		if err == io.EOF {
			break
		} else {
			encryptMessage = append(encryptMessage, h)
		}
	}
	targetMessage = encryptMessage[len(encryptMessage)-1]
	encryptMessage = encryptMessage[:len(encryptMessage)-1]
	return encryptMessage, targetMessage
}
