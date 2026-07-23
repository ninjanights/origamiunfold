from apscheduler.schedulers.background import BackgroundScheduler
from sessions.manager import SessionManager
from core.config import Settings
import atexit

scheduler = BackgroundScheduler()
manager = SessionManager()

_started = False


def start_scheduler():
    global _started

    if _started:
        return

    _started = True

    scheduler.add_job(
        manager.cleanup_expired_session,
        trigger="interval",
        minutes=Settings.SESSION_CLEANUP_INTERVAL,
        id="cleanup_session",
        replace_existing=True,
    )
    scheduler.start()


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)

atexit.register(shutdown_scheduler)