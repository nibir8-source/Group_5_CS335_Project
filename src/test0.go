package main

import "Fmt"
import "String"
import "Math"
type Address struct {
	name string 
	street string
	city string
	state string
	Pincode int
}

func myFunc(x,y int) (string) {
	if (x+y)==5 {
		return "Equal condition satisfied"
	} else {
		return "Not satisfied"
	}
}


func main(){

	var our_add Address;
	our_add.name="Nibir Baruah"

	a,b,c:= 10,20,30
	if(a>b){
		s:="helloworld"
		our_add.city=s

	} else {
		l:=100
	}
	today := 97979;
    khnik := today<<3
	switch khnik {
	case today + 0:
		var x,y int;
		var z string;
		x=2;y=3;
		z=myFunc(x,y);
	case today + 1:
		var x,y int;
		var z string;
		x=1;y=6;
	case today + 2:
		is := "sfdf"
	default:
		is:="Too far away."
	};






}
