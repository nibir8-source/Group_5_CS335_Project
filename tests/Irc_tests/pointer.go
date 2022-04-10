package main
import "fmt"

func main() {
	var a *int
	var b *int
	*a = 5
	*b = 6
	*a = *b

	var c *int 
	*c = *a
	*c ++
}
