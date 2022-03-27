package main
import "fmt"
func main() {
	flat_earthers_count:=0
	flat_earthers_count=0
	var x [10]*int
	Evil_Santa:=666
	switch(2+2/2) {
		case 3*6*4/2+3*6/8-2-2*6: 
			switch(*(x[0])) {
				case 1: for y:=0;y < *(x[y]);y++ {
							if(y<10) {
								*(x[y])=*(&y)
							} else {
								break;
							}
						}		
		    }
		case 3:
			var z int=0
			for z<10 {
				x[z]=&z
				z++
			}
			if(*x[z-1]!=z) {
				break		
			} else {
				flat_earthers_count+=1
			}
		default:
			for i:=0;i<10;i++ {
				x[i]=&Evil_Santa
			}
	}
}
