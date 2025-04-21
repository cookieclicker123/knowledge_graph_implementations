import networkx as nx
import matplotlib.pyplot as plt # Optional: for visualization

# Create a graph - let's use a slightly more complex one
# This is a Peterson graph modified slightly
G = nx.Graph()
G.add_edges_from([
    (1, 2), (1, 3), (1, 4), (2, 5), (2, 6),
    (3, 7), (3, 8), (4, 9), (4, 10),
    (5, 7), (5, 9), (6, 8), (6, 10),
    (7, 10), (8, 9)
])
G.add_node(11) # Add an isolated node

# --- Shortest Path --- 
print("--- Shortest Path ---")
try:
    # Find the shortest path between node 1 and node 10
    path = nx.shortest_path(G, source=1, target=10)
    print(f"Shortest path between 1 and 10: {path}")

    # Find the length (number of edges) of the shortest path
    length = nx.shortest_path_length(G, source=1, target=10)
    print(f"Length of shortest path between 1 and 10: {length}")

    # Find shortest path to an unreachable node (node 11)
    #path_to_11 = nx.shortest_path(G, source=1, target=11) # This would raise NetworkXNoPath
except nx.NetworkXNoPath:
    print("Node 11 is not reachable from node 1.")


# --- Degree Centrality ---
# Measures the number of edges connected to a node (normalized)
print("\n--- Degree Centrality ---")
degree_centrality = nx.degree_centrality(G)
print("Degree Centrality:")
for node, centrality in degree_centrality.items():
    print(f"  Node {node}: {centrality:.3f}")

# Find the node with the highest degree centrality
most_central_node = max(degree_centrality, key=degree_centrality.get)
print(f"Node with highest degree centrality: {most_central_node}")

# --- Other Centrality Measures (Examples) ---
# Closeness Centrality: Average shortest path distance to all other nodes
# Betweenness Centrality: How often a node lies on the shortest path between others
print("\n--- Other Centrality Measures (Examples) ---")
closeness_centrality = nx.closeness_centrality(G)
print(f"Closeness Centrality (Node 1): {closeness_centrality[1]:.3f}")

betweenness_centrality = nx.betweenness_centrality(G)
print(f"Betweenness Centrality (Node 4): {betweenness_centrality[4]:.3f}")


# --- Optional: Drawing the graph ---
# You might need to install matplotlib: pip install matplotlib
print("\n--- Drawing Graph (Optional) ---")
try:
    pos = nx.spring_layout(G) # Position nodes using Fruchterman-Reingold force-directed algorithm
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
    plt.title("Sample Graph for Algorithm Demo")
    plt.show() # Uncomment to display the plot
    print("Graph drawing generated (plot display commented out). Install matplotlib if needed.")
except ImportError:
    print("Matplotlib not found. Skipping graph drawing.") 