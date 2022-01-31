package main

import "fmt"

type simple_struct struct {
	orange, apple float64
}

var m map[string]simple_struct

func main() {

	m := make(map[string]simple_struct)

	m["key1"] = simple_struct{
		40, -74.399,
	}
	fmt.Println(m["key1"])

	m1 := make(map[string]int)

	m1["k1"] = 7
	m1["k2"] = 13

	fmt.Println("map:", m1)

	v1 := m1["k1"]
	fmt.Println("v1: ", v1)

	fmt.Println("len:", len(m1))

	delete(m1, "k2")
	fmt.Println("map:", m1)

	_, prs := m1["k2"]
	fmt.Println("prs:", prs)

	n := map[string]int{"foo": 1, "bar": 2}
	fmt.Println("map:", n)
}
