package word

type Word struct {
	Text string
	Freq int
}

func NewWord(text string, freq int) *Word {
	return &Word{Text: text, Freq: freq}
}
