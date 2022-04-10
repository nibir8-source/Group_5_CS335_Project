package main
import "fmt"
func main(){
	//Trying Different If conditions and for conditions
	a:=10
	b:=20 
	//Nested If statement
	if (a>b){
		var c = 1
		if(c<10){
			m:=10
			if (c<8){
				z:=10
			}
		}else {
			m:=12
		}
	} else{
		a=a+b

	}
	//Nested for statement
	for i := 2; i < 100; i++ {
		for j := 2; j <= (i/j); j++ {
		   if(i%j==0) {
			  break; 
		   }
		
		if(j > (i/j)) {
		   p:="Helloworld"
		   continue;
		}
	 } 
	}

	//Switch Case 

	temp:=0
	temp=0
	var x [10]*int
	hell0:=666
	switch(2+2/2) {
		case 3*6*4/2+3*6/8-2-2*6: 
			var y int=1
		case 3:
			var z int=0
			
			
		default:
			var x int =2
	}



}



