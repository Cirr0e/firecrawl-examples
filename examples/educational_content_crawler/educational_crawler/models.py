from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ContentChunk(BaseModel):
    """A semantic chunk of educational content"""
    text: str
    type: str = Field(description="Type of chunk (definition, example, explanation, etc.)")
    importance: float = Field(description="Importance score 0-1")

class ContentMetadata(BaseModel):
    """Metadata for educational content"""
    subject: str
    grade_level: str
    learning_objectives: List[str]
    prerequisites: List[str]
    license: Optional[str]

class ValidationResult(BaseModel):
    """Result of content validation"""
    is_valid: bool
    score: float
    issues: List[str] = []
    improvements: List[str] = []

class EducationalContent(BaseModel):
    """Educational content with metadata and validation"""
    title: str
    content: str
    chunks: List[ContentChunk]
    metadata: Optional[ContentMetadata] = None
    validation_result: Optional[ValidationResult] = None
    raw_data: Dict[str, Any]