from apscheduler.schedulers.background import BackgroundScheduler
from sessions.manager import SessionManager
import atexit

scheduler = BackgroundScheduler()

manager = SessionManager()
from core.config import Settings


def start_scheduler():

    scheduler.add_job(
        manager.cleanup_expired_session,
        trigger="interval",
        minutes=Settings.SESSION_CLEANUP_INTERVAL,
        id="cleanup_session",
        replace_existing=True,
    )
    scheduler.start()


atexit.register(lambda: scheduler.shutdown())
