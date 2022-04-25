package main
import "math"
type marksheet struct{
	var assignment int;
	var quiz int;
	var project float;
}
func main(){
	var a[10] marksheet;
	for i:=0; i<10;i++{
		a[i].assignment=i+10
		a[i].quiz=30
		a[i].project=12.2

		print(a[i].assignment)
	}
	
}

