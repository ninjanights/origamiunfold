from .events import send_progress


class ProgressReporter:
    def __init__(self, session_id):
        self.session_id = session_id

    def upload(
        self,
        stage,
        message,
        progress,
        preview=None,
        after=None,
    ):
        send_progress(
            self.session_id,
            "upload",
            stage,
            message,
            progress,
            preview=preview,
            after=after,
        )

    def chat(self, stage, message, progress, preview=None, after=None):
        send_progress(
            self.session_id,
            "chat",
            stage,
            message,
            progress,
            preview=preview,
            after=after,
        )
