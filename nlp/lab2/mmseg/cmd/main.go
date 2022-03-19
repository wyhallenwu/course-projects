package main

import (
	"fmt"
	"mmseg/internal/mmseggo"
)

func main() {
	filename := "../dataset/data.txt"
	dict := mmseggo.NewDict(filename)
	var text = []string{"张志刚是一名信息员", "中关村是中国的硅谷", "我们必须坚持马克思主义和毛泽东思想",
		"明天可能会下雨", "请不要大声喧哗"}
	for _, sentence := range text {
		result := dict.CutWholeSentence(sentence)
		fmt.Println(result)
	}
}
