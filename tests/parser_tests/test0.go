package main
import "ghth"
func mulReturn (a string) (string,string){
    var x,y string
    x=a
    y=a
    return x,y
}
func main(){
    var a string ="ufsrhgihgi"
    var b,c string
    (b),c = mulReturn(a)
};