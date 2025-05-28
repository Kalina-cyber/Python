import sqlite3
import hashlib

# Підключення до БД
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Створення таблиці, якщо ще не створена
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    login TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL
)
''')
conn.commit()

# Функція хешування пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Додавання нового користувача
def add_user():
    login = input("Введіть логін: ")
    full_name = input("Введіть ПІБ: ")
    password = input("Введіть пароль: ")
    hashed = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
                       (login, hashed, full_name))
        conn.commit()
        print("Користувача додано.")
    except sqlite3.IntegrityError:
        print("Користувач з таким логіном вже існує.")

# Оновлення пароля
def update_password():
    login = input("Введіть логін: ")
    new_password = input("Введіть пароль: ")
    hashed = hash_password(new_password)

    cursor.execute("UPDATE users SET password = ? WHERE login = ?", (hashed, login))
    if cursor.rowcount == 0:
        print("Користувача не знайдено.")
    else:
        conn.commit()
        print("Пароль оновлено.")

# Аутентифікація
def authenticate():
    login = input("Введіть логін: ")
    password = input("Введіть пароль: ")
    hashed = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, hashed))
    user = cursor.fetchone()
    if user:
        print(f"Аутентифікація успішна. Ласкаво просимо, {user[2]}!")
    else:
        print("Невірний логін або пароль.")

# Функція для перегляду усіх користувачів
def show_all_users():
    cursor.execute("SELECT login, full_name FROM users")
    users = cursor.fetchall()
    if users:
        print("\nСписок користувачів:")
        for login, full_name in users:
            print(f"Логін: {login}, ПІБ: {full_name}")
    else:
        print("Користувачів немає.")

# Функція для видалення користувача
def delete_user():
    login = input("Введіть логін: ")
    password = input("Введіть пароль: ")
    hashed = hash_password(password)

    cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
    row = cursor.fetchone()
    if row is None:
        print("Користувача не знайдено.")
        return

    stored_password = row[0]
    if hashed != stored_password:
        print("Невірний пароль. Видалення скасовано.")
        return

    cursor.execute("DELETE FROM users WHERE login = ?", (login,))
    conn.commit()
    print(f"Користувача '{login}' видалено.")


# Меню
def main():
    while True:
        print("\n1. Додати користувача")
        print("2. Оновити пароль")
        print("3. Аутентифікація")
        print("4. Перегляду усіх користувачів")
        print("5. Видалити користувача")
        print("6. Вихід")

        choice = input("Оберіть опцію: ")
        if choice == '1':
            add_user()
        elif choice == '2':
            update_password()
        elif choice == '3':
            authenticate()
        elif choice == '4':
            show_all_users()
        elif choice == '5':
            delete_user()
        elif choice == '6':
            break
        else:
            print("Невірний вибір.")

    conn.close()

if __name__ == '__main__':
    main()
