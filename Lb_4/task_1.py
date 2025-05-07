import hashlib
from datetime import datetime


# Базовий клас User
class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == self._hash_password(password)


# Підклас Administrator
class Administrator(User):
    def __init__(self, username, password, permissions=None, is_active=True):
        super().__init__(username, password, is_active)
        self.permissions = permissions if permissions is not None else []

    def add_permission(self, permission):
        if permission not in self.permissions:
            self.permissions.append(permission)


# Підклас RegularUser
class RegularUser(User):
    def __init__(self, username, password, last_login=None, is_active=True):
        super().__init__(username, password, is_active)
        self.last_login = last_login

    def update_login_time(self):
        self.last_login = datetime.now()


# Підклас GuestUser
class GuestUser(User):
    def __init__(self, username, password="guest", is_active=True):
        super().__init__(username, password, is_active)
        self.restricted = True


# Клас AccessControl
class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        if user.username not in self.users:
            self.users[user.username] = user

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.is_active and user.verify_password(password):
            if isinstance(user, RegularUser):
                user.update_login_time()
            return user
        return None


# Приклад використання
if __name__ == "__main__":
    ac = AccessControl()

    admin = Administrator("admin", "admin123", permissions=["manage_users", "edit_settings"])
    user = RegularUser("john_doe", "userpass")
    guest = GuestUser("guest")

    ac.add_user(admin)
    ac.add_user(user)
    ac.add_user(guest)

    # Аутентифікація
    u = ac.authenticate_user("john_doe", "userpass")
    if u:
        print(f"Successful log in: {u.username}")
        if isinstance(u, RegularUser):
            print(f"Last log in: {u.last_login}")
    else:
        print("Unsuccessful log in")
