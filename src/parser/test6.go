package main

import "fmt"

func main() {
	
	type (
		A1 = string
		A2 = A1
	)

	type (
		B1 string
		B2 B1
		B3 []B1
		B4 B3
	)

	[32]byte
	[2*N] struct { x, y int32 }
	[1000]*float64
	[3][5]int
	[2][2][2]float64  // same as [2]([2]([2]float64))

	struct {
		x, y int
		u float32
		_ float32  // padding
		A *[]int
		F func()
	}

	struct {
		T1        // field name is T1
		*T2       // field name is T2
		P.T3      // field name is T3
		*P.T4     // field name is T4
		x, y int  // field names are x and y
	}

	struct {
		T     // conflicts with embedded field *T and *P.T
		*T    // conflicts with embedded field T and *P.T
		*P.T  // conflicts with embedded field T and *T
	}

	fmt.Println(34)
}
