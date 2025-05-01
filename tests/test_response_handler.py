"""
Tests for the ResponseHandler class
"""
import pytest
from datetime import datetime

from src.handlers.response_handler import ResponseHandler
from src.models.response_models import PerplexityResponse, PerplexityChoice, PerplexityMessage, PerplexityUsage

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

# Sample response data with citation
SAMPLE_RESPONSE_WITH_CITATION = {
    "id": "chatcmpl-123456789",
    "object": "chat.completion",
    "created": 1677825464,
    "model": "sonar-medium-online",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "According to recent research [citation: Smith et al., 2023], AI has made significant progress."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 12,
        "completion_tokens": 15,
        "total_tokens": 27
    }
}

class TestResponseHandler:
    """Tests for the ResponseHandler class"""
    
    @pytest.fixture
    def handler(self):
        """Return a response handler instance"""
        return ResponseHandler()
    
    @pytest.fixture
    def sample_response(self):
        """Return a sample PerplexityResponse instance"""
        return PerplexityResponse(
            id="chatcmpl-123456789",
            object="chat.completion",
            created=datetime.fromtimestamp(1677825464),
            model="sonar-medium-online",
            choices=[
                PerplexityChoice(
                    index=0,
                    message=PerplexityMessage(
                        role="assistant",
                        content="This is a test response from the Perplexity API."
                    ),
                    finish_reason="stop"
                )
            ],
            usage=PerplexityUsage(
                prompt_tokens=12,
                completion_tokens=10,
                total_tokens=22
            ),
            system_fingerprint="fp123456",
            raw_response=SAMPLE_RESPONSE_DATA
        )
    
    def test_process_response(self, handler):
        """Test processing a raw API response"""
        response = handler.process_response(SAMPLE_RESPONSE_DATA)
        
        assert isinstance(response, PerplexityResponse)
        assert response.id == "chatcmpl-123456789"
        assert response.model == "sonar-medium-online"
        assert response.created.timestamp() == 1677825464
        assert len(response.choices) == 1
        assert response.choices[0].message.content == "This is a test response from the Perplexity API."
        assert response.usage.total_tokens == 22
    
    def test_extract_text(self, handler, sample_response):
        """Test extracting text from a response"""
        text = handler.extract_text(sample_response)
        assert text == "This is a test response from the Perplexity API."
    
    def test_extract_citations(self, handler):
        """Test extracting citations from a response with embedded citations"""
        # Create a response with embedded citation
        response = PerplexityResponse.from_dict(SAMPLE_RESPONSE_WITH_CITATION)
        
        # Extract citations
        citations = handler.extract_citations(response)
        
        # Check that we extracted the citation
        assert len(citations) > 0
        assert "Smith et al., 2023" in str(citations)
    
    def test_format_markdown(self, handler, sample_response):
        """Test formatting a response as markdown"""
        # Regular text should remain largely unchanged
        markdown = handler.format_markdown(sample_response)
        assert "This is a test response from the Perplexity API." in markdown
        
        # Create a response with potential headings and test formatting
        response = PerplexityResponse.from_dict(SAMPLE_RESPONSE_DATA)
        response.choices[0].message.content = "Introduction:\nThis is a test.\n\nConclusion:\nThis is the end of the test."
        
        markdown = handler.format_markdown(response)
        assert "## Introduction:" in markdown
        assert "## Conclusion:" in markdown