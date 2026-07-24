from pathlib import Path
from sessions.manager import SessionManager
from sessions.session_model import SessionModel

from services.indexing_service import IndexingService
from backend.realtime.progress_reporter import ProgressReporter


class UploadService:

    @property
    def indexing_service(self):
        if not hasattr(self, "_indexing_service"):
            self._indexing_service = IndexingService()
        return self._indexing_service

    def upload(self, uploaded_file, session: SessionModel):
        progress = ProgressReporter(session.session_id)
        progress.upload(
            "received",
            f"Received {uploaded_file.name}",
            5,
            preview="File 2. 'abc abc   def  #'",
            after="File 2. 'abc abc   def  #'",
        )
        
        
        
        
        # save in file path
        destination = session.workspace / "uploads" / uploaded_file.name
        progress.upload(
            "saving",
            "Saving uploaded file...",
            10,
            preview="File 2. 'abc abc   def  #'",
            after="File 2. 'abc abc   def  #'",
        )

        
        
        
        
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
