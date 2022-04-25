package main

func main(){
    var a int
	b := 2
    scan(a)
    switch a {
        case 1:
            print(1)
			break
        case 2:
            print(2)
			break
        case b+1:
            print(b+1)
        case (5 + (2 * 3) - (12 / 2) - 3) << 1:
            print(4)
        default:
            print(100)
    }
}
