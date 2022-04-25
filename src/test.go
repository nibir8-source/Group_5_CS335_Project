package main
import "fmt"

func fact (x int) (int) {
	if x == 1 {
		return x
	}else {
		return x * fact(x - 1)
	}	
}

func main() {
	a := fact(7)
	print(a)
}
