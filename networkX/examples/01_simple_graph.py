import networkx as nx

# Create an empty graph
G = nx.Graph() # Undirected graph

# Add single nodes
G.add_node(1)
G.add_node("spam") # Nodes can be numbers, strings, or any hashable object

# Add multiple nodes from a list
G.add_nodes_from([2, 3])

# Add single edges (nodes are created if they don't exist)
G.add_edge(1, 2)
G.add_edge("spam", 3)

# Add multiple edges from a list of tuples
G.add_edges_from([(1, 3), (2, "spam")])

print(f"Nodes: {G.nodes()}")
print(f"Edges: {G.edges()}")
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}") 