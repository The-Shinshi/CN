# Develop a program to find the shortest path between vertices using the Bellman-Ford

class Edge:
    def __init__(self, source, destination, weight):
        self.source = source
        self.destination = destination
        self.weight = weight


def bellman_ford(graph, vertices, edges, source):
    distance = [float('inf')] * vertices
    distance[source] = 0

    for _ in range(vertices - 1):
        for edge in edges:
            if distance[edge.source] != float('inf') and distance[edge.source] + edge.weight < distance[edge.destination]:
                distance[edge.destination] = distance[edge.source] + edge.weight

    for edge in edges:
        if distance[edge.source] != float('inf') and distance[edge.source] + edge.weight < distance[edge.destination]:
            print("Negative cycle detected")
            return

    print("Vertex   Distance from Source")
    for i in range(vertices):
        print(f"{i} \t\t {distance[i]}")


def main():
    vertices = 6
    graph_edges = [
        Edge(0, 1, 5),
        Edge(0, 2, 7),
        Edge(1, 2, 3),
        Edge(1, 3, 4),
        Edge(1, 4, 6),
        Edge(3, 4, -1),
        Edge(3, 5, 2),
        Edge(4, 5, -3)
    ]

    bellman_ford(graph_edges, vertices, graph_edges, 0)


if __name__ == "__main__":
    main()
