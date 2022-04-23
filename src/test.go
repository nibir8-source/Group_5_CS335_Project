package main
import "fmt"

func main() {
	var a[4] int
	a[0] = 1
	a[1] = 2
	a[2] = 3
	a[3] = 4

	for i:=0 ; i<3; i++ {
		c := a[i] + a[i + 1]
		print(c)
	}

}
