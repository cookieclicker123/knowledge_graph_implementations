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

**Environment Variables:**

Many examples require API keys or other configuration. 
1. Navigate to the `LightRAG` directory.
2. Copy the example environment file: `cp .env.example .env`
3. Edit the new `.env` file and add your actual API keys (e.g., `OPENAI_API_KEY`). Ensure `OPENAI_API_BASE` is also set (usually to `https://api.openai.com/v1` for standard OpenAI).
   *Note: The `.env` file is typically ignored by version control (add it to `.gitignore`) to keep secrets safe.*

Python scripts using libraries like `python-dotenv` (which `lightrag-hku` might use internally, or you might add explicitly) can automatically load these variables. Otherwise, you might need to `export` them manually before running scripts if they don't load automatically.

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
# Ensure you have set up your .env file as described above
# Then, run examples from the root 'knowledge_graphs' directory:

# Run the first simple example:
python -m LightRAG.examples.01_simple_LightRAG_impl

# Run the second example (processing a text document):
python -m LightRAG.examples.02_document_LightRAG_impl

# Run the third example (processing pre-parsed PDF text):
# Note: Requires 01_basic_pymupdf_parser.py to be run first.
python -m LightRAG.examples.03_pdf_LightRAG_impl
```

## Parsing Document Examples

This section contains scripts focused specifically on parsing documents (like PDFs) using different methods before potentially feeding them into a RAG system like LightRAG. The goal is to compare the outputs and complexities of various parsing techniques.

Parsed outputs will typically be saved in `LightRAG/tmp/pdf_parsing_outputs/`.

**1. Basic PyMuPDF Text Extraction:**

This script uses the `PyMuPDF` library (`fitz`) to perform basic text extraction from the `light_rag.pdf` file. It extracts plain text content page by page.

```bash
# Ensure PyMuPDF is installed (see LightRAG_requirements.txt)
# Run from the root 'knowledge_graphs' directory:
python -m LightRAG.examples.parsing_documents_examples.01_basic_pymupdf_parser
```

*(More parsing examples comparing different methods will be added here)*


