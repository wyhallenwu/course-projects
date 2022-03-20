package manytimepad

import (
	"strings"
)

const (
	blank = byte(' ')
)

// HexXor returns the XOR result in []byte type
func HexXor(x []byte, y []byte) []byte {
	length := func(x []byte, y []byte) int {
		if len(x) < len(y) {
			return len(x)
		} else {
			return len(y)
		}
	}(x, y)

	var result []byte
	for i := 0; i < length; i++ {
		result = append(result, x[i]^y[i])
	}
	return result

}

func XorWithOthers(index int, encryptMessage [][]byte) [][]byte {
	var xorResult [][]byte
	for ix, message := range encryptMessage {
		if ix != index {
			xorWithOther := HexXor(encryptMessage[index], message)
			xorResult = append(xorResult, xorWithOther)
		}
	}
	return xorResult
}

func Isalpha(b byte) bool {
	if (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z') {
		return true
	}
	return false
}

func IsSpace(b byte) bool {
	if b == ' ' {
		return true
	}
	return false
}

func Compute(xorResult [][]byte) []int {
	// get shortest length of a single xor message
	var length int = len(xorResult[0])
	for _, xorMessage := range xorResult {
		if len(xorMessage) < length {
			length = len(xorMessage)
		}
	}
	var spaceCount [200]int
	for i := 0; i < length; i++ {
		for j := 0; j < len(xorResult); j++ {
			if Isalpha(xorResult[j][i]) {
				spaceCount[i] += 1
			}
		}
	}
	return spaceCount[:]
}

func GetSpaceIndex(spaceCount []int) []int {
	var KnownSpaceIndex []int
	for ix, val := range spaceCount {
		if val >= 6 {
			KnownSpaceIndex = append(KnownSpaceIndex, ix)
		}
	}
	return KnownSpaceIndex
}

func Infer(knownSpaceIndex []int, message []byte, finalKey []byte) {
	// all space hex string
	var spaceMessage = []byte(strings.Repeat(" ", 200))
	xorWithSpace := HexXor(message, spaceMessage)
	for _, valIndex := range knownSpaceIndex {
		if finalKey[valIndex] == '\x00' {
			finalKey[valIndex] = xorWithSpace[valIndex]
		}
	}
}

func DecryptKey(encryptMessage [][]byte) []byte {
	var finalKey [200]byte
	for ix, message := range encryptMessage {
		xorResult := XorWithOthers(ix, encryptMessage)
		spaceIndex := Compute(xorResult)
		knowSpaceIndex := GetSpaceIndex(spaceIndex)
		Infer(knowSpaceIndex, message, finalKey[:])
	}
	return finalKey[:]
}

func Decrypt(encryptMessage [][]byte, target []byte) string {
	key := DecryptKey(encryptMessage)
	hexResult := HexXor(target, key)
	var decryptTarget string = ""
	for _, val := range hexResult {
		if Isalpha(val) || IsSpace(val) {
			decryptTarget += string(val)
		} else {
			decryptTarget += "*"
		}
	}

	return decryptTarget

}
