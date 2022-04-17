package main

import (
	"bufio"
	"fmt"
	"log"
	"mmseg/internal/mmseggo"
	"os"
	"strings"
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
	writeFile, err := os.OpenFile("../../result/mmseg_cut_result.txt", os.O_WRONLY|os.O_CREATE, 0666)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	buf := bufio.NewWriter(writeFile)
	for _, sentence := range sentences {
		result := dict.CutWholeSentence(sentence)
		fmt.Println(result)
		cutSentence := strings.Join(result, "_")
		buf.WriteString(cutSentence + "\n")
	}
	buf.Flush()
	log.Println("export result to file result/mmseg_cut_result.txt")
}
