package main
import "fmt"

var e int = 5
var d int = 6

func main(){
    var a *int
    var b *int
    *a = 6
    *b = 8
    c := *a + *b
}
