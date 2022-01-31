package main

import "fmt"

/*
   return list of primes less than N
   input integer N
   output array of primes less than N
*/
func sieveOfEratosthenes(N int) (primes []int) {
	b := make([]bool, N)
	for i := 2; i < N; i++ {
		if b[i] == true {
			// not prime
			continue
		}
		primes = append(primes, i)
		for k := i * i; k < N; k += i {
			b[k] = true
		}
	}
	return
}

func main() {
	primes := sieveOfEratosthenes(100)
	for _, p := range primes {
		fmt.Println(p)
	}
}
