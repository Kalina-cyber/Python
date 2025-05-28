# Завдання: Управління обліковими записами з різними рівнями доступу
# Спроектуйте класи для управління обліковими записами користувачів з різними рівнями доступу до системи.
# Створіть базовий клас User (Користувач) з атрибутами:
# username (ім'я користувача)
# password_hash (хеш пароля)
# is_active (булеве значення, що вказує, чи активований обліковий запис).
# Метод verify_password(password), який приймає пароль та порівнює його з password_hash.
# Створіть підкласи, що представляють різні ролі користувачів, наприклад:
# Administrator (Адміністратор), який успадковує від User та може мати додаткові атрибути або методи, пов'язані з адмініструванням системи (наприклад, список дозволів).
# RegularUser (Звичайний користувач), який також успадковує від User та може мати специфічні для звичайних користувачів атрибути (наприклад, остання дата входу).
# GuestUser (Гість), який є підкласом User та може мати обмежені права доступу.
# Створіть клас AccessControl (Контроль доступу) з атрибутами:
# users (словник, де ключами є імена користувачів, а значеннями - об'єкти класів користувачів).
# Метод add_user(user), який додає нового користувача до системи.
# Метод authenticate_user(username, password), який перевіряє, чи існує користувач з таким ім'ям та чи правильний введений пароль. Повертає об'єкт користувача у разі успішної аутентифікації, і None у разі невдачі.

import hashlib
from datetime import datetime

# Базовий клас користувача
class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self._hash_password(password) == self.password_hash

# Адміністратор
class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions if permissions else []

    def add_permission(self, permission):
        if permission not in self.permissions:
            self.permissions.append(permission)

# Звичайний користувач
class RegularUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.last_login = None

    def update_last_login(self):
        self.last_login = datetime.now()

# Гість
class GuestUser(User):
    def __init__(self, username="guest", password="guest"):
        super().__init__(username, password)
        self.is_active = False  # Зазвичай гість має обмежені права

# Система контролю доступу
class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user
        print(f"Додано користувача: {user.username} ({user.__class__.__name__})")

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            if isinstance(user, RegularUser):
                user.update_last_login()
            return user
        return None

# Приклад використання
if __name__ == "__main__":
    ac = AccessControl()

    admin = Administrator("admin", "admin123", permissions=["add_user", "delete_user"])
    user = RegularUser("john", "johnpassword")
    guest = GuestUser("guest", "guest")

    ac.add_user(admin)
    ac.add_user(user)
    ac.add_user(guest)

    # Спроба автентифікації
    for username, password in [("admin", "admin123"), ("john", "johnpassword"), ("guest", "gue_t"), ("gue_t", "guest"), ("guest", "guest"), ("jake", "pass")]:
        authenticated_user = ac.authenticate_user(username, password)
        if authenticated_user:
            print(f"Успішна автентифікація: {authenticated_user.username} ({authenticated_user.__class__.__name__})")
        else:
            print(f"Не вдалося автентифікувати користувача: {username}")
