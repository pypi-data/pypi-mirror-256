class BaseSessionStorage:
    def get_session_dict(self, session_id, key):
        raise NotImplementedError("Subclasses must implement get_session_dict.")
    
    def destroy_session(self, session_id):
        raise NotImplementedError("Subclasses must implement session_id.")

    def save_session(self, session_id, key, data, expiration):
        raise NotImplementedError("Subclasses must implement save_session.")
    
    def create_storage(self):
        raise NotImplementedError("Subclasses must implement create_storage.")
    
    def clear_expired(self):
        raise NotImplementedError("Subclasses must implement clear_expired.")