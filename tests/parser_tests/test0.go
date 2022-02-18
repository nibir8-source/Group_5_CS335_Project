package main;

import "fmt";

func main() {
	var n, m int;
	// scan n,m;
	fmt.Scanf("%d", &n);
	fmt.Scanf("%d", &m);

	var a, b, c [100][100]int;
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			// scan a[i][j];
			fmt.Scanf("%d", &a[i][j]);
		};
	};

	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			// scan b[i][j];
			fmt.Scanf("%d", &b[i][j]);
		};
	};

	// Do matmul
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			ans := 0;
			for k := 0; k < m; k++ {
				ans = ans + a[i][k]*b[k][j];
			};
			c[i][j] = ans;
		};
	};

	// Print
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			// print c[i][j];
			fmt.Print(c[i][j]);
		};
	};

};
