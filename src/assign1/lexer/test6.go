package main

func main() {
	// dsonvjdjvnlfs \n sicscinsv\'983849&*&**&**

	/* SNVJKIDNVNDVNLDNVN
	   CSDVCJDNVJ&*&(*)*) */
	   'a'
	   'ä'
	   '本'
	   '\t'
	   '\000'
	   '\007'
	   '\377'
	   '\x07'
	   '\xff'
	   '\u12e4'
	   '\U00101234'
	   '\''         // rune literal containing single quote character
	   '\"'
	   '\\'
	   'aa'         // illegal: too many characters
	   '\xa'        // illegal: too few hexadecimal digits
	   '\0'         // illegal: too few octal digits
	   '\uDFFF'     // illegal: surrogate half
	   '\U00110000' // illegal: invalid Unicode code point

}
