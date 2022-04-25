package main
import "fmt";
func main(){
	var a * int;
	c:=10
	a=&c;
	print(*a)
	var * b int;
	*b=*c
	print(*b);
}