package main

import "fmt"

func main() {
	var b [5]int
	d := 0 
	len := 5
	for i := 0; i < len; i++ {
		scan(d)
		b[i] = d
	}

	for i := 0; i < len; i = i + 1 {
		for j := 0; j < (len-1); j = j + 1 {
			if b[j] > b[j+1] {
				c := b[j]
				b[j] = b[j+1]
				b[j+1] = c
			}
		}
	}

	for i := 0; i < len; i = i + 1 {
		d = b[i]
		print(d)
	}
}
