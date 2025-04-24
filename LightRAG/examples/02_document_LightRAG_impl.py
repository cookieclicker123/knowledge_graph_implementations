import os
import asyncio
import logging
from dotenv import load_dotenv

# --- Determine Paths ---
script_dir = os.path.dirname(__file__)
lightrag_root_dir = os.path.abspath(os.path.join(script_dir, '..'))

# Define the working directory for this specific example
working_dir = os.path.join(lightrag_root_dir, 'tmp', 'lightrag_data', '02_document_example')

# Define path to .env file
dotenv_path = os.path.join(lightrag_root_dir, '.env')

# --- Load Environment Variables ---
load_dotenv(dotenv_path=dotenv_path)

# --- LightRAG Imports ---
from lightrag.lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

# --- Configuration & Logging ---
# Check for API Key
if not os.getenv("OPENAI_API_KEY"):
    print("\nWARNING: OPENAI_API_KEY environment variable not set.")
    print("This example requires an OpenAI API key to function (set in .env or environment).")
    # exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LightRAG_Example_02") # Updated logger name

# --- Define Embedding Function Details ---
EMBEDDING_DIM = 1536
MAX_TOKEN_SIZE = 8191
embedding_details = EmbeddingFunc(
    func=openai_embed,
    embedding_dim=EMBEDDING_DIM,
    max_token_size=MAX_TOKEN_SIZE
)

# Define path to the sample document
sample_doc_path = os.path.join(script_dir, 'sample_doc.txt')


async def main():
    logger.info("Initializing LightRAG for Document Example...")

    # --- Create Working Directory ---
    logger.info(f"Ensuring working directory exists: {working_dir}")
    os.makedirs(working_dir, exist_ok=True)

    # Initialize LightRAG
    rag = LightRAG(
        embedding_func=embedding_details,
        llm_model_func=gpt_4o_mini_complete,
        working_dir=working_dir # Use the new path
    )

    # --- Perform necessary async initialization ---
    logger.info("Initializing LightRAG storage and pipeline status...")
    try:
        await rag.initialize_storages()
        await initialize_pipeline_status()
        logger.info("Storage and pipeline status initialized.")
    except Exception as e:
        logger.error(f"Error during LightRAG initialization: {e}")
        return

    logger.info("LightRAG Initialized and Ready.")

    # --- Read document content ---
    logger.info(f"Reading document content from: {sample_doc_path}")
    document_content = ""
    try:
        # Open the file in read mode with UTF-8 encoding
        with open(sample_doc_path, 'r', encoding='utf-8') as f:
            document_content = f.read()
        logger.info(f"Successfully read {len(document_content)} characters from the document.")
    except FileNotFoundError:
        logger.error(f"Sample document not found at {sample_doc_path}")
        return
    except Exception as e:
        logger.error(f"Error reading document: {e}")
        return

    if not document_content:
        logger.error("Document content is empty.")
        return

    # --- Data Insertion ---
    # Prepare a snippet for logging, replacing newlines
    log_snippet = document_content[:100].replace('\n', ' ')
    logger.info(f"Inserting document content: '{log_snippet}...'")
    try:
        # Use the async version 'ainsert' and await it, passing the document_content
        insert_result = await rag.ainsert(document_content)
        logger.info(f"Insertion result: {insert_result}") # Actual content depends on library version
    except Exception as e:
        logger.error(f"Error during insertion: {e}")
        return

    logger.info("Document content inserted successfully.")

    # --- Querying ---
    query_text = "What are the conceptual processing steps in LightRAG according to the document?"
    logger.info(f"Performing query: '{query_text}'")

    query_params = QueryParam(mode="mix") # Or other modes as needed

    try:
        # Use the async version 'aquery' and await it
        query_response = await rag.aquery(query_text, param=query_params)
        logger.info("Query successful.")
        print("\n----------------------------")
        print(f"Query: {query_text}")
        # Adapt attribute names based on actual response object structure if needed
        response_text = getattr(query_response, 'answer', getattr(query_response, 'response', str(query_response)))
        print(f"Answer: {response_text}")
        context_info = getattr(query_response, 'context_chunks_ids', getattr(query_response, 'context', None))
        if context_info:
            print(f"Context Used: {context_info}")
        # print(f"Full Response Object: {query_response}")
        print("----------------------------\n")

    except Exception as e:
        logger.error(f"Error during query: {e}")
        return

if __name__ == "__main__":
    asyncio.run(main()) # Uncommented
