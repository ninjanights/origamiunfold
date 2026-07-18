from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass
class SessionModel:
    session_id: str
    workspace: Path
    created_at: datetime
    last_access: datetime