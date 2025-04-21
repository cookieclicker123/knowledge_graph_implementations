from typing import Protocol, List, Optional, AsyncGenerator
from ..models.data_models import Document, Chunk, Query, RetrieverResult, GeneratorContext, GeneratorResponse, Metadata

# Storage Interfaces
class BaseStorage(Protocol):
    """Interface for storing and retrieving documents and chunks."""

    async def add_document(self, document: Document) -> None:
        """Adds a single document to the storage."""
        ...

    async def add_chunks(self, chunks: List[Chunk]) -> None:
        """Adds multiple chunks to the storage."""
        ...

    async def get_document(self, doc_id: str) -> Optional[Document]:
        """Retrieves a document by its ID."""
        ...

    async def get_chunk(self, chunk_id: str) -> Optional[Chunk]:
        """Retrieves a chunk by its ID."""
        ...

    async def get_chunks_by_doc_id(self, doc_id: str) -> List[Chunk]:
        """Retrieves all chunks associated with a document ID."""
        ...

class BaseVectorStorage(BaseStorage, Protocol):
    """Interface specifically for vector storage and similarity search."""

    async def search_similar_chunks(self, query_embedding: List[float], top_k: int, filters: Optional[Metadata] = None) -> List[Chunk]:
        """Finds chunks with embeddings similar to the query embedding."""
        ...

# RAG Component Interfaces
class BaseRetriever(Protocol):
    """Interface for retrieving relevant context based on a query."""

    async def retrieve(self, query: Query) -> RetrieverResult:
        """Retrieves relevant chunks for a given query."""
        ...

class BaseGenerator(Protocol):
    """Interface for generating a response based on query and context."""

    async def generate(self, context: GeneratorContext) -> GeneratorResponse:
        """Generates an answer using the LLM."""
        ...

    async def stream_generate(self, context: GeneratorContext) -> AsyncGenerator[str, None]:
        """Streams the generated answer token by token."""
        # Yield intermediate results
        yield ""
        # Ensure the generator is properly defined
        if False: # Placeholder to make it a generator
            yield 