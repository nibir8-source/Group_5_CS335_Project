package main

import (
	"fmt"
	"sort"
	"strings"
)

type NoTextToEncryptError struct{}
type KeyMissingError struct{}

func (n *NoTextToEncryptError) Error() string {
	return "No text to encrypt"
}
func (n *KeyMissingError) Error() string {
	return "Missing Key"
}

func getKey(keyWord string) []int {
	keyWord = strings.ToLower(keyWord)
	word := []rune(keyWord)
	var sortedWord = make([]rune, len(word))
	copy(sortedWord, word)
	sort.Slice(sortedWord, func(i, j int) bool { return sortedWord[i] < sortedWord[j] })
	usedLettersMap := make(map[rune]int)
	wordLength := len(word)
	resultKey := make([]int, wordLength)
	for i := 0; i < wordLength; i++ {
		char := word[i]
		numberOfUsage := usedLettersMap[char]
		resultKey[i] = getIndex(sortedWord, char) + numberOfUsage + 1 //+1 -so that indexing does not start at 0
		numberOfUsage++
		usedLettersMap[char] = numberOfUsage
	}
	return resultKey
}

func getIndex(wordSet []rune, subString rune) int {
	n := len(wordSet)
	for i := 0; i < n; i++ {
		if wordSet[i] == subString {
			return i
		}
	}
	return 0
}

func Encrypt(text []rune, keyWord string) (string, error) {
	key := getKey(keyWord)
	space := ' '
	keyLength := len(key)
	textLength := len(text)
	if keyLength <= 0 {
		return "", &KeyMissingError{}
	}
	if textLength <= 0 {
		return "", &NoTextToEncryptError{}
	}
	n := textLength % keyLength

	for i := 0; i < keyLength-n; i++ {
		text = append(text, space)
	}
	textLength = len(text)
	result := ""
	for i := 0; i < textLength; i += keyLength {
		transposition := make([]rune, keyLength)
		for j := 0; j < keyLength; j++ {
			transposition[key[j]-1] = text[i+j]
		}
		result += string(transposition)
	}
	return result, nil
}

func Decrypt(text []rune, keyWord string) (string, error) {
	key := getKey(keyWord)
	textLength := len(text)
	if textLength <= 0 {
		return "", &NoTextToEncryptError{}
	}
	keyLength := len(key)
	if keyLength <= 0 {
		return "", &KeyMissingError{}
	}
	space := ' '
	n := textLength % keyLength
	for i := 0; i < keyLength-n; i++ {
		text = append(text, space)
	}
	result := ""
	for i := 0; i < textLength; i += keyLength {
		transposition := make([]rune, keyLength)
		for j := 0; j < keyLength; j++ {
			transposition[j] = text[i+key[j]-1]
		}
		result += string(transposition)
	}
	return result, nil
}

func main() {
	var palintext string = `
	Three Rings for the Elven-kings under the sky,
	Seven for the Dwarf-lords in their halls of stone,
	Nine for Mortal Men doomed to die,
	One for the Dark Lord on his dark throne
	In the Land of Mordor where the Shadows lie.
	One Ring to rule them all, One Ring to find them,
	One Ring to bring them all and in the darkness bind them
	In the Land of Mordor where the Shadows lie.
	`

	// get a key
	var Key string = "Gandalf"

	// encrypt
	var Encypted, _ = Encrypt([]rune(palintext), Key)

	// print encrypted
	fmt.Printf(Encypted)

	// decrypt
	var Decrypted, _ = Decrypt([]rune(Encypted), Key)

	fmt.Print("\n \n")

	// print decrypted
	fmt.Print(Decrypted)
}
