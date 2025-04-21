from typing import List, Dict, Optional, Tuple, AsyncGenerator
import uuid
from dataclasses import dataclass, field

from LightRAG.core.interfaces import BaseRetriever, BaseGenerator, BaseVectorStorage
from LightRAG.models.data_models import Document, Chunk, Query, RetrieverResult, GeneratorContext, GeneratorResponse, Metadata
from LightRAG.models.enums import RetrievalMode, DataSource

# --- Mock Component Implementations ---

class MockVectorStorage(BaseVectorStorage):
    """A simple in-memory mock for vector storage and basic retrieval."""
    def __init__(self, documents: Dict[str, Document] = None, chunks: Dict[str, Chunk] = None):
        self._documents: Dict[str, Document] = documents or {}
        self._chunks: Dict[str, Chunk] = chunks or {}
        self._chunk_embeddings: Dict[str, List[float]] = {
            chunk_id: chunk.embedding
            for chunk_id, chunk in self._chunks.items()
            if chunk.embedding is not None
        }

    async def add_document(self, document: Document) -> None:
        self._documents[document.id] = document

    async def add_chunks(self, chunks_to_add: List[Chunk]) -> None:
        for chunk in chunks_to_add:
            self._chunks[chunk.id] = chunk
            if chunk.embedding:
                self._chunk_embeddings[chunk.id] = chunk.embedding

    async def get_document(self, doc_id: str) -> Optional[Document]:
        return self._documents.get(doc_id)

    async def get_chunk(self, chunk_id: str) -> Optional[Chunk]:
        return self._chunks.get(chunk_id)

    async def get_chunks_by_doc_id(self, doc_id: str) -> List[Chunk]:
        return [chunk for chunk in self._chunks.values() if chunk.document_id == doc_id]

    async def search_similar_chunks(self, query_embedding: List[float], top_k: int, filters: Optional[Metadata] = None) -> List[Chunk]:
        # Extremely naive mock similarity: just return the first top_k chunks
        # A real mock might calculate dummy distances or use pre-defined results
        print(f"MockVectorStorage: Searching with top_k={top_k} (Ignoring embedding and filters)")
        all_chunk_ids = list(self._chunks.keys())
        result_ids = all_chunk_ids[:top_k]
        return [self._chunks[id] for id in result_ids if id in self._chunks]

class MockRetriever(BaseRetriever):
    """Mock retriever that uses a mock storage or predefined results."""
    def __init__(self, storage: BaseVectorStorage, predefined_results: Optional[Dict[str, List[Chunk]]] = None):
        self.storage = storage
        # Maps query text to list of chunks to return
        self.predefined_results = predefined_results or {}

    async def retrieve(self, query: Query) -> RetrieverResult:
        print(f"MockRetriever: Retrieving for query '{query.text}' (mode: {query.mode})")
        if query.text in self.predefined_results:
            chunks = self.predefined_results[query.text]
            print(f"  -> Using predefined result for query: {query.text}")
        else:
            # Fallback to mock storage search (ignoring embedding quality)
            # In a real scenario, we might need a mock embedder
            mock_embedding = [0.0] * 10 # Dummy embedding
            chunks = await self.storage.search_similar_chunks(mock_embedding, query.top_k, query.filters)
            print(f"  -> Using fallback mock storage search (found {len(chunks)} chunks)")

        return RetrieverResult(
            query_id=query.id,
            retrieved_chunks=chunks,
            scores=[1.0] * len(chunks) # Dummy scores
        )

class MockGenerator(BaseGenerator):
    """Mock generator that returns predefined answers."""
    def __init__(self, predefined_answers: Optional[Dict[str, str]] = None):
        # Maps query text to the answer string
        self.predefined_answers = predefined_answers or {}

    async def generate(self, context: GeneratorContext) -> GeneratorResponse:
        query_text = context.query.text
        print(f"MockGenerator: Generating for query '{query_text}'")

        if query_text in self.predefined_answers:
            answer = self.predefined_answers[query_text]
            print(f"  -> Using predefined answer for query: {query_text}")
        else:
            answer = f"Mock answer for query: '{query_text}'. Context chunks: {[c.id for c in context.retrieved_context.retrieved_chunks]}"
            print("  -> Using default generated mock answer.")

        return GeneratorResponse(
            query_id=context.query.id,
            answer=answer,
            context_used=[c.id for c in context.retrieved_context.retrieved_chunks]
        )

    async def stream_generate(self, context: GeneratorContext) -> AsyncGenerator[str, None]:
        response = await self.generate(context)
        # Simulate streaming by yielding parts of the answer
        words = response.answer.split()
        for i in range(0, len(words), 2): # Yield two words at a time
            yield " ".join(words[i:i+2]) + (" " if i+2 < len(words) else "")
        # Ensure the generator finishes
        if False: yield # Should not be reached

# --- Mock Configuration Dataclass ---

