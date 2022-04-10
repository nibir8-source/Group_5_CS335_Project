package main
import "fmt"
type pair struct {
    x,y int
    z struct *pair
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


}


