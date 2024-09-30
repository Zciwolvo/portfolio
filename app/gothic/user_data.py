import json
import os

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, user_data):
        return cls(
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role']
        )

    def save_to_json(self):
        user_file_path = os.path.join('/home/IgorGawlowicz/mysite/users', f'{self.username}.json')
        with open(user_file_path, 'w') as file:
            json.dump(self.to_dict(), file)

    @classmethod
    def load_from_json(cls, username):
        user_file_path = os.path.join('/home/IgorGawlowicz/mysite/users', f'{username}.json')
        if os.path.exists(user_file_path):
            with open(user_file_path, 'r') as file:
                user_data = json.load(file)
                return cls.from_dict(user_data)
        return None
