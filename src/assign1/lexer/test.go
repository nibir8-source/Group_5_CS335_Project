package main

func main() {
	// dsonvjdjvnlfs \n sicscinsv\'983849&*&**&**

	/* SNVJKIDNVNDVNLDNVN
	   CSDVCJDNVJ&*&(*)*) */

	var a int = 42
	var b int = 4_2
	var z int = 0b10101011
	var y int = 0b10000100
	var c int = 0600
	var d int = 0_600
	var e int = 0o600
	var f int = 0o600 // second character is capital letter 'O'
	var g int = 0xBadFace
	var h int = 0xBad_Face
	var i int = 0x_67_7a_2f_cc_40_c6
	var j uint64 = 170141183460469231
	var k int = 170_141183_460469_231
	var _43 int = 56
	var tr int = _42         // an identifier, not an integer literal
	var er int = 42_         // invalid: _ must separate successive digits
	var yu int = 4__2        // invalid: only one _ at a time
	var gh int = 0_xBadFace  // invalid: _ must separate successive digits

}
