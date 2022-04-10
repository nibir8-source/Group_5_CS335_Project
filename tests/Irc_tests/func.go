package main
import "fmt"
func calc(x,y int , z float) {
	var a int
	var b float
	a = (x+y)*(x-y)
	b = z*z*z*z*z*z
}

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
	var s int =sum(4,5)
	calc(1,2,3.1)
	
 }
