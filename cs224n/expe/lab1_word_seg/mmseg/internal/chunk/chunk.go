package chunk

import (
	"math"
	"mmseg/internal/word"
)

//const ChunkLength int = 3

type Chunk struct {
	Words []*word.Word
}

func NewChunk(w []*word.Word) *Chunk {
	return &Chunk{Words: w}
}

// four rules

//Length returns all characters of one chunk(rule 1)
func (c *Chunk) Length() int {
	length := 0
	for _, word := range c.Words {
		length += len(word.Text)
	}
	return length
}

// AverageLength returns average length of the chunk(3 words) (rule 2)
func (c *Chunk) AverageLength() float64 {
	return float64(c.Length()) / float64(len(c.Words))
}

// VarianceOfWords returns the variance of the chunk
func (c *Chunk) VarianceOfWords() float64 {
	averageLength := c.AverageLength()
	var numerator float64
	for _, word := range c.Words {
		numerator += math.Pow(float64(len(word.Text))-averageLength, 2.0)
	}
	return math.Sqrt(numerator / float64(len(c.Words)))
}

//SingleWordFreq returns single character log frequency summation
func (c *Chunk) SingleWordFreq() float64 {
	var freq float64
	for _, word := range c.Words {
		if len(word.Text) == 1 {
			freq += math.Log(float64(word.Freq))
		}
	}
	return freq
}
