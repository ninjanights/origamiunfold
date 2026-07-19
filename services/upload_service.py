from pathlib import Path
from sessions.manager import SessionManager
from sessions.session_model import SessionModel

from services.indexing_service import IndexingService


class UploadService:
    def __init__(self):
        self.indexing_service = IndexingService()

    def upload(self, uploaded_file, session: SessionModel):
        # save in file path
        destination = session.workspace / "uploads" / uploaded_file.name

        # inbuilt django chunks so a huge file gets broken into parts
        with open(destination, "wb") as file:
            for chunk in uploaded_file.chunks():
                file.write(chunk)

        # 4. Store in Chroma
        self.indexing_service.index(
            destination,
            session,
        )

        return session
