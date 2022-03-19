package mmseggo

import (
	"bufio"
	"bytes"
	"mmseg/internal/chunk"
	"mmseg/internal/word"
	"os"
	"strconv"
)

// Dictionary for matching
type Dictionary struct {
	Wordmap map[string]*word.Word
}

func NewDict(filename string) *Dictionary {
	// read corpus
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// build Dictionary
	reader := bufio.NewReader(file)
	var wordMap map[string]*word.Word
	wordMap = make(map[string]*word.Word)

	for {
		line, _, readErr := reader.ReadLine()
		if readErr != nil {
			break
		}
		info := bytes.Split(line, []byte("\t"))
		text := string(info[0])
		freq, _ := strconv.Atoi(string(info[1]))
		wordMap[text] = word.NewWord(text, freq)
	}
	return &Dictionary{Wordmap: wordMap}
}

func (d *Dictionary) Get(text string) (*word.Word, bool) {
	w, ok := d.Wordmap[text]
	return w, ok
}

// MatchWords is to match all possible words at the head of the text
func (d *Dictionary) MatchWords(text string) []*word.Word {
	var (
		matchString string = ""
		matchWords  []*word.Word
	)
	for _, char := range text {
		matchString += string(char)
		if w, ok := d.Get(matchString); ok {
			matchWords = append(matchWords, w)
		}
	}
	if len(matchWords) == 0 {
		strChinese := []rune(text)
		matchWords = append(matchWords, word.NewWord(string(strChinese[0]), 0))
	}
	return matchWords
}

// GetChunks is to get all possible words chunks which contains at most 3 words
func (d *Dictionary) GetChunks(text string) []*chunk.Chunk {
	var chunks []*chunk.Chunk
	for _, word1 := range d.MatchWords(text) {
		textLength := len(text)
		word1Length := len(word1.Text)
		if word1Length < textLength {
			text1 := string([]byte(text)[word1Length:])
			for _, word2 := range d.MatchWords(text1) {
				word2Length := len(word2.Text)
				if word2Length < len(text1) {
					text2 := string([]byte(text)[word1Length+word2Length:])
					for _, word3 := range d.MatchWords(text2) {
						chunks = append(chunks, chunk.NewChunk([]*word.Word{word1, word2, word3}))
					}
				} else {
					chunks = append(chunks, chunk.NewChunk([]*word.Word{word1, word2}))
				}
			}
		} else {
			chunks = append(chunks, chunk.NewChunk([]*word.Word{word1}))
		}
	}
	return chunks
}

func (d *Dictionary) Filter(chunks []*chunk.Chunk) *chunk.Chunk {
	var filterChunks []*chunk.Chunk
	var maxLength int = 0
	// rule1
	for _, ch := range chunks {
		if maxLength < ch.Length() {
			filterChunks = []*chunk.Chunk{ch}
			maxLength = ch.Length()
		} else if maxLength == ch.Length() {
			filterChunks = append(filterChunks, ch)
		}
	}

	// rule2
	var avergeLenChunks []*chunk.Chunk
	var maxAverageLength float64 = 0.0
	for _, ch := range filterChunks {
		if maxAverageLength < ch.AverageLength() {
			avergeLenChunks = []*chunk.Chunk{ch}
		} else if maxAverageLength == ch.AverageLength() {
			avergeLenChunks = append(avergeLenChunks, ch)
		}
	}

	// rule3
	var varianceChunks []*chunk.Chunk
	var maxVariance float64 = avergeLenChunks[0].AverageLength()
	for _, ch := range avergeLenChunks {
		if maxVariance > ch.VarianceOfWords() {
			varianceChunks = []*chunk.Chunk{ch}
			maxVariance = ch.VarianceOfWords()
		} else if maxVariance == ch.VarianceOfWords() {
			varianceChunks = append(varianceChunks, ch)
		}
	}

	// rule4
	var singleCharChunks []*chunk.Chunk
	var maxSingleDegree float64 = varianceChunks[0].SingleWordFreq()
	for _, ch := range varianceChunks {
		if maxSingleDegree < ch.SingleWordFreq() {
			singleCharChunks = []*chunk.Chunk{ch}
			maxSingleDegree = ch.SingleWordFreq()
		} else if maxSingleDegree == ch.SingleWordFreq() {
			singleCharChunks = append(singleCharChunks, ch)
		}
	}

	// if there exists more than 1 chunks, choose the first one as the final result
	return singleCharChunks[0]
}

// GetOneWord is to cut the first word of the whole sentence
func (d *Dictionary) GetOneWord(text string) string {
	allPossibleChunks := d.GetChunks(text)
	filteredChunk := d.Filter(allPossibleChunks)
	return filteredChunk.Words[0].Text
}

// CutWholeSentence returns the segmentation of the sentence
func (d *Dictionary) CutWholeSentence(text string) []string {
	var pos int = 0
	var result []string

	for pos < len(text) {
		cutedText := string([]byte(text)[pos:])
		firstWord := d.GetOneWord(cutedText)
		result = append(result, firstWord)
		pos += len(firstWord)
	}
	return result
}
