package main

import (
	"fmt"
	"manytimepad/internal/file"
	"manytimepad/internal/manytimepad"
)

func main() {
	// get encrypt message and target message
	encryptMessage, target := file.ReadEncryptFile("../encrypt.txt")
	decryptMessage := manytimepad.Decrypt(encryptMessage, target)
	fmt.Println(decryptMessage)
}
