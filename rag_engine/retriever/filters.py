from dataclasses import dataclass

@dataclass(slots=True)
class SearchFilters:
    sources: list[str] | None = None
    file_type: str | None = None
    page_number : int | None = None
    session_id: str | None = None