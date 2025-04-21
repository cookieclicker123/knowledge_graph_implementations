import networkx as nx

G = nx.Graph()

# Add nodes with attributes
G.add_node(1, time='5pm')
G.add_node(3, color='blue', label='Node 3')

# Add nodes from a list of tuples (node, attribute_dict)
nodes_with_attrs = [
    (2, {"color": "red"}),
    ("spam", {"food": True, "label": "Spam Node"})
]
G.add_nodes_from(nodes_with_attrs)


# Add edges with attributes
G.add_edge(1, 2, weight=4.7)
G.add_edge(3, "spam", capacity=15, label='Edge 3-Spam')

# Add multiple edges with attributes from a list of tuples
# (node1, node2, attribute_dict)
edges_with_attrs = [
    (1, 3, {"weight": 0.9, "relation": "friend"}),
    (2, "spam", {"weight": 8})
]
G.add_edges_from(edges_with_attrs)


print("Nodes and their attributes:")
for node, attributes in G.nodes(data=True):
    print(f"  Node: {node}, Attributes: {attributes}")

print("\nEdges and their attributes:")
for u, v, attributes in G.edges(data=True):
    print(f"  Edge: ({u}, {v}), Attributes: {attributes}")

# Access specific attributes
print(f"\nNode 1 time: {G.nodes[1]['time']}")
print(f"Edge (1, 2) weight: {G.edges[1, 2]['weight']}") 