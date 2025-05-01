"""
Perplexity API Client - Core module for interacting with Perplexity's API
"""
import json
import requests
from typing import Dict, Any, Optional, List, Union

from .utils.config import Config
from .utils.logger import get_logger
from .models.response_models import PerplexityResponse
from .handlers.response_handler import ResponseHandler

logger = get_logger(__name__)

class PerplexityClient:
    """
    A client for interacting with the Perplexity API.
    """
    
    BASE_URL = "https://api.perplexity.ai"
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Config] = None):
        """
        Initialize the Perplexity API client.
        
        Args:
            api_key: Perplexity API key. If not provided, it will try to read from config or environment variables.
            config: Configuration object. If not provided, a default configuration will be used.
        """
        self.config = config or Config()
        self.api_key = api_key or self.config.get_api_key()
        
        if not self.api_key:
            raise ValueError("API key must be provided either directly or through the config.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.response_handler = ResponseHandler()
        
        logger.info("Perplexity client initialized")
    
    def query(self, 
              query: str, 
              model: str = "sonar-medium-online", 
              temperature: float = 0.7,
              max_tokens: int = 1024,
              context: Optional[List[Dict[str, str]]] = None,
              stream: bool = False) -> Union[PerplexityResponse, Dict[str, Any]]:
        """
        Send a query to the Perplexity API.
        
        Args:
            query: The question or prompt to send to the model
            model: The model to use for the query (default: sonar-medium-online)
            temperature: Controls randomness of the output (0.0-1.0)
            max_tokens: Maximum number of tokens to generate
            context: Optional list of context items to provide the model
            stream: Whether to stream the response or not
            
        Returns:
            A PerplexityResponse object or raw API response
        """
        endpoint = f"{self.BASE_URL}/chat/completions"
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": query}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        if context:
            payload["context"] = context
            
        logger.debug(f"Sending request to Perplexity API: {json.dumps(payload, indent=2)}")
        
        try:
            if stream:
                return self._handle_stream_response(endpoint, payload)
            else:
                return self._handle_standard_response(endpoint, payload)
        except Exception as e:
            logger.error(f"Error querying Perplexity API: {str(e)}")
            raise
    
    def _handle_standard_response(self, endpoint: str, payload: Dict[str, Any]) -> PerplexityResponse:
        """Handle a standard (non-streaming) response from the API"""
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"Received response from Perplexity API: {json.dumps(result, indent=2)}")
        
        return self.response_handler.process_response(result)
    
    def _handle_stream_response(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a streaming response from the API"""
        with requests.post(endpoint, headers=self.headers, json=payload, stream=True) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    if line.strip() == b"data: [DONE]":
                        break
                    
                    if line.startswith(b"data: "):
                        json_str = line[6:].decode('utf-8')
                        try:
                            chunk = json.loads(json_str)
                            yield chunk
                        except json.JSONDecodeError as e:
                            logger.error(f"Error decoding JSON from stream: {str(e)}")
                            
    def search(self, query: str, **kwargs) -> PerplexityResponse:
        """
        Perform a web search query through Perplexity API.
        This is a convenience method that adds search-specific parameters.
        
        Args:
            query: The search query
            **kwargs: Additional parameters to pass to the query method
            
        Returns:
            A PerplexityResponse object
        """
        context = kwargs.pop('context', [])
        context.append({"type": "search", "search_query": query})
        
        return self.query(
            query=f"Please provide information about: {query}",
            context=context,
            **kwargs
        )