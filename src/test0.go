package main
import "fmt"
type pair struct {
    x,y int
    z struct *pair
}
type Vertex struct{
    s int
    t int
    u struct *Vertex
}
func our_func (a Vertex,b int ) (int){
    a.s=(*(a.u)).s
    a.t=(*(a.u)).t
    return a.s+a.t
}

func main()  {
	var a [10]pair
    for i:=0;i<10;i++{
        if(i%2==(0|0)){
            a[i].x=i+(i>>3)
            a[i].y=i+(i&(i+1))
        } else {
            a[i].x=56
            a[i].y=a[i].x
        }
        if(i!=0){
            a[i].z=&(a[i-1])
        }
    }

	var var1,var2 Vertex
    var b *int
    *b=2
    var1.u=&var2
    var1.s=1
    var1.t=2
    var2.s=3
    var2.t=4
    f := our_func(var1,7)
}


