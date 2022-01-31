package main

func main() {
	// dsonvjdjvnlfs \n sicscinsv\'983849&*&**&**

	/* SNVJKIDNVNDVNLDNVN
	   CSDVCJDNVJ&*&(*)*) */

	   var a float64 = 0.
	   var b float64 = 72.40
	   var c float64 = 072.40       // == 72.40
	   var d float64 = 2.71828
	   var e float64 = 1.e+0
	   var f float64 = 6.67428e-11
	   var g float64 = 1E6
	   var h float64 = .25
	   var i float64 = .12345E+5
	   var i float64 = 1_5.         // == 15.0
	   var i float64 = 0.15e+0_2    // == 15.0
	   
	   var i float64 = 0x1p-2       // == 0.25
	   var i float64 = 0x2.p10      // == 2048.0
	   var i float64 = 0x1.Fp+0     // == 1.9375
	   var i float64 = 0X.8p-0      // == 0.5
	   var i float64 = 0X_1FFFP-16  // == 0.1249847412109375
	   var i float64 = 0x15e-2      // == 0x15e - 2 (integer subtraction)
	   
	   var i float64 = 0x.p1        // invalid: mantissa has no digits
	   var i float64 = 1p-2         // invalid: p exponent requires hexadecimal mantissa
	   var i float64 = 0x1.5e-2     // invalid: hexadecimal mantissa requires p exponent
	   var i float64 = 1_.5         // invalid: _ must separate successive digits
	   var i float64 = 1._5         // invalid: _ must separate successive digits
	   var i float64 = 1.5_e1       // invalid: _ must separate successive digits
	   var i float64 = 1.5e_1       // invalid: _ must separate successive digits
	   var i float64 = 1.5e1_       // invalid: _ must separate successive digits

}
