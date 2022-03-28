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
			switch(*(x[0])) {
				case 1: for y:=0;y < *(x[y]);y++ {
							if(y<10) {
								*(x[y])=*(&y)
							} else {
								break;
							}
						}		
		    }
		case 3:
			var z int=0
			for z<10 {
				x[z]=&z
				z++
			}
			if(*x[z-1]!=z) {
				break		
			} else {
				temp+=1
			}
		default:
			for i:=0;i<10;i++ {
				x[i]=&hell0
			}
	}



}



