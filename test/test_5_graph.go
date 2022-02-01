package main

import (
	"fmt"
	"errors"
)

// Color provides a type for vertex color
type Color int

// Graph provides a structure to store an undirected graph.
// It is safe to use its empty object.
type Graph struct {
	vertices int
	edges    map[int]map[int]struct{}
}

// AddVertex will add a new vertex in the graph, if the vertex already
// exist it will do nothing
func (g *Graph) AddVertex(v int) {
	if g.edges == nil {
		g.edges = make(map[int]map[int]struct{})
	}

	// Check if vertex is present or not
	if _, ok := g.edges[v]; !ok {
		g.vertices++
		g.edges[v] = make(map[int]struct{})
	}
}

// AddEdge will add a new edge between the provided vertices in the graph
func (g *Graph) AddEdge(one, two int) {
	// Add vertices: one and two to the graph if they are not present
	g.AddVertex(one)
	g.AddVertex(two)

	// and finally add the edges: one->two and two->one for undirected graph
	g.edges[one][two] = struct{}{}
	g.edges[two][one] = struct{}{}
}

func (g *Graph) ValidateColorsOfVertex(colors map[int]Color) error {
	if g.vertices != len(colors) {
		return errors.New("coloring: not all vertices of graph are colored")
	}
	// check colors
	for vertex, neighbours := range g.edges {
		for nb := range neighbours {
			if colors[vertex] == colors[nb] {
				return errors.New("coloring: same colors of neighbouring vertex")
			}
		}
	}
	return nil
}

func (g *Graph) TryBipartiteColoring() map[int]Color {
	// 0 is uncolored, 1/2 is colors
	colors := make(map[int]Color)
	visited := make(map[int]bool)

	for i := range g.edges {
		colors[i] = 0
		visited[i] = false
	}

	var color_node func(int)
	color_node = func(s int) {
		visited[s] = true
		coloring := []Color{0, 2, 1}

		for n := range g.edges[s] {
			if colors[n] == 0 {
				colors[n] = coloring[colors[s]]
			}
			if !visited[n] {
				color_node(n)
			}
		}
	}

	for i := range g.edges {
		if colors[i] == 0 {
			colors[i] = 1
			color_node(i)
		}
	}

	return colors
}

// basically tries to color the graph in two colors if each edge
// connects 2 differently colored nodes the graph can be considered bipartite
func BipartiteCheck(N int, edges [][]int) bool {
	var graph Graph
	for i := 0; i < N; i++ {
		graph.AddVertex(i)
	}
	for _, e := range edges {
		graph.AddEdge(e[0], e[1])
	}
	return graph.ValidateColorsOfVertex(graph.TryBipartiteColoring()) == nil
}

var testCases = []struct {
	name        string
	N           int
	isBipartite bool
	edges       [][]int
}{
	{
		"basic true", 2, true,
		[][]int{{1, 0}},
	},
	{
		"basic false", 3, false,
		[][]int{{0, 1}, {1, 2}, {2, 0}},
	},
}

func main() {
	for _, tc := range testCases {
		actual := BipartiteCheck(tc.N, tc.edges)
		fmt.Print(actual, "\n")
	}
}
