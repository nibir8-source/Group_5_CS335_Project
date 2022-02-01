package main

func main() {
	// dsonvjdjvnlfs \n sicscinsv\'983849&*&**&**

	/* SNVJKIDNVNDVNLDNVN
	   CSDVCJDNVJ&*&(*)*) */
	   var a string = `abc`                // same as "abc"
		var b string = `\n
		\n`                  // same as "\\n\n\\n"
		var c string = `fjdnvjdnv
		vdjvdjnvjdv
		vdjvnjdnvjdv\n`			// string
		var d string = "\n"
		var e string = "\""                 // same as `"`
		var f string = "Hello, \" world!\n"
		var b string = "日本語"
		var c string = "\u65e5本\U00008a9e"
		var f string = "\xff\u00FF"
		var g string = "\uD800"             // illegal: surrogate half
		var h string = "\U00110000"         // illegal: invalid Unicode code point

		var i string = "日本語"                                 // UTF-8 input text
		var j string = `日本語`                                 // UTF-8 input text as a raw literal
		var fg string = "\u65e5\u672c\u8a9e"                    // the explicit Unicode code points
		var fgt string = "\U000065e5\U0000672c\U00008a9e"        // the explicit Unicode code points
		var ty string = "\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e"  // the explicit UTF-8 bytes

}
