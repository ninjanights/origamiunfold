from dataclasses import dataclass, field
from typing import Any

@dataclass
class Document:
    """
    Standard document object used throughout the RAG pipeline.
    Every loader should return one or more Document objects.
    """

    content: str
    source: str
    file_type: str
    page_number: int | None = None
    
    metadata: dict[str, Any] = field(default_factory=dict)