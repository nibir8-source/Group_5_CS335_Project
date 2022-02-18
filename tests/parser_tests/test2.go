package main

import (
	"math"
)

type Point struct {
	X, Y float64
}

type Line struct {
	P1, P2 Point
}

func Distance(a, b *Point) float64 {
	return math.Sqrt(math.Pow(a.X-b.X, 2) + math.Pow(a.Y-b.Y, 2))
}

func Section(p1, p2 *Point, r float64) Point {
	var point Point
	point.X = (r*p2.X + p1.X) / (r + 1)
	point.Y = (r*p2.Y + p1.Y) / (r + 1)
	return point
}

func Slope(l *Line) float64 {
	return (l.P2.Y - l.P1.Y) / (l.P2.X - l.P1.X)
}

func Intercept(p *Point, slope float64) float64 {
	return p.Y - (slope * p.X)
}

func IsParallel(l1, l2 *Line) bool {
	return Slope(l1) == Slope(l2)
}

func IsPerpendicular(l1, l2 *Line) bool {
	return Slope(l1)*Slope(l2) == -1
}

func PointDistance(p *Point, equation [3]float64) float64 {
	return math.Abs(equation[0]*p.X+equation[1]*p.Y+equation[2]) / math.Sqrt(math.Pow(equation[0], 2)+math.Pow(equation[1], 2))
}

func main() {
	p1 := Point{0, 0}
	p2 := Point{3, 4}

	var Distance float64 = Distance(&p1, &p2)
	if Distance != 5. {
		print("wrong distance")
	}

	var midpoint Point = Section(&p1, &p2, 1)
	if midpoint != (Point{1.5, 2.}) {
		print("wrong midpoint")
	}

	var equation [3]float64 = [3]float64{1, 1, 0}
	PointDistanc := PointDistance(&p2, equation)
	print("distace =", PointDistanc)

}
