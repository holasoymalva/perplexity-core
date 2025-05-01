"""
Response models for the Perplexity API
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PerplexityMessage:
    """Represents a single message in a Perplexity conversation"""
    role: str
    content: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerplexityMessage':
        """Create a PerplexityMessage from a dictionary"""
        return cls(
            role=data.get('role', ''),
            content=data.get('content', '')
        )

@dataclass
class PerplexityUsage:
    """Usage statistics for a Perplexity API response"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerplexityUsage':
        """Create a PerplexityUsage from a dictionary"""
        return cls(
            prompt_tokens=data.get('prompt_tokens', 0),
            completion_tokens=data.get('completion_tokens', 0),
            total_tokens=data.get('total_tokens', 0)
        )

@dataclass
class PerplexityChoice:
    """A single choice/completion from the Perplexity API"""
    index: int
    message: PerplexityMessage
    finish_reason: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerplexityChoice':
        """Create a PerplexityChoice from a dictionary"""
        return cls(
            index=data.get('index', 0),
            message=PerplexityMessage.from_dict(data.get('message', {})),
            finish_reason=data.get('finish_reason', '')
        )

@dataclass
class PerplexityResponse:
    """Complete response from a Perplexity API request"""
    id: str
    object: str
    created: datetime
    model: str
    choices: List[PerplexityChoice]
    usage: PerplexityUsage
    system_fingerprint: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    
    @property
    def content(self) -> str:
        """Get the content of the first choice's message"""
        if not self.choices:
            return ""
        return self.choices[0].message.content
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerplexityResponse':
        """Create a PerplexityResponse from a dictionary"""
        return cls(
            id=data.get('id', ''),
            object=data.get('object', ''),
            created=datetime.fromtimestamp(data.get('created', 0)),
            model=data.get('model', ''),
            choices=[PerplexityChoice.from_dict(choice) for choice in data.get('choices', [])],
            usage=PerplexityUsage.from_dict(data.get('usage', {})),
            system_fingerprint=data.get('system_fingerprint'),
            raw_response=data
        )