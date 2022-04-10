package main
import "fmt"
func main(){
    var d *int 
    var c *int
    *d = 5
    *c = 5
    *c = *d
}

