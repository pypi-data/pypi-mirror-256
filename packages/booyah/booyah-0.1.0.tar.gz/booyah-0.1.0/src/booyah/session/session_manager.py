from booyah.session.storages.database_storage import DatabaseStorage
from booyah.cookies.cookies_manager import cookies_manager
from booyah.session.flash_message import FlashMessage

class SessionManager:
    def __init__(self, storage=None):
        if not storage:
            self.storage = DatabaseStorage()
        else:
            self.storage = storage

    def get_session(self, session_id, key):
        return self.storage.get_session_dict(session_id, key)

    def delete_session(self, session_id):
        self.storage.destroy_session(session_id)

    def save_session(self):
        session_id = cookies_manager.get_cookie('sessionid')
        session_key = cookies_manager.get_cookie('sessionkey')
        expiration = cookies_manager.expiration_date('sessionid')
        self.storage.save_session(session_id, session_key, self.session, expiration)
    
    def clear_expired(self):
        self.storage.clear_expired()
    
    def from_cookie(self):
        self.session = self.get_session(cookies_manager.get_cookie('sessionid'), cookies_manager.get_cookie('sessionkey'))
        if not '_flash' in self.session:
            self.session['_flash'] = {}
        self.flash_messages = FlashMessage(self.session['_flash'])
        self.flash_messages.set_session_manager(self)
        return self.session

session_manager = SessionManager()