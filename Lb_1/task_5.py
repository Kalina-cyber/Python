#Аутентифікація користувачів
import hashlib

# Словник користувачів: ключ - логін, значення - (захешований пароль, ПІБ)
users = {
    "user1": (hashlib.md5("password123".encode()).hexdigest(), "Іваненко Іван Іванович"),
    "user2": (hashlib.md5("securepass".encode()).hexdigest(), "Петренко Петро Петрович"),
    "user3": (hashlib.md5("qwerty".encode()).hexdigest(), "Сидоренко Сергій Олександрович")
}

# Функція перевірки пароля
def authenticate_user(login, password):
    if login in users:
        hashed_input_password = hashlib.md5(password.encode()).hexdigest()
        stored_password, full_name = users[login]

        if hashed_input_password == stored_password:
            print(f"Аутентифікація успішна! Ласкаво просимо, {full_name}!")
        else:
            print("Невірний пароль!")
    else:
        print("Користувача не знайдено!")


# Введення логіна та пароля
login = input("Введіть логін: ")
password = input("Введіть пароль: ")

# Перевірка аутентифікації
authenticate_user(login, password)