from rest_framework.response import Response

from sessions.manager import SessionManager
from sessions.session_model import SessionModel
from core.config import Settings


class SessionService:
    COOKIE_NAME = "origami_session"
    COOKIE_AGE = Settings.SESSION_TIMEOUT * 60  # 24 Hours

    def __init__(self):
        self.session_manager = SessionManager()

    def get_session_id_from_request(self, request) -> str | None:
        session_id = request.COOKIES.get(self.COOKIE_NAME)
        if not session_id:
            session_id = request.headers.get("X-Session-ID") or request.META.get("HTTP_X_SESSION_ID")
        return session_id

    # Upload
    # Create a session if one doesn't already exist
    def get_or_create_session(
        self,
        request,
    ) -> SessionModel:

        session_id = self.get_session_id_from_request(request)

        if session_id:
            try:
                session = self.session_manager.get_session(session_id)

                if self.session_manager.is_expired(
                    session.session_id,
                    timeout_minutes=Settings.SESSION_TIMEOUT,
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

        session_id = self.get_session_id_from_request(request)

        if session_id is None:
            raise FileNotFoundError("No active session.")

        try:
            session = self.session_manager.get_session(session_id)
        except FileNotFoundError as error:
            raise FileNotFoundError("Session expired.") from error

        if self.session_manager.is_expired(
            session.session_id,
            timeout_minutes=Settings.SESSION_TIMEOUT,
        ):
            self.session_manager.delete_session(
                session.session_id,
            )
            session = self.session_manager.create_session()

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
            httponly=False,
            samesite="None",
            secure=True,  # True in production
        )

    # Remove Cookie
    def clear_session(
        self,
        response: Response,
    ) -> None:

        response.delete_cookie(
            self.COOKIE_NAME,
        )
