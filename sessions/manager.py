from pathlib import Path
import shutil
import uuid
from core.logger import logger
import json
from datetime import (
    datetime,
    timedelta,
)


class SessionManager:
    def __init__(self):
        self.base_path = Path("./backend/sessions/workspaces")
        self.base_path.mkdir(parents=True, exist_ok=True)

    # assign a new identity
    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        workspace = self.base_path / session_id
        (workspace / "uploads").mkdir(parents=True)
        (workspace / "chroma").mkdir(parents=True)

        logger.info(f"Created session: {session_id}")
        return session_id

    # find the identity with session id
    def get_workspace(
        self,
        session_id: str,
    ) -> Path:
        workspace = self.base_path / session_id

        if not workspace.exists():
            logger.error(f"Session not found: {session_id}")
            raise FileNotFoundError(f"Session {session_id} does not exist.")

        return workspace

    # recursively delete folders of the identity after inactivity
    def delete_session(
        self,
        session_id: str,
    ) -> None:
        workspace = self.get_workspace(session_id)
        shutil.rmtree(workspace)
        logger.info(f"Deleted session: {session_id}")

    # touch / redeclear time cause identity has interacted
    def touch_session(
        self,
        session_id: str,
    ) -> None:
        workspace = self.get_workspace(session_id)
        metadata = workspace / "metadata.json"
        data = {
            "session_id": session_id,
            "last_access": datetime.now().isoformat(),
        }
        metadata.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8",
        )
        logger.info(f"Updated session: {session_id}")

    # check last_access and sees it has expired in time, so backend can delete the instance
    def expired(
        self,
        session_id: str,
        timeout_minutes: int = 30,
    ) -> bool:
        workspace = self.get_workspace(session_id)
        metadata = workspace / "metadata.json"
        data = json.loads(
            metadata.read_text(
                encoding="utf-8",
            )
        )
        last_access = datetime.fromisoformat(data["last_access"])
        now = datetime.now()
        return now - last_access > timedelta(minutes=timeout_minutes)
