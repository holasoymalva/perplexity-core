"""
Tests for the PerplexityClient class
"""
import pytest
import json
import os
from unittest.mock import patch, MagicMock

from src.perplexity_client import PerplexityClient
from src.models.response_models import PerplexityResponse

# Sample API response data for testing
SAMPLE_RESPONSE_DATA = {
    "id": "chatcmpl-123456789",
    "object": "chat.completion",
    "created": 1677825464,
    "model": "sonar-medium-online",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "This is a test response from the Perplexity API."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 12,
        "completion_tokens": 10,
        "total_tokens": 22
    },
    "system_fingerprint": "fp123456"
}

class TestPerplexityClient:
    """Tests for the PerplexityClient class"""
    
    @pytest.fixture
    def client(self):
        """Return a client with a mock API key"""
        with patch.dict(os.environ, {"PERPLEXITY_API_KEY": "fake-api-key-for-testing"}):
            return PerplexityClient()
    
    def test_init_with_api_key(self):
        """Test initialization with explicit API key"""
        client = PerplexityClient(api_key="test-api-key")
        assert client.api_key == "test-api-key"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer test-api-key"
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                PerplexityClient()
    
    @patch("requests.post")
    def test_query(self, mock_post, client):
        """Test the query method with a mock response"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_RESPONSE_DATA
        mock_post.return_value = mock_response
        
        # Call the query method
        response = client.query("Test query")
        
        # Assertions
        assert isinstance(response, PerplexityResponse)
        assert response.id == SAMPLE_RESPONSE_DATA["id"]
        assert response.model == SAMPLE_RESPONSE_DATA["model"]
        assert response.content == "This is a test response from the Perplexity API."
        assert response.usage.total_tokens == 22
        
        # Check that the request was called with the right parameters
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]["headers"]["Authorization"] == "Bearer fake-api-key-for-testing"
        
        # Check payload
        payload = json.loads(call_args[1]["json"]["messages"][0]["content"])
        assert payload == "Test query"
    
    @patch("requests.post")
    def test_search(self, mock_post, client):
        """Test the search method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_RESPONSE_DATA
        mock_post.return_value = mock_response
        
        # Call the search method
        response = client.search("Test search query")
        
        # Assertions
        assert isinstance(response, PerplexityResponse)
        
        # Check that the request was called with context that includes the search
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        
        assert "context" in payload
        assert len(payload["context"]) > 0
        assert payload["context"][0]["type"] == "search"
        assert payload["context"][0]["search_query"] == "Test search query"