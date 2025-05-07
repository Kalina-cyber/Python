import hashlib

# Базовий клас користувача
class User:
    pass

# Адміністратор
class Administrator(User):
    pass

# Звичайний користувач
class RegularUser(User):
    pass

# Гість
class GuestUser(User):
    pass

# Система контролю доступу
class AccessControl:
    pass

# Приклад використання
if __name__ == "__main__":
    print()