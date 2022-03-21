package main

import (
	"bufio"
	"fmt"
	"mmseg/internal/mmseggo"
	"os"
)

func main() {
	filename := "../dataset/data.txt"
	dict := mmseggo.NewDict(filename)
	// read raw data and form them in a []string
	file, _ := os.Open("../dataset/raw.txt")
	defer file.Close()
	reader := bufio.NewReader(file)
	var sentences []string
	for {
		line, _, err := reader.ReadLine()
		if err != nil {
			break
		}
		sentences = append(sentences, string(line))
	}

	for _, sentence := range sentences {
		result := dict.CutWholeSentence(sentence)
		fmt.Println(result)
	}
}
