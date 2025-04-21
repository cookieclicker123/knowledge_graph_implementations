import networkx as nx

G = nx.Graph()

# Add edges (nodes are implicitly created)
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, "spam")])

print("Iterating through all nodes:")
for node in G.nodes:
    print(f"  Node: {node}")

print("\nIterating through all edges:")
for u, v in G.edges:
    print(f"  Edge: ({u}, {v})")

# Get neighbors of node 1
print("\nNeighbors of node 1:")
for neighbor in G.neighbors(1):
    print(f"  Neighbor: {neighbor}")

# Can also use G[node] to get neighbors (returns an iterator)
print("\nNeighbors of node 4 (using G[node]):")
neighbors_of_4 = list(G[4]) # Convert iterator to list for printing
print(f"  Neighbors: {neighbors_of_4}")

print(f"\nNumber of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}") 