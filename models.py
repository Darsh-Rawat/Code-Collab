from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, country, password_hash=None):
        self.id = id
        self.username = username
        self.email = email
        self.country = country
        self.password_hash = password_hash
    
    def set_password_hash(self, password_hash):
        self.password_hash = password_hash

class Room:
    def __init__(self, id, name, owner_id, password_hash=None):
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.password_hash = password_hash
        self.active_users = []

class Message:
    def __init__(self, id, room_id, user_id, content, timestamp):
        self.id = id
        self.room_id = room_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp

class CodeSnippet:
    def __init__(self, room_id, code, language, last_updated_by, last_updated_at):
        self.room_id = room_id
        self.code = code
        self.language = language
        self.last_updated_by = last_updated_by
        self.last_updated_at = last_updated_at
