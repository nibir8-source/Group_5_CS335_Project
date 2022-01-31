package main

import "fmt"

func init() {
	return 0
}
func mul(a1, a2 int) int {

	res := a1 * a2
	fmt.Println(res)
	return 0
}

func main() {
	var varvarelseIf = 1
	var switch_1_const = "hello_world" //playing with different identifiers names
	var _Hello234world = 2
	var map_1 map[int]int

	a := 20.25           //float assignment condition
	b := 10 + 20i        //complex variable initialisation
	c := 314159e-5       //float assignment in diff way
	const Correct = true //assgning bool to const
	p, q, r := 80, 70, 60
	Arithmatic_operators := (p + q - r + p*q + p/r) % q
	Relational_logical_operator := (p == q) && (p != r) || (q < r) && (!(r <= q)) || (p > r) || (p >= r)
	Bitwise_opeartor := p&q + p ^ q + p | q + p<<2 + q>>2 + p&^q
	//Assignment operators
	p += p
	p -= p
	p *= p
	p /= p
	p %= p
	p &= p
	p |= p
	p ^= p

LOOP:
	for i := 0; i < 4; i++ {
		if p < 100 {
			if q == 100 {
				fmt.Printf("Nibir")
			} else if q > 100 {
				break
			} else if q < 300 {
				q--
			} else {
				goto LOOP
			}
		}
	}
	var string = "GeeksforGeeks"
	for i, item := range string {

	}

	switch day := 2; day {
	case 1:
		fallthrough
	case 2:
	default:
	}

	select {
	// case 1 for portal 1
	case p := <-q:

	}
	type tank interface {
	}

	fmt.Println(varvarelseIf)
	fmt.Printf("The value of myvariable1 is : %d\n", _Hello234world)
	defer mul(11, 11)

	//taking true as identifier

	//issue with complex numbers
	//issue with fmtprintln

	//int32 int 16 encoded or not
	//int as identifier
	//address (&)   pointer(*)
	//OR_ASSIGNMENT(!=)

}
