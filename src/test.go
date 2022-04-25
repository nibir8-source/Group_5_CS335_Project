package main

func main(){
    var a int
	b := 2
    scan(a)
    switch b {
        case 1:
            print(1)
        case 2:
            print(2)
        case b+1:
            print(b+1)
        case 4:
            print(4)
        default:
            print(100)
    }
}
