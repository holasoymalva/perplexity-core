"""
Handlers for processing Perplexity API responses
"""
from typing import Dict, Any, Optional, List, Union
import json

from ..models.response_models import PerplexityResponse
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ResponseHandler:
    """
    Handler for processing responses from the Perplexity API.
    """
    
    def __init__(self):
        """Initialize the response handler."""
        pass
    
    def process_response(self, data: Dict[str, Any]) -> PerplexityResponse:
        """
        Process a raw response from the Perplexity API and convert it to a PerplexityResponse.
        
        Args:
            data: Raw API response data
            
        Returns:
            A processed PerplexityResponse object
        """
        try:
            response = PerplexityResponse.from_dict(data)
            logger.debug(f"Processed response: ID={response.id}, Model={response.model}")
            return response
        except Exception as e:
            logger.error(f"Error processing API response: {str(e)}")
            logger.debug(f"Raw response data: {json.dumps(data, indent=2)}")
            raise
    
    def extract_text(self, response: PerplexityResponse) -> str:
        """
        Extract the text content from a PerplexityResponse.
        
        Args:
            response: The PerplexityResponse object
            
        Returns:
            The extracted text content
        """
        return response.content
    
    def extract_citations(self, response: PerplexityResponse) -> List[Dict[str, Any]]:
        """
        Extract citations from a PerplexityResponse, if available.
        
        Args:
            response: The PerplexityResponse object
            
        Returns:
            A list of citation objects, or an empty list if none are found
        """
        # This implementation is a placeholder since the exact format of citations
        # in the Perplexity API response would need to be determined from the API docs
        # or experimentation
        
        # Example implementation:
        try:
            raw_response = response.raw_response
            if raw_response and 'citations' in raw_response:
                return raw_response['citations']
            
            # Attempt to parse citations from the content if they're embedded there
            content = response.content
            if content and "[citation:" in content:
                # Simplified citation extraction logic
                # This would need to be enhanced based on the actual citation format
                citations = []
                for line in content.split('\n'):
                    if "[citation:" in line:
                        parts = line.split("[citation:", 1)[1].split("]", 1)
                        if len(parts) > 1:
                            citation_text = parts[0].strip()
                            citations.append({"text": citation_text})
                return citations
                
        except Exception as e:
            logger.warning(f"Error extracting citations: {str(e)}")
        
        return []
    
    def format_markdown(self, response: PerplexityResponse) -> str:
        """
        Format the response content as markdown.
        
        Args:
            response: The PerplexityResponse object
            
        Returns:
            Markdown formatted content
        """
        content = response.content
        
        # If content already appears to be in markdown format, return as is
        if "```" in content or "##" in content or "*" in content:
            return content
            
        # Simple formatting: wrap paragraphs, add heading
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
            elif line.endswith(':') and len(line) < 50:
                # Likely a heading
                formatted_lines.append(f"## {line}")
                formatted_lines.append("")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)