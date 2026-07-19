from rest_framework.response import Response

from sessions.manager import SessionManager
from sessions.session_model import SessionModel


class SessionService:

    COOKIE_NAME = "origami_session"
    COOKIE_AGE = 60 * 60 * 24  # 24 Hours

    def __init__(self):
        self.session_manager = SessionManager()

    # Upload
    # Create a session if one doesn't already exist
    def get_or_create_session(
        self,
        request,
    ) -> SessionModel:

        session_id = request.COOKIES.get(self.COOKIE_NAME)

        if session_id:
            try:
                session = self.session_manager.get_session(session_id)

                if self.session_manager.is_expired(
                    session.session_id,
                    timeout_minutes=60 * 24,
                ):
                    self.session_manager.delete_session(
                        session.session_id,
                    )
                    session = self.session_manager.create_session()

            except FileNotFoundError:
                session = self.session_manager.create_session()

        else:
            session = self.session_manager.create_session()

        return session

    # Chat
    # Must already have a valid session
    def get_active_session(
        self,
        request,
    ) -> SessionModel:

        session_id = request.COOKIES.get(self.COOKIE_NAME)

        if session_id is None:
            raise FileNotFoundError("No active session.")

        session = self.session_manager.get_session(session_id)

        if self.session_manager.is_expired(
            session.session_id,
            timeout_minutes=60 * 24,
        ):
            self.session_manager.delete_session(
                session.session_id,
            )
            raise FileNotFoundError("Session expired.")

        return session

    # Refresh Cookie + Update last_access
    def refresh_session(
        self,
        response: Response,
        session: SessionModel,
    ) -> None:

        self.session_manager.touch_session(
            session.session_id,
        )

        response.set_cookie(
            key=self.COOKIE_NAME,
            value=session.session_id,
            max_age=self.COOKIE_AGE,
            httponly=True,
            samesite="Lax",
            secure=False,  # True in production
        )

    # Remove Cookie
    def clear_session(
        self,
        response: Response,
    ) -> None:

        response.delete_cookie(
            self.COOKIE_NAME,
        )
