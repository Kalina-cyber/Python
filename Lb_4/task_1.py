import hashlib
from datetime import datetime

import hashlib
from datetime import datetime

# Базовий клас користувача
class User:
    def __init__(self, username: str, password: str, is_active: bool = True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)

    def __str__(self):
        return f"User(username={self.username}, active={self.is_active})"

# Адміністратор
class Administrator(User):
    def __init__(self, username: str, password: str, permissions=None, is_active: bool = True):
        super().__init__(username, password, is_active)
        self.permissions = permissions if permissions else []

    def add_permission(self, permission: str):
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission: str):
        if permission in self.permissions:
            self.permissions.remove(permission)

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    def __str__(self):
        return f"Administrator(username={self.username}, permissions={self.permissions})"

# Звичайний користувач
class RegularUser(User):
    def __init__(self, username: str, password: str, is_active: bool = True):
        super().__init__(username, password, is_active)
        self.last_login = None

    def login(self, password: str) -> bool:
        if self.verify_password(password) and self.is_active:
            self.last_login = datetime.now()
            return True
        return False

    def __str__(self):
        login_time = self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else 'Never'
        return f"RegularUser(username={self.username}, last_login={login_time})"

# Гість
class GuestUser(User):
    def __init__(self, username: str = "guest", is_active: bool = True):
        super().__init__(username, password="", is_active=is_active)
        self.access_level = "read-only"

    def verify_password(self, password: str) -> bool:
        return False  # гість не проходить автентифікацію за паролем

    def has_access(self, feature: str) -> bool:
        allowed_features = ["view_content", "read_news"]
        return feature in allowed_features

    def __str__(self):
        return f"GuestUser(username={self.username}, access_level={self.access_level})"

# Система контролю доступу
class AccessControl:
    def __init__(self):
        self.users = {}  # ключ: username, значення: об'єкт User

    def add_user(self, user: User):
        if user.username in self.users:
            print(f"Користувач '{user.username}' вже існує.")
        else:
            self.users[user.username] = user
            print(f"Користувач '{user.username}' доданий до системи.")

    def authenticate_user(self, username: str, password: str):
        user = self.users.get(username)
        if user and user.verify_password(password):
            if user.is_active:
                print(f"Аутентифікація успішна для '{username}'")
                return user
            else:
                print(f"Користувач '{username}' неактивний.")
        else:
            print(f"Аутентифікація не вдалася для '{username}'")
        return None

# Приклад використання
if __name__ == "__main__":
    # Створення користувачів
    admin = Administrator("admin", "adminpass", permissions=["create_user", "delete_user"])
    user = RegularUser("karina", "secure123")
    guest = GuestUser()

    # Система доступу
    ac = AccessControl()
    ac.add_user(admin)
    ac.add_user(user)
    ac.add_user(guest)

    # Аутентифікація
    ac.authenticate_user("karina", "secure123")  # Успішно
    ac.authenticate_user("admin", "wrongpass")  # Невдача
    ac.authenticate_user("guest", "")  # Невдача, гість не аутентифікується

