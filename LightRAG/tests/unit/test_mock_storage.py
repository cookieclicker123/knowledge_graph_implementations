import pytest
import uuid
from datetime import datetime, timezone

from LightRAG.models.data_models import Document, Chunk
from LightRAG.models.enums import DataSource
from LightRAG.tests.mocks.mock_factory import MockVectorStorage

# Sample Data for Tests
TEST_DOC_ID_1 = "doc-001"
TEST_DOC_ID_2 = "doc-002"
TEST_CHUNK_ID_1 = "chunk-001a"
TEST_CHUNK_ID_2 = "chunk-001b"
TEST_CHUNK_ID_3 = "chunk-002a"

@pytest.fixture
def sample_doc1() -> Document:
    return Document(
        id=TEST_DOC_ID_1,
        content="This is the content of document 1.",
        source=DataSource.TEXT,
        timestamp=datetime.now(timezone.utc)
    )

@pytest.fixture
def sample_chunk1(sample_doc1: Document) -> Chunk:
    return Chunk(
        id=TEST_CHUNK_ID_1,
        document_id=sample_doc1.id,
        content="First chunk of document 1.",
        embedding=[0.1, 0.2, 0.3],
        metadata={"position": 0}
    )

@pytest.fixture
def sample_chunk2(sample_doc1: Document) -> Chunk:
    return Chunk(
        id=TEST_CHUNK_ID_2,
        document_id=sample_doc1.id,
        content="Second chunk of document 1.",
        embedding=[0.4, 0.5, 0.6],
        metadata={"position": 1}
    )

@pytest.fixture
def sample_doc2() -> Document:
    return Document(
        id=TEST_DOC_ID_2,
        content="Content for the second document.",
        source=DataSource.FILE,
        source_uri="/path/to/doc2.txt",
        timestamp=datetime.now(timezone.utc)
    )

@pytest.fixture
def sample_chunk3(sample_doc2: Document) -> Chunk:
    return Chunk(
        id=TEST_CHUNK_ID_3,
        document_id=sample_doc2.id,
        content="Only chunk of document 2.",
        embedding=[0.7, 0.8, 0.9],
        metadata={"position": 0}
    )

@pytest.mark.asyncio
async def test_add_and_get_document(sample_doc1: Document):
    """Test adding and retrieving a single document."""
    storage = MockVectorStorage()
    await storage.add_document(sample_doc1)
    retrieved_doc = await storage.get_document(sample_doc1.id)

    assert retrieved_doc is not None
    assert retrieved_doc.id == sample_doc1.id
    assert retrieved_doc.content == sample_doc1.content

@pytest.mark.asyncio
async def test_get_nonexistent_document():
    """Test retrieving a document that doesn't exist."""
    storage = MockVectorStorage()
    retrieved_doc = await storage.get_document("nonexistent-id")
    assert retrieved_doc is None

@pytest.mark.asyncio
async def test_add_and_get_chunks(sample_chunk1: Chunk, sample_chunk2: Chunk):
    """Test adding multiple chunks and retrieving one."""
    storage = MockVectorStorage()
    await storage.add_chunks([sample_chunk1, sample_chunk2])
    retrieved_chunk = await storage.get_chunk(sample_chunk1.id)

    assert retrieved_chunk is not None
    assert retrieved_chunk.id == sample_chunk1.id
    assert retrieved_chunk.content == sample_chunk1.content
    assert retrieved_chunk.embedding == sample_chunk1.embedding

@pytest.mark.asyncio
async def test_get_chunks_by_doc_id(sample_chunk1: Chunk, sample_chunk2: Chunk, sample_chunk3: Chunk):
    """Test retrieving all chunks associated with a specific document ID."""
    storage = MockVectorStorage()
    await storage.add_chunks([sample_chunk1, sample_chunk2, sample_chunk3])

    # Get chunks for doc1
    doc1_chunks = await storage.get_chunks_by_doc_id(TEST_DOC_ID_1)
    assert len(doc1_chunks) == 2
    assert {chunk.id for chunk in doc1_chunks} == {TEST_CHUNK_ID_1, TEST_CHUNK_ID_2}

    # Get chunks for doc2
    doc2_chunks = await storage.get_chunks_by_doc_id(TEST_DOC_ID_2)
    assert len(doc2_chunks) == 1
    assert doc2_chunks[0].id == TEST_CHUNK_ID_3

    # Get chunks for non-existent doc id
    nonexistent_chunks = await storage.get_chunks_by_doc_id("nonexistent-doc")
    assert len(nonexistent_chunks) == 0

@pytest.mark.asyncio
async def test_search_similar_chunks_mock(sample_chunk1: Chunk, sample_chunk2: Chunk, sample_chunk3: Chunk):
    """Test the mock similarity search behaviour."""
    storage = MockVectorStorage()
    await storage.add_chunks([sample_chunk1, sample_chunk2, sample_chunk3])

    # Mock search ignores embedding, just returns first k
    mock_embedding = [0.0] * 3
    results_top_2 = await storage.search_similar_chunks(mock_embedding, top_k=2)
    assert len(results_top_2) == 2
    # Order depends on internal dict order, so check IDs present
    assert {chunk.id for chunk in results_top_2}.issubset({TEST_CHUNK_ID_1, TEST_CHUNK_ID_2, TEST_CHUNK_ID_3})

    results_top_5 = await storage.search_similar_chunks(mock_embedding, top_k=5)
    assert len(results_top_5) == 3 # Only 3 chunks available
    assert {chunk.id for chunk in results_top_5} == {TEST_CHUNK_ID_1, TEST_CHUNK_ID_2, TEST_CHUNK_ID_3} 