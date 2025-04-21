import os
import asyncio
import logging
from dotenv import load_dotenv

# --- Determine Paths ---
# Get the directory where this script is located
script_dir = os.path.dirname(__file__)
# Go up one level to get the root of the LightRAG package
lightrag_root_dir = os.path.abspath(os.path.join(script_dir, '..'))
# Define the working directory inside a 'tmp' folder within the LightRAG root
working_dir = os.path.join(lightrag_root_dir, 'tmp', 'lightrag_data', '01_simple_example')
# Define path to .env file, also relative to the LightRAG root
dotenv_path = os.path.join(lightrag_root_dir, '.env')

# --- Load Environment Variables ---
load_dotenv(dotenv_path=dotenv_path)

# --- LightRAG Imports ---
# Using lightrag_hku based on previous install
from lightrag.lightrag import LightRAG, QueryParam
# Import the helper functions directly
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete
from lightrag.utils import EmbeddingFunc # Wrapper for embedding function details
# Correct import path for initialize_pipeline_status
from lightrag.kg.shared_storage import initialize_pipeline_status

# --- Configuration ---
# For this simple example, we rely on LightRAG's defaults which often use
# simple in-memory storage (JSON files, NetworkX graphs, NanoVectorDB).
# The library requires functions for embedding and LLM completion.
# We'll use the provided OpenAI helpers, which require an API key.

# IMPORTANT: Set your OpenAI API key as an environment variable OR in the .env file
# export OPENAI_API_KEY="your-key-here"
if not os.getenv("OPENAI_API_KEY"):
    print("\nWARNING: OPENAI_API_KEY environment variable not set.")
    print("This example requires an OpenAI API key to function (set in .env or environment).")
    # You could exit here, or let it potentially fail later
    # exit(1)

# Configure logging for LightRAG (optional, but helpful)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LightRAG_Example")

# --- Define Embedding Function Details ---
# LightRAG often expects embedding dimension and token size info.
# We wrap the openai_embed function using EmbeddingFunc.
# Get dimension from the model name (e.g., text-embedding-ada-002 is 1536)
# You might need to adjust this based on the default model used by openai_embed
# or explicitly pass a model name to openai_embed if the helper supports it.
# For now, using a common default dimension.
# A more robust way would be to call the embedding func once to get the dim.
EMBEDDING_DIM = 1536 # Common dimension for text-embedding-ada-002
MAX_TOKEN_SIZE = 8191 # Common limit for ada-002

embedding_details = EmbeddingFunc(
    func=openai_embed, # Pass the function itself
    embedding_dim=EMBEDDING_DIM,
    max_token_size=MAX_TOKEN_SIZE
)

async def main():
    logger.info("Initializing LightRAG...")

    # --- Create Working Directory ---
    logger.info(f"Ensuring working directory exists: {working_dir}")
    os.makedirs(working_dir, exist_ok=True) # Create if it doesn't exist

    # Initialize LightRAG with embedding and LLM functions
    rag = LightRAG(
        embedding_func=embedding_details, # Pass the wrapped function details
        llm_model_func=gpt_4o_mini_complete, # Pass the completion function
        working_dir=working_dir # Use the calculated path
    )

    # --- Perform necessary async initialization --- 
    logger.info("Initializing LightRAG storage and pipeline status...")
    try:
        await rag.initialize_storages() # Ensure storage components are ready
        await initialize_pipeline_status() # Initialize pipeline status tracking
        logger.info("Storage and pipeline status initialized.")
    except Exception as e:
        logger.error(f"Error during LightRAG initialization: {e}")
        return

    logger.info("LightRAG Initialized and Ready.")

    # --- Data Insertion ---
    sample_text = ( "LightRAG is a framework for Retrieval-Augmented Generation. "
                    "It helps build systems that answer questions using external knowledge. "
                    "The core components are typically a retriever and a generator." )

    logger.info(f"Inserting text: '{sample_text[:50]}...'" )
    try:
        # Use the async version 'ainsert' and await it
        insert_result = await rag.ainsert(sample_text)
        logger.info(f"Insertion result: {insert_result}") # Actual content depends on library version
    except Exception as e:
        logger.error(f"Error during insertion: {e}")
        logger.error("Ensure your embedding model (OpenAI) is configured correctly (API Key?).")
        return

    logger.info("Text inserted successfully.")

    # --- Querying --- 
    query_text = "What are the core components of LightRAG?"
    logger.info(f"Performing query: '{query_text}'")

    query_params = QueryParam(mode="mix")

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
        logger.error("Ensure your LLM (OpenAI) is configured correctly (API Key?).")
        return

if __name__ == "__main__":
    asyncio.run(main()) 