import pytest

from LightRAG.models.data_models import Query, Chunk, RetrieverResult, GeneratorContext, GeneratorResponse
from LightRAG.models.enums import RetrievalMode
from LightRAG.tests.mocks.mock_factory import create_mock_rag_pipeline, MockPipelineConfig

# --- Test Data ---
def create_sample_chunk(id: str, doc_id: str, content: str) -> Chunk:
    return Chunk(id=id, document_id=doc_id, content=content)

chunk_C1 = create_sample_chunk("cC1", "docC", "Context chunk C1")
chunk_C2 = create_sample_chunk("cC2", "docC", "Context chunk C2")

# --- Test Cases ---

@pytest.fixture
def basic_generator_config() -> MockPipelineConfig:
    """Provides a basic config with one predefined answer."""
    return MockPipelineConfig(
        generator_predefined_answers={
            "question about C": "This is the predefined answer about C."
        }
    )

@pytest.fixture
def sample_retriever_result() -> RetrieverResult:
    """Creates a sample retriever result to pass to the generator."""
    return RetrieverResult(
        query_id="q-gen-test",
        retrieved_chunks=[chunk_C1, chunk_C2],
        scores=[0.9, 0.8]
    )

@pytest.mark.asyncio
async def test_generator_predefined_answer(basic_generator_config: MockPipelineConfig, sample_retriever_result: RetrieverResult):
    """Test generating an answer defined in the mock config."""
    _, _, generator = create_mock_rag_pipeline(basic_generator_config)

    query_text = "question about C"
    query_id = sample_retriever_result.query_id # Use ID from retriever result
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.VECTOR)

    context = GeneratorContext(query=user_query, retrieved_context=sample_retriever_result)
    response: GeneratorResponse = await generator.generate(context)

    assert response.query_id == query_id
    assert response.answer == "This is the predefined answer about C."
    assert response.context_used == [chunk_C1.id, chunk_C2.id]

@pytest.mark.asyncio
async def test_generator_default_answer(basic_generator_config: MockPipelineConfig, sample_retriever_result: RetrieverResult):
    """Test generator providing a default mock answer when no predefined one exists."""
    _, _, generator = create_mock_rag_pipeline(basic_generator_config)

    query_text = "different question"
    query_id = sample_retriever_result.query_id
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.VECTOR)

    context = GeneratorContext(query=user_query, retrieved_context=sample_retriever_result)
    response: GeneratorResponse = await generator.generate(context)

    assert response.query_id == query_id
    expected_default_answer = f"Mock answer for query: '{query_text}'. Context chunks: {[chunk_C1.id, chunk_C2.id]}"
    assert response.answer == expected_default_answer
    assert response.context_used == [chunk_C1.id, chunk_C2.id]

@pytest.mark.asyncio
async def test_generator_stream_predefined(basic_generator_config: MockPipelineConfig, sample_retriever_result: RetrieverResult):
    """Test streaming a predefined answer."""
    _, _, generator = create_mock_rag_pipeline(basic_generator_config)

    query_text = "question about C"
    query_id = sample_retriever_result.query_id
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.VECTOR)
    context = GeneratorContext(query=user_query, retrieved_context=sample_retriever_result)

    streamed_output = []
    async for token in generator.stream_generate(context):
        streamed_output.append(token)

    full_streamed_answer = "".join(streamed_output)
    expected_answer = basic_generator_config.generator_predefined_answers[query_text]

    # Mock stream yields chunks, check if concatenated result matches
    assert full_streamed_answer.replace(" ", "") == expected_answer.replace(" ", "") # Compare ignoring spaces from chunking
    # More robust: check if expected answer contains all streamed parts in order
    reconstructed = ""
    original_answer_words = expected_answer.split()
    stream_idx = 0
    for chunk in streamed_output:
        chunk_words = chunk.strip().split()
        expected_words_chunk = original_answer_words[stream_idx : stream_idx + len(chunk_words)]
        assert chunk_words == expected_words_chunk
        reconstructed += chunk
        stream_idx += len(chunk_words)

    assert reconstructed.strip() == expected_answer

@pytest.mark.asyncio
async def test_generator_stream_default(basic_generator_config: MockPipelineConfig, sample_retriever_result: RetrieverResult):
    """Test streaming a default mock answer."""
    _, _, generator = create_mock_rag_pipeline(basic_generator_config)

    query_text = "another different question"
    query_id = sample_retriever_result.query_id
    user_query = Query(id=query_id, text=query_text, mode=RetrievalMode.VECTOR)
    context = GeneratorContext(query=user_query, retrieved_context=sample_retriever_result)

    # Generate the expected default answer first
    expected_response = await generator.generate(context)
    expected_answer = expected_response.answer

    streamed_output = []
    async for token in generator.stream_generate(context):
        streamed_output.append(token)

    full_streamed_answer = "".join(streamed_output)

    assert full_streamed_answer.replace(" ", "") == expected_answer.replace(" ", "")
    assert full_streamed_answer.strip() == expected_answer # Check exact match after stripping 