from sessions.manager import SessionManager
class CleanupService:
    def __init__(self):
        self.manager = SessionManager()
        
    def cleanup(self):
        deleted = self.manager.cleanup_expired_session()
        return {
            "deleted" : deleted
        }
        
        
        