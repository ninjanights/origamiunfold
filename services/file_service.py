from sessions.session_model import SessionModel


class FileService:

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