package main

import "fmt"

func main() {
	//Different type of integer assignment
	a := 42
	b := 4_2
	c := 0666
	d := 0_666
	e := 0o666
	f := 0o65_4
	g := 0xBabeFace
	h := 0xBabe_Face
	i := 0x_67_7a_2f_cc_40_c6
	j := 170141183460469
	k := 170_141183_46046
	fmt.Println(a, b, c, d, e, f, g, h, i, j, k)

	//floating point assignment
	l := 0.
	m := 72.40
	n := 072.40
	o := 2.71828
	p := 1.e+0
	q := 6.67428e-11
	r := 1e6
	s := .25
	t := .12345e+5
	u := 1_5.
	v := 0.15e+0_2
	fmt.Println(l, m, n, o, p, q, r, s, t, u, v)

	la := 0x1p-2
	ma := 0x2.p10
	na := 0x1.Fp+0
	oa := 0x.8p-0
	pa := 0x_1FFFp-16
	fmt.Println(la, ma, na, oa, pa)

	//Imaginary number assignment
	qa := 0i
	qb := 123i
	qc := 0o123i
	qd := 0xabci
	qe := 0.i
	qf := 2.71828i
	qg := 1.e+0i
	qh := 6.67428e-11i
	qi := 1e6i
	qj := .25i
	qk := .12345e+5i
	ql := 0x1p-2i
	fmt.Println(qa, qb, qc, qd, qe, qf, qg, qh, qi, qj, qk, ql)

	//Rune literals

	r1 := '\a' // U+0007
	r2 := '\b' // U+0008
	r3 := '\f' //U+000C
	r4 := '\n' //U+000A
	r5 := '\r' //U+000D
	r6 := '\t' //U+0009
	r7 := '\v' //U+000B
	r8 := '\\' //U+005C
	r9 := '\'' //U+0027

	r11 := 'a'
	r12 := 'ä'
	r13 := '本'
	r14 := '\t'
	r15 := '\002'
	r16 := '\005'
	r17 := '\372'
	r18 := '\x02'
	r19 := '\xf4'
	r20 := '\u33e4'
	r21 := '\U00101234'
	fmt.Println(r1, r2, r3, r4, r5, r6, r7, r8, r9, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21)

	//string representation
	s1 := `abc`
	s2 := `\n
	\n`
	s4 := "\n"
	s5 := "\""
	s6 := "CS335 amazing course!\n"
	s7 := "日本語"
	s8 := "\u65e5本\U00008a9e"
	s9 := "\xff\u00FF"
	str := `vjn
	dnv\"dvd\n`
	fmt.Println(s1, s2, s4, s5, s6, s7, s8, s9, str)

}
