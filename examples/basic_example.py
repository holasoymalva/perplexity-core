"""
Basic example showing how to use the Perplexity client
"""
import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.perplexity_client import PerplexityClient
from src.utils.logger import get_logger

# Configure logging
logger = get_logger(__name__, logging.INFO)

def main():
    """
    Run a basic example using the Perplexity client.
    """
    # Get API key from environment variable
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        logger.error("PERPLEXITY_API_KEY environment variable not set")
        return
    
    # Initialize the client
    client = PerplexityClient(api_key=api_key)
    
    # Simple query example
    query = "What are the main applications of artificial intelligence in healthcare?"
    
    logger.info(f"Sending query: {query}")
    response = client.query(query)
    
    # Print the results
    print("\n" + "="*50)
    print("QUERY RESULTS")
    print("="*50)
    print(f"Query: {query}")
    print(f"Model: {response.model}")
    print(f"Response ID: {response.id}")
    print("="*50)
    print("\nResponse content:")
    print(response.content)
    print("\n" + "="*50)
    print(f"Token usage: {response.usage.total_tokens} total tokens")
    print(f"  - Prompt tokens: {response.usage.prompt_tokens}")
    print(f"  - Completion tokens: {response.usage.completion_tokens}")
    
    # Example of extracting citations if available
    from src.handlers.response_handler import ResponseHandler
    handler = ResponseHandler()
    citations = handler.extract_citations(response)
    
    if citations:
        print("\nCitations:")
        for i, citation in enumerate(citations, 1):
            print(f"{i}. {citation}")

if __name__ == "__main__":
    main()