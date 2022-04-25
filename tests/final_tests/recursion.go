package main

import "fmt"

func f(m int, n int) (int) {
	if m == 0 {
		return n + 1
	}

	if n == 0 {
		return f(m-1, 1)
	}

	return f(m-1, f(m, n-1))
}

func main() {
    print(f(3, 4))
}
