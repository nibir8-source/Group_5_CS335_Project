package main
import "math"
type def struct{
	a,b int;
};

func main(){
	var arr[10] def;
	for i:=0; i<10;i++{
		arr[i].a = i+10
		arr[i].b = 30
		c := arr[i].a + arr[i].b
		print(c)
	}
};




