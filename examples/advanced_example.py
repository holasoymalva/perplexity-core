"""
Advanced example showing more features of the Perplexity client
"""
import os
import sys
import json
import asyncio
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.perplexity_client import PerplexityClient
from src.utils.config import Config
from src.utils.logger import get_logger

# Configure logging
logger = get_logger(__name__)

async def process_stream(stream_generator):
    """Process a streaming response"""
    full_response = ""
    async for chunk in stream_generator:
        if 'choices' in chunk and len(chunk['choices']) > 0:
            delta = chunk['choices'][0].get('delta', {})
            content = delta.get('content', '')
            if content:
                full_response += content
                print(content, end='', flush=True)
    print()  # Final newline
    return full_response

async def main():
    """
    Run an advanced example using the Perplexity client.
    """
    # Create a configuration
    config = Config()
    
    # Set some custom configuration
    config.set('model', 'sonar-medium-online')
    config.set('temperature', 0.7)
    
    # Save the configuration
    config_path = Path.home() / '.perplexity' / 'config.json'
    os.makedirs(os.path.dirname(str(config_path)), exist_ok=True)
    config.save(str(config_path))
    
    # Get API key from environment variable
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        logger.error("PERPLEXITY_API_KEY environment variable not set")
        return
    
    # Initialize the client with the configuration
    client = PerplexityClient(api_key=api_key, config=config)
    
    # Example 1: Simple question with custom parameters
    print("\n=== Example 1: Custom Parameters ===")
    response = client.query(
        query="What are 5 strategies for implementing responsible AI?",
        model="sonar-small-online",  # Use a smaller model for faster response
        temperature=0.2,  # Lower temperature for more deterministic results
        max_tokens=500  # Limit response length
    )
    
    print(f"Response (using {response.model}, {response.usage.total_tokens} tokens):")
    print(response.content)
    
    # Example 2: Search query with context
    print("\n=== Example 2: Search Functionality ===")
    search_response = client.search(
        query="Latest advancements in quantum computing",
        model="sonar-medium-online"  # Use a more powerful model for search
    )
    
    print(f"Search Response ({search_response.usage.total_tokens} tokens):")
    print(search_response.content)
    
    # Example 3: Streaming response
    print("\n=== Example 3: Streaming Response ===")
    print("Streaming response for query: 'Explain the concept of transfer learning in AI'")
    
    # Note: We're converting the generator to an async generator for demonstration
    stream_gen = client.query(
        query="Explain the concept of transfer learning in AI",
        stream=True
    )
    
    # Process the streaming response
    await process_stream(stream_gen)
    
    # Example 4: Using multiple contexts
    print("\n=== Example 4: Multiple Context Items ===")
    
    # Create context with background information
    context = [
        {
            "type": "text",
            "text": "Large Language Models (LLMs) are AI systems trained on vast amounts of text data."
        },
        {
            "type": "text",
            "text": "Transformers are a type of neural network architecture that uses self-attention mechanisms."
        },
        {
            "type": "search",
            "search_query": "limitations of large language models"
        }
    ]
    
    response = client.query(
        query="What are the key limitations of current Large Language Models and how might they be addressed?",
        context=context
    )
    
    print(f"Response with multiple context items ({response.usage.total_tokens} tokens):")
    print(response.content)

if __name__ == "__main__":
    asyncio.run(main())