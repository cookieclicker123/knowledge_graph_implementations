import networkx as nx
import matplotlib.pyplot as plt

# --- Create a Knowledge Graph representing a simple project team ---
KG = nx.DiGraph() # Directed graph to show relationships

# Nodes represent entities (People, Projects, Skills)
# Add people with roles
KG.add_node("Alice", type="Person", role="Developer")
KG.add_node("Bob", type="Person", role="Project Manager")
KG.add_node("Charlie", type="Person", role="Designer")
KG.add_node("David", type="Person", role="Developer")

# Add projects
KG.add_node("Project Alpha", type="Project", status="Ongoing")
KG.add_node("Project Beta", type="Project", status="Planning")

# Add skills
KG.add_node("Python", type="Skill")
KG.add_node("UX Design", type="Skill")
KG.add_node("Project Management", type="Skill")
KG.add_node("Database", type="Skill")

# Edges represent relationships between entities
# 'works_on' relationship (Person -> Project)
KG.add_edge("Alice", "Project Alpha", relation="works_on")
KG.add_edge("Bob", "Project Alpha", relation="works_on")
KG.add_edge("Charlie", "Project Alpha", relation="works_on")
KG.add_edge("David", "Project Beta", relation="works_on")
KG.add_edge("Bob", "Project Beta", relation="works_on")

# 'has_skill' relationship (Person -> Skill)
KG.add_edge("Alice", "Python", relation="has_skill")
KG.add_edge("Alice", "Database", relation="has_skill")
KG.add_edge("Bob", "Project Management", relation="has_skill")
KG.add_edge("Charlie", "UX Design", relation="has_skill")
KG.add_edge("David", "Python", relation="has_skill")

# 'requires_skill' relationship (Project -> Skill)
KG.add_edge("Project Alpha", "Python", relation="requires_skill")
KG.add_edge("Project Alpha", "UX Design", relation="requires_skill")
KG.add_edge("Project Alpha", "Project Management", relation="requires_skill")
KG.add_edge("Project Beta", "Python", relation="requires_skill")
KG.add_edge("Project Beta", "Database", relation="requires_skill")

# --- Demonstrate Graph Usefulness ---

print("--- Knowledge Graph Demo ---")
print(f"Total entities (nodes): {KG.number_of_nodes()}")
print(f"Total relationships (edges): {KG.number_of_edges()}")

# --- Querying the Graph --- 
print("\n--- Querying the Knowledge Graph ---")

# Q1: Who works on Project Alpha?
print("\nQ1: Who works on Project Alpha?")
for person in KG.predecessors("Project Alpha"): # Find nodes pointing TO Project Alpha
    # Check if the predecessor is a Person and the relationship is 'works_on'
    if KG.nodes[person]['type'] == 'Person' and KG.get_edge_data(person, "Project Alpha")['relation'] == 'works_on':
        print(f" - {person} ({KG.nodes[person]['role']})")

# Q2: What skills does Alice have?
print("\nQ2: What skills does Alice have?")
for skill in KG.successors("Alice"): # Find nodes Alice points TO
    if KG.nodes[skill]['type'] == 'Skill' and KG.get_edge_data("Alice", skill)['relation'] == 'has_skill':
        print(f" - {skill}")

# Q3: Which developers know Python?
print("\nQ3: Which developers know Python?")
for person in KG.predecessors("Python"): # People pointing to Python skill
    if KG.nodes[person]['type'] == 'Person' and KG.nodes[person]['role'] == 'Developer' and KG.get_edge_data(person, "Python")['relation'] == 'has_skill':
        print(f" - {person}")

# Q4: Is Project Beta feasible with the current team assigned (Bob, David)?
# Check if required skills are met by assigned people
print("\nQ4: Checking skill coverage for Project Beta (Bob, David)")
required_skills = {skill for project, skill, data in KG.out_edges("Project Beta", data=True) if data['relation'] == 'requires_skill'}
print(f"  Required skills: {required_skills}")

assigned_people = {person for person, project, data in KG.in_edges("Project Beta", data=True) if data['relation'] == 'works_on'}
print(f"  Assigned people: {assigned_people}")

available_skills = set()
for person in assigned_people:
    person_skills = {skill for p, skill, data in KG.out_edges(person, data=True) if data['relation'] == 'has_skill'}
    available_skills.update(person_skills)
print(f"  Available skills from team: {available_skills}")

missing_skills = required_skills - available_skills
if not missing_skills:
    print("  Conclusion: All required skills are covered by the assigned team.")
else:
    print(f"  Conclusion: Missing skills for Project Beta: {missing_skills}")

# --- Graph Analysis --- 
print("\n--- Basic Graph Analysis ---")
# Example: Find the most connected people (highest degree)
degrees = dict(KG.degree()) # Combined in-degree and out-degree
people_degrees = {node: degrees[node] for node, data in KG.nodes(data=True) if data['type'] == 'Person'}
most_connected_person = max(people_degrees, key=people_degrees.get)
print(f"Most connected person (interactions): {most_connected_person} with degree {people_degrees[most_connected_person]}")

# --- Visualization (Optional) ---
print("\n--- Visualizing the Knowledge Graph ---")
plt.figure(figsize=(12, 10))

# Define colors for node types
node_colors = []
for node in KG.nodes(data=True):
    if node[1]['type'] == 'Person':
        node_colors.append('skyblue')
    elif node[1]['type'] == 'Project':
        node_colors.append('lightgreen')
    elif node[1]['type'] == 'Skill':
        node_colors.append('salmon')
    else:
        node_colors.append('gray')

# Use a layout algorithm
pos = nx.spring_layout(KG, k=0.9, iterations=50) # Increase k for more spread

# Draw nodes, edges, and labels
nx.draw_networkx_nodes(KG, pos, node_size=2500, node_color=node_colors)
nx.draw_networkx_edges(KG, pos, arrowstyle='->', arrowsize=15, edge_color='gray', alpha=0.6)
nx.draw_networkx_labels(KG, pos, font_size=9)

# Draw edge labels (optional, can get cluttered)
edge_labels = nx.get_edge_attributes(KG, 'relation')
# nx.draw_networkx_edge_labels(KG, pos, edge_labels=edge_labels, font_size=7)

plt.title("Project Team Knowledge Graph")
plt.axis('off') # Turn off the axis
plt.show() # Uncomment to display the plot
print("Graph drawing generated (plot display commented out).")
print("\nThis demo shows how a graph can represent complex relationships and answer structured questions, forming the basis for knowledge graph applications.") 