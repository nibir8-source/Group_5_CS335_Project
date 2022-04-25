package main
import "fmt";
func main(){
	var a *int;
	var b *int;
	*a = 10
	*b = 20
	var c int = *a
	var d int = *b
	print(c,d)
	a = b
	c = *a
	d = *b
	print(c,d)
}
