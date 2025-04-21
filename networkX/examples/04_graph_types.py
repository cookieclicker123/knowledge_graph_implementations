import networkx as nx

# --- Directed Graph (DiGraph) ---
DG = nx.DiGraph()
DG.add_edge(1, 2, relation='follows')
DG.add_edge(2, 3, relation='mentions')
DG.add_edge(3, 1, relation='replies_to')
DG.add_edge(2, 1, relation='follows') # Different direction

print("--- Directed Graph (DiGraph) ---")
print(f"Nodes: {DG.nodes()}")
print(f"Edges: {DG.edges(data=True)}")
print(f"Successors of node 2: {list(DG.successors(2))}") # Nodes reachable from 2
print(f"Predecessors of node 2: {list(DG.predecessors(2))}") # Nodes pointing to 2
print(f"In-degree of node 1: {DG.in_degree(1)}") # Number of edges pointing to 1
print(f"Out-degree of node 1: {DG.out_degree(1)}") # Number of edges starting from 1


# --- MultiGraph ---
# Allows multiple edges between the same nodes
MG = nx.MultiGraph()
MG.add_edge(1, 2, relation='friend')
MG.add_edge(1, 2, relation='coworker') # Second edge between 1 and 2
MG.add_edge(2, 3, weight=5)

print("\n--- MultiGraph ---")
print(f"Nodes: {MG.nodes()}")
print(f"Edges (with keys): {MG.edges(keys=True, data=True)}")
print(f"Edges between 1 and 2: {MG.get_edge_data(1, 2)}") # Returns dict {key: attributes}
print(f"Number of edges between 1 and 2: {MG.number_of_edges(1, 2)}")


# --- MultiDiGraph ---
# Combines directed edges and multiple edges
MDG = nx.MultiDiGraph()
MDG.add_edge(1, 2, relation='like', timestamp='2024-01-01')
MDG.add_edge(1, 2, relation='retweet', timestamp='2024-01-02')
MDG.add_edge(2, 1, relation='reply')

print("\n--- MultiDiGraph ---")
print(f"Nodes: {MDG.nodes()}")
print(f"Edges (with keys): {MDG.edges(keys=True, data=True)}")
print(f"Edges from 1 to 2: {MDG.get_edge_data(1, 2)}")
print(f"Successors of node 1: {list(MDG.successors(1))}") 