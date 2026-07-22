from pathlib import Path
from sessions.manager import SessionManager
from sessions.session_model import SessionModel

from services.indexing_service import IndexingService


class UploadService:

    @property
    def indexing_service(self):
        if not hasattr(self, "_indexing_service"):
            self._indexing_service = IndexingService()
        return self._indexing_service

    def upload(self, uploaded_file, session: SessionModel):
        # save in file path
        destination = session.workspace / "uploads" / uploaded_file.name

        # inbuilt django chunks so a huge file gets broken into parts
        with open(destination, "wb") as file:
            if hasattr(uploaded_file, "chunks"):
                for chunk in uploaded_file.chunks():
                    file.write(chunk)
                else:
                    file.write(uploaded_file.read())

        # 4. Store in Chroma
        self.indexing_service.index(
            destination,
            session,
        )

        return session
