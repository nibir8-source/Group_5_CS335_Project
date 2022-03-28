package main
import "fmt"
func factorial(n int) (int) {
    if (n == 0 || n == 1) {
        return 1
    }    
    if n < 0 {
        return -1
    }
    return n*factorial(n - 1)
}

func sum(p,q int)(int){
	return p+q
}

func main(){
   var l int =factorial(10)
   //All types of expression
   var e1,e2,e3,e4,e5,e6,e7,e8 = 10,11,12,13,14,15,16,17
   e1=e1+e2
   e3=e4*e5
   s:=10.1
   s=e1+e2 
   e7=e7|e8&e1
   e7=e7<<4
   e7=e7>>4
   e7+=e2
   d:=3*4*(5+6+7)-3*(-3)
}