@dataclass
class MockPipelineConfig:
    """Configuration for creating a mock RAG pipeline."""
    initial_documents: List[Document] = field(default_factory=list)
    initial_chunks: List[Chunk] = field(default_factory=list)
    # Maps query text -> list of chunks to be retrieved
    retriever_predefined_results: Dict[str, List[Chunk]] = field(default_factory=dict)
    # Maps query text -> predefined answer string
    generator_predefined_answers: Dict[str, str] = field(default_factory=dict)

# --- Mock Factory Function ---

def create_mock_rag_pipeline(config: MockPipelineConfig) -> Tuple[BaseVectorStorage, BaseRetriever, BaseGenerator]:
    """
    Factory function to create and configure mock RAG components.

    Args:
        config: Configuration dataclass specifying initial data and predefined behaviors.

    Returns:
        A tuple containing instances of (MockVectorStorage, MockRetriever, MockGenerator).
    """
    print("\n--- Creating Mock RAG Pipeline ---")
    # 1. Create Mock Storage
    mock_storage = MockVectorStorage()
    print(f"Initializing MockVectorStorage...")
    # Use asyncio.run or manage event loop if needed for async methods here
    # For simplicity in mock setup, we might call async methods directly if they are simple
    # await mock_storage.add_document(...) # Requires async context or event loop management
    # Instead, initialize directly:
    mock_storage = MockVectorStorage(
        documents={doc.id: doc for doc in config.initial_documents},
        chunks={chunk.id: chunk for chunk in config.initial_chunks}
    )
    print(f"  Added {len(config.initial_documents)} initial documents.")
    print(f"  Added {len(config.initial_chunks)} initial chunks.")


    # 2. Create Mock Retriever
    mock_retriever = MockRetriever(
        storage=mock_storage,
        predefined_results=config.retriever_predefined_results
    )
    print(f"Initialized MockRetriever with {len(config.retriever_predefined_results)} predefined results.")

    # 3. Create Mock Generator
    mock_generator = MockGenerator(
        predefined_answers=config.generator_predefined_answers
    )
    print(f"Initialized MockGenerator with {len(config.generator_predefined_answers)} predefined answers.")
    print("--- Mock Pipeline Creation Complete ---\n")

    return mock_storage, mock_retriever, mock_generator

# --- Example Usage (for demonstration) ---

async def example_mock_usage():
    # Define some mock data
    doc1 = Document(id="doc1", content="This is the first document.", source=DataSource.TEXT)
    chunk1 = Chunk(id="chunk1", document_id="doc1", content="first document chunk 1")
    chunk2 = Chunk(id="chunk2", document_id="doc1", content="first document chunk 2")

    doc2 = Document(id="doc2", content="A second document about cats.", source=DataSource.FILE)
    chunk3 = Chunk(id="chunk3", document_id="doc2", content="Cats are furry.")
    chunk4 = Chunk(id="chunk4", document_id="doc2", content="Cats like naps.")

    # Configure the mock pipeline
    config = MockPipelineConfig(
        initial_documents=[doc1, doc2],
        initial_chunks=[chunk1, chunk2, chunk3, chunk4],
        retriever_predefined_results={
            "tell me about doc1": [chunk1, chunk2],
            "what about cats?": [chunk3, chunk4]
        },
        generator_predefined_answers={
            "tell me about doc1": "Document 1 is about the first document.",
            "what is the second doc about?": "The second document is about cats."
        }
    )

    # Create the mock components
    storage, retriever, generator = create_mock_rag_pipeline(config)

    # Simulate a query flow
    print("\n--- Simulating Query Flow ---")
    query_text = "what about cats?"
    query_id = str(uuid.uuid4())
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.HYBRID, top_k=2)
    print(f"User Query: {user_query}")

    # 1. Retrieval
    retriever_result = await retriever.retrieve(user_query)
    print(f"Retriever Result: {retriever_result}")

    # 2. Generation
    generator_context = GeneratorContext(query=user_query, retrieved_context=retriever_result)
    generator_response = await generator.generate(generator_context)
    print(f"Generator Response: {generator_response}")

    # 3. Streaming Generation (Example)
    query_text_stream = "tell me about doc1"
    query_id_stream = str(uuid.uuid4())
    user_query_stream = Query(id=query_id_stream, text=query_text_stream, mode=RetrievalMode.VECTOR, top_k=2)
    retriever_result_stream = await retriever.retrieve(user_query_stream)
    generator_context_stream = GeneratorContext(query=user_query_stream, retrieved_context=retriever_result_stream)

    print("\nStreaming Generator Response:")
    async for token in generator.stream_generate(generator_context_stream):
        print(f"  Stream chunk: '{token}'")
    print("--- Simulation Complete ---")

if __name__ == "__main__":
    import asyncio
    # Need an event loop to run the async example function
    asyncio.run(example_mock_usage()) 