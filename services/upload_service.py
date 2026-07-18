from pathlib import Path
from sessions.manager import SessionManager
from sessions.session_model import SessionModel


class UploadService:
    def __init__(self):
        self.session_manager = SessionManager()

    def upload(self, uploaded_file) -> SessionModel:
        session = self.session_manager.create_session()
        destination = session.workspace / "uploads" / uploaded_file.name
        with open(destination, "wb") as file:
            for chunk in uploaded_file.chunks():
                file.write(chunk)
        return session
