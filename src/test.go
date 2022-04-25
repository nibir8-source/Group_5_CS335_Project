package main;

// Output: 27 331

func main(){
    var a *int
	*a = 5
	var b *int = &a
	c := *b
	print(c)
};