package main;

import "fmt";

func mul(a1, a2 int) int {

	res := a1 * a2;
	fmt.Println(res);
	return 0;
};

type simple_struct struct {
	orange, apple float64;
};

func main() {
	var varvarelseIf = 1;
	var switch_1_const = "hello_world"; //playing with different identifiers names
	var _Hello234world = 2;

	m := make(map[string]simple_struct);

	m["key1"] = simple_struct{
		40, -74.399,
	};

	fmt.Println(m["key1"]);

	map_1 := make(map[string]int);

	map_1["k1"] = 7;
	map_1["k2"] = 13;

	fmt.Println("map:", map_1);

	v1 := map_1["k1"];
	fmt.Println("v1: ", v1);

	fmt.Println("len:", len(map_1));

	delete(map_1, "k2");
	fmt.Println("map:", map_1);

	_, prs := map_1["k2"];
	fmt.Println("prs:", prs);

	n := map[string]int{"foo": 1, "bar": 2};
	fmt.Println("map:", n);

	a := 20.25;           //float assignment condition
	b := 10 + 20i;        //complex variable initialisation
	c := 314159e-5;       //float assignment in diff way
	const Correct = true; //assgning bool to const
	p, q, r := 80, 70, 60;
	Arithmatic_operators := (p + q - r + p*q + p/r) % q;
	Relational_logical_operator := (p == q) && (p != r) || (q < r) && (!(r <= q)) || (p > r) || (p >= r);
	Bitwise_opeartor := p&q + p ^ q + p | q + p<<2 + q>>2 + p&^q;

	fmt.Println(switch_1_const, a, b, c, Arithmatic_operators, Relational_logical_operator, Bitwise_opeartor, Correct);
	//Assignment operators
	p += p;
	p -= p;
	p *= p;
	p /= p + 1;
	p %= p + 1;
	p &= p;
	p |= p;
	p ^= p;

}
