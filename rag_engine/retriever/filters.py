from dataclasses import dataclass

@dataclass(slots=True)
class SearchFilters:
    source: str | None = None
    file_type: str | None = None
    page_number : int | None = None