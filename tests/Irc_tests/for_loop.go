package main
import "fmt"
func main(){
    var a int= 34<<45
    i:=0
    for {
		for j:=0; j<10; j++ {
			j++
		}

        if (56|i) < 78{
            continue
        }
        a=a+(56|i)
        i++
    }
}
