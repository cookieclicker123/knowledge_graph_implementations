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

Here are some exmaples and a demo for you to run, increasing in complexity:

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

### LightRAG

This section explores the LightRAG framework for building Retrieval-Augmented Generation pipelines.

**Project Structure:**

*   `LightRAG/`: Contains the core logic, examples, and tests for our LightRAG implementation.
*   `LightRAG/models/`: Pydantic models defining data structures (Documents, Chunks, etc.).
*   `LightRAG/core/`: Interfaces for core components (Storage, Retriever, Generator).
*   `LightRAG/tests/`: Contains unit and integration tests.
*   `LightRAG/tests/mocks/`: Mock implementations and a factory for testing.
*   `LightRAG/examples/`: Example scripts demonstrating LightRAG usage.
*   `LightRAG/pyproject.toml`: Defines the `LightRAG` directory as an installable Python package and manages dependencies.

**Setup:**

After activating your virtual environment (`source .venv/bin/activate`), ensure the necessary dependencies are installed. The `LightRAG` directory is set up as a Python package using `pyproject.toml`. To make it correctly importable by Python tools like `pytest` and scripts run with `python -m`, install it in "editable" mode along with its dependencies (including test dependencies):

```bash
# From the root 'knowledge_graphs' directory:
pip install -e "LightRAG[test]"
```

This command reads `LightRAG/pyproject.toml`, installs required packages like `lightrag-hku[api]` and `pytest`, and creates a link in your environment pointing to your `LightRAG` source code directory. This allows imports like `from LightRAG.models import ...` to work correctly everywhere.

**Running Mocks and Tests:**

To verify the basic setup and mock components:

```bash
# From the root 'knowledge_graphs' directory:

# 1. Run the mock factory example (demonstrates mock usage)
python -m LightRAG.tests.mocks.mock_factory

# 2. Run the unit tests (uses mocks to test component contracts)
pytest
```

**Examples:**

Example scripts demonstrating different LightRAG functionalities will be added here.

```bash
cd LightRAG
# python examples/01_simple_LightRAG_impl.py # (Example to be added)

```


