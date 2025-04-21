# Knowledge Graph implementations

## Graphs

We are going to start by adding exmaples of implementing two knowledge graphs:

 - **NetworkX**: for familiarity with lower level graph concepts like nodes and edges and how to index and search over them.
 - **LightRAG**: for a more involved demo where we will index many files and review the potential of the hybrid LightRAG framework in production compared to more traditional similairty search methods.


## Initial setup:

```bash
git clone 
cd knowledge_graph_implementations

which python3.11,12,13 #3.11>

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

pip install -r NetworkX_requirements.txt
pip install -r LightRAG_requirements.txt
```

### NetworkX

```bash
cd NetworkX

python examples/01_basic_graph_creation.py
python examples/02_basic_graph_iteration.py
python examples/03_iteration_neighbors_copy.py
python examples/04_graph_types_copy.py
python examples/05_basic_algorithms.py
# Run a simple demo to see the graphs in action on a simple but case
python NetworkX_demo.py
```

Here are some exmaples and a demo for you to run, increasing in complexity:


Here are the pytests to run:

### LightRAG

```bash
cd LightRAG
```

Here are some exmaples and a demo for you to run, increasing in complexity:


Here are the pytests to run: