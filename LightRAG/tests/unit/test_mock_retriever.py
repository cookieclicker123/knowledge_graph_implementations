import pytest
import uuid

from LightRAG.models.data_models import Chunk, Query, RetrieverResult
from LightRAG.models.enums import  RetrievalMode
from LightRAG.tests.mocks.mock_factory import create_mock_rag_pipeline, MockPipelineConfig

# --- Test Data ---
def create_sample_chunk(id: str, doc_id: str, content: str) -> Chunk:
    return Chunk(id=id, document_id=doc_id, content=content)

chunk_A1 = create_sample_chunk("cA1", "docA", "Content A part 1")
chunk_A2 = create_sample_chunk("cA2", "docA", "Content A part 2")
chunk_B1 = create_sample_chunk("cB1", "docB", "Content B part 1")

# --- Test Cases ---

@pytest.fixture
def basic_retriever_config() -> MockPipelineConfig:
    """Provides a basic config with some chunks and one predefined result."""
    return MockPipelineConfig(
        initial_chunks=[chunk_A1, chunk_A2, chunk_B1],
        retriever_predefined_results={
            "find content A": [chunk_A1, chunk_A2]
        }
    )

@pytest.mark.asyncio
async def test_retriever_predefined_result(basic_retriever_config: MockPipelineConfig):
    """Test retrieving results defined in the mock config."""
    _, retriever, _ = create_mock_rag_pipeline(basic_retriever_config)

    query_text = "find content A"
    query_id = str(uuid.uuid4())
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.VECTOR)

    result: RetrieverResult = await retriever.retrieve(user_query)

    assert result.query_id == query_id
    assert len(result.retrieved_chunks) == 2
    assert {chunk.id for chunk in result.retrieved_chunks} == {"cA1", "cA2"}
    assert result.scores is not None
    assert len(result.scores) == 2

@pytest.mark.asyncio
async def test_retriever_fallback_search(basic_retriever_config: MockPipelineConfig):
    """Test retriever falling back to mock storage search when no predefined result exists."""
    _, retriever, _ = create_mock_rag_pipeline(basic_retriever_config)

    query_text = "find something else"
    query_id = str(uuid.uuid4())
    # Ask for top 2 results
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.VECTOR, top_k=2)

    result: RetrieverResult = await retriever.retrieve(user_query)

    assert result.query_id == query_id
    # Mock storage search returns first k chunks (cA1, cA2 in this case based on order)
    assert len(result.retrieved_chunks) == 2
    assert {chunk.id for chunk in result.retrieved_chunks}.issubset({chunk_A1.id, chunk_A2.id, chunk_B1.id})

@pytest.mark.asyncio
async def test_retriever_respects_top_k_in_fallback(basic_retriever_config: MockPipelineConfig):
    """Test that the fallback search uses the query's top_k value."""
    _, retriever, _ = create_mock_rag_pipeline(basic_retriever_config)

    query_text = "find everything"
    query_id = str(uuid.uuid4())
    # Ask for top 5 results (more than available)
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.VECTOR, top_k=5)

    result: RetrieverResult = await retriever.retrieve(user_query)

    assert result.query_id == query_id
    # Should return all 3 available chunks from mock storage
    assert len(result.retrieved_chunks) == 3
    assert {chunk.id for chunk in result.retrieved_chunks} == {chunk_A1.id, chunk_A2.id, chunk_B1.id} 