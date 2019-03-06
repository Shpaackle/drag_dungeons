# Python program for Kruskal's algorithm to find
# Minimum Spanning Tree of a given connected,
# undirected and weighted graph

from collections import defaultdict


# Class to represent a graph
class Graph:

    def __init__(self, vertices=0):
        self.V = vertices  # No. of vertices
        self.graph = []  # default dictionary
        # to store graph
        self.result = None

    # function to add an edge to graph
    def add_edge(self, point, u, v, w):
        self.graph.append([point, u, v, w])

        # A utility function to find set of an element i

    # (uses path compression technique)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

        # A function that does union of two sets of x and y

    # (uses union by rank)
    def union(self, parent, rank, x, y):
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)

        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root

            # If ranks are same, then make one as root
        # and increment its rank by one
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    # The main function to construct MST using Kruskal's
    # algorithm
    def kruskal_MST(self):
        print(len(self.graph))
        result = []  # This will store the resultant MST

        i = 0  # An index variable, used for sorted edges
        e = 0  # An index variable, used for result[]

        # Step 1: Sort all the edges in non-decreasing
        # order of their
        # weight. If we are not allowed to change the
        # given graph, we can create a copy of graph
        self.graph = sorted(self.graph, key=lambda item: item[3])

        parent = []
        rank = []

        # Create V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

            # Number of edges to be taken is equal to V-1
        while e < self.V - 1:

            # Step 2: Pick the smallest edge and increment
            # the index for next iteration
            point, u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # If including this edge doesn't cause cycle,
            # include it in result and increment the index
            # of result for next edge
            if x != y:
                e += 1
                result.append([point, u, v, w])
                self.union(parent, rank, x, y)
                # Else discard the edge

        self.result = result

    def print(self):
        # print the contents of result[] to display the built MST
        for point, u, v, weight in self.result:
            print(f"{point!s:>8}\t{u}\t{v}\t{weight}")


if __name__ == "__main__":
    # Driver code
    g = Graph(5)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 6)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 4)

    g.kruskal_MST()

# This code is contributed by Neelam Yadav
# https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/