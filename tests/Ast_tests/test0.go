package main;

import "fmt";
import "math";
import "string";

type Address struct {
	name string 
	street string
	city string
	state string
	Pincode int
}

const c1,c2,c3 =1,2,3

var v1 ,v2,v3 float = 1,1.2,1.3 

func main(){
	// all type of variable Decl
	var a1 int;
	var  a2,a3,a4 int;
	var a5,a6 int = 10,20;
	var a7,a8 =1,2;
	 
	// all constants decl
	const a9 ;
	const a10,a11 = "helloworld","Hopefully code work"
	const a12, a13 int = 11,12


	//Short Decl 
	l:=10
	p,q,r:=1,2,"helloworld"

	//Array Decl 
	var myarr[10]string;

	//pointer decl 
	x := 10
	var s *int;
	s=&x

}
