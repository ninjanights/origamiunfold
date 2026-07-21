from sessions.session_model import SessionModel
from rag_engine.vectorstore.chroma_store import ChromaStore
import shutil


class FileService:

    def __init__(self):
        self.vector_store = ChromaStore()

    def list_files(self, session: SessionModel):
        uploads = session.workspace / "uploads"

        files = []

        for file in uploads.iterdir():
            if file.is_file():
                files.append(
                    {
                        "filename": file.name,
                        "size": file.stat().st_size,
                        "extension": file.suffix.lower(),
                    }
                )

        return files

    def delete_files(
        self,
        session: SessionModel,
        filenames: list[str],
    ):
        uploads = session.workspace / "uploads"

        deleted = []
        failed = []

        for filename in filenames:

            self.vector_store.delete_by_source(
                session_id=session.session_id,
                sources=[filename],
            )

            path = uploads / filename
            if path.exists():
                path.unlink()
                deleted.append(filename)
            else:
                failed.append(filename)
        return {
            "deleted": deleted,
            "failed": failed,
        }

    def delete_all(
        self,
        session: SessionModel,
    ) -> None:
        uploads = session.workspace / "uploads"
        # delete every files from workspace
        if uploads.exists():
            shutil.rmtree(uploads)
            uploads.mkdir(parents=True, exist_ok=True)

        # Delete every embedding belonging to this workspace
        self.vector_store.delete_session(
            session.session_id,
        )
