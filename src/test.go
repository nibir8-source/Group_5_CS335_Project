package main
import "fmt"

func main() {
	var a *int
	var b *int
	*a = 5
	*b = 6
	*a = *b
	// *a = 5
	// *b = 6
	// c := *a + *b
	// print(c)
	// *a = *b

	// var c *int 
	// *c = *a
	// *c ++
}
