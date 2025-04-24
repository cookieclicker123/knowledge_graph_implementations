# LightRAG/examples/parsing_documents_examples/01_basic_pymupdf_parser.py

import os
import asyncio
import logging
import fitz  # PyMuPDF

# --- Configuration & Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PyMuPDF_Parser")

# Define paths
script_dir = os.path.dirname(__file__)
lightrag_root_dir = os.path.abspath(os.path.join(script_dir, '..', '..')) # Go up two levels
# Assuming fixtures/data exists relative to the root knowledge_graphs directory
# If tests/fixtures is correct, adjust accordingly.
# INPUT_PDF_PATH = os.path.join(lightrag_root_dir, 'tests', 'fixtures', 'light_rag.pdf') # Use this if in tests/fixtures
INPUT_PDF_PATH = os.path.join(lightrag_root_dir, 'tests', 'fixtures', 'light_rag.pdf') # Assumed path
OUTPUT_DIR = os.path.join(lightrag_root_dir, 'tmp', 'pdf_parsing_outputs')
OUTPUT_FILENAME = "01_basic_pymupdf_output.txt"

# --- Core Functions ---

async def parse_pdf_text(pdf_path: str) -> str | None:
    """Parses text content from a PDF file using PyMuPDF."""
    logger.info(f"Attempting to parse PDF: {pdf_path}")
    full_text = []
    try:
        # Note: fitz.open is synchronous, wrapping in async for structure
        doc = fitz.open(pdf_path)
        logger.info(f"Opened PDF with {len(doc)} pages.")
        for page_num, page in enumerate(doc.pages(), start=1):
            try:
                page_text = page.get_text("text") # Extract plain text
                if page_text:
                    full_text.append(page_text)
            except Exception as page_e:
                logger.warning(f"Could not extract text from page {page_num}: {page_e}")
        doc.close()
        logger.info(f"Successfully extracted text from {len(full_text)} pages.")
        return "\n".join(full_text)
    except FileNotFoundError:
        logger.error(f"Input PDF not found at: {pdf_path}")
        return None
    except Exception as e:
        logger.error(f"Failed to open or parse PDF '{pdf_path}': {e}")
        return None

async def save_text_output(text_content: str, output_dir: str, filename: str) -> bool:
    """Saves the extracted text content to a file."""
    output_path = os.path.join(output_dir, filename)
    logger.info(f"Attempting to save output to: {output_path}")
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Note: open/write is synchronous, wrapping in async for structure
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        logger.info(f"Successfully saved output to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save output file '{output_path}': {e}")
        return False

# --- Main Execution --- 

async def main():
    """Main async function to parse PDF and save output."""
    logger.info("Starting PDF parsing process...")
    
    parsed_text = await parse_pdf_text(INPUT_PDF_PATH)
    
    if parsed_text is not None:
        await save_text_output(parsed_text, OUTPUT_DIR, OUTPUT_FILENAME)
    else:
        logger.error("Parsing failed, output not saved.")
        
    logger.info("PDF parsing process finished.")

if __name__ == "__main__":
    asyncio.run(main()) 