from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    id: str
    content: str
    source: str
    file_type: str
    page_number: int | None = None
    chunk_number: int = 0
    session_id: str | None = None
    start_index: int = 0
    end_index: int = 0
    embedding: list[float] | None = None
    score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
