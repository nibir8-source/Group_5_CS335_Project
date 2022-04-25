package main

import "fmt"

func main() {
	for i := 0; i<20; i++ {
		if i < 7 {
			i++
			continue
		}
		print(i)
		if i > 15 {
			break
		}
	}
}
