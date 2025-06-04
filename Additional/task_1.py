import sqlite3
from datetime import datetime, timedelta

# Підключення до БД та створення таблиць
def init_db():
    conn = sqlite3.connect("security_events.db")
    cur = conn.cursor()

    cur.execute("""
    PRAGMA foreign_keys = ON;
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS EventSources (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        location TEXT,
        type TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS EventTypes (
        id INTEGER PRIMARY KEY,
        type_name TEXT UNIQUE,
        severity TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS SecurityEvents (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME,
        source_id INTEGER,
        event_type_id INTEGER,
        message TEXT,
        ip_address TEXT,
        username TEXT,
        FOREIGN KEY (source_id) REFERENCES EventSources(id),
        FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
    );
    """)

    conn.commit()
    return conn

# Вставка тестових типів подій
def insert_event_types(conn):
    cur = conn.cursor()
    data = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical")
    ]
    for type_name, severity in data:
        try:
            cur.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", (type_name, severity))
        except sqlite3.IntegrityError:
            continue
    conn.commit()

# Функція для додавання джерела подій
def add_event_source(conn, name, location, type_):
    cur = conn.cursor()
    cur.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)", (name, location, type_))
    conn.commit()

# Функція для додавання типу подій
def add_event_type(conn, type_name, severity):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", (type_name, severity))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Тип події '{type_name}' вже існує.")

# Функція для запису події безпеки
def log_security_event(conn, source_id, event_type_id, message, ip_address=None, username=None):
    cur = conn.cursor()
    timestamp = datetime.now().isoformat()
    cur.execute("""
        INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, source_id, event_type_id, message, ip_address, username))
    conn.commit()

# Функції запиту даних:
# Отримати всі події Login Failed за останні 24 години
def get_login_failed_last_24h(conn):
    cur = conn.cursor()
    since = (datetime.now() - timedelta(days=1)).isoformat()
    cur.execute("""
        SELECT * FROM SecurityEvents 
        WHERE event_type_id = (SELECT id FROM EventTypes WHERE type_name = 'Login Failed') 
        AND timestamp >= ?
    """, (since,))
    return cur.fetchall()

# IP-адреси з більше ніж 5 невдалими входами за годину
def detect_brute_force_attempts(conn):
    cur = conn.cursor()
    one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
    cur.execute("""
        SELECT ip_address, COUNT(*) as attempts FROM SecurityEvents
        WHERE event_type_id = (SELECT id FROM EventTypes WHERE type_name = 'Login Failed')
        AND timestamp >= ? AND ip_address IS NOT NULL
        GROUP BY ip_address
        HAVING attempts > 5
    """, (one_hour_ago,))
    return cur.fetchall()

# Отримати всі події з рівнем серйозності "Critical" за останній тиждень, згруповані за джерелом.
def get_critical_events_last_week(conn):
    cur = conn.cursor()
    week_ago = (datetime.now() - timedelta(weeks=1)).isoformat()
    cur.execute("""
        SELECT es.name, COUNT(*) FROM SecurityEvents se
        JOIN EventTypes et ON se.event_type_id = et.id
        JOIN EventSources es ON se.source_id = es.id
        WHERE et.severity = 'Critical' AND se.timestamp >= ?
        GROUP BY se.source_id
    """, (week_ago,))
    return cur.fetchall()

# Знайти всі події, що містять певне ключове слово у повідомленні (message)
def search_events_by_keyword(conn, keyword):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM SecurityEvents
        WHERE message LIKE ?
    """, (f"%{keyword}%",))
    return cur.fetchall()

# Ініціалізація БД і тестування
if __name__ == '__main__':
    conn = init_db()
    insert_event_types(conn)

    # Приклад додавання джерел та подій
    for name, ip, type_ in [
        ("Firewall_A", "192.168.1.1", "Firewall"),
        ("Web_Server_Logs", "192.168.1.10", "Web Server"),
        ("IDS_Sensor_B", "192.168.1.20", "IDS")
    ]:
        try:
            add_event_source(conn, name, ip, type_)
        except Exception as e:
            print(f"Не вдалося додати {name}: {e}")

    # Приклад запису подій
    for i in range(10):
        log_security_event(
            conn,
            source_id=1,
            event_type_id=2,  # Login Failed
            message=f"Login failed attempt #{i+1}",
            ip_address="192.168.100.10",
            username="admin"
        )


    def main_menu(conn):
        while True:
            print("\n--- СИСТЕМА ЛОГУВАННЯ ПОДІЙ ---")
            print("1. Додати джерело подій")
            print("2. Додати тип події")
            print("3. Записати подію безпеки")
            print("4. Переглянути події 'Login Failed' за останні 24 години")
            print("5. Виявити IP з >5 невдалими входами за 1 годину")
            print("6. Переглянути критичні події за останній тиждень")
            print("7. Пошук подій за ключовим словом")
            print("0. Вихід")

            choice = input("Оберіть опцію: ")

            if choice == "1":
                name = input("Назва джерела: ")
                location = input("Місцезнаходження/IP: ")
                type_ = input("Тип джерела: ")
                add_event_source(conn, name, location, type_)

            elif choice == "2":
                type_name = input("Назва типу події: ")
                severity = input("Рівень серйозності (Informational/Warning/Critical): ")
                add_event_type(conn, type_name, severity)

            elif choice == "3":
                source_id = int(input("ID джерела: "))
                event_type_id = int(input("ID типу події: "))
                message = input("Повідомлення: ")
                ip_address = input("IP-адреса (можна залишити порожнім): ") or None
                username = input("Ім'я користувача (можна залишити порожнім): ") or None
                log_security_event(conn, source_id, event_type_id, message, ip_address, username)

            elif choice == "4":
                rows = get_login_failed_last_24h(conn)
                print("--- Події 'Login Failed' за 24 год ---")
                for row in rows:
                    print(row)

            elif choice == "5":
                print("--- Підозрілі IP з >5 невдалими входами ---")
                for row in detect_brute_force_attempts(conn):
                    print(f"IP: {row[0]} | Кількість: {row[1]}")

            elif choice == "6":
                print("--- Критичні події за останній тиждень ---")
                for row in get_critical_events_last_week(conn):
                    print(f"Джерело: {row[0]} | Кількість: {row[1]}")

            elif choice == "7":
                keyword = input("Введіть ключове слово для пошуку: ")
                results = search_events_by_keyword(conn, keyword)
                for row in results:
                    print(row)

            elif choice == "0":
                print("Вихід з програми.")
                break

            else:
                print("Невірна опція. Спробуйте ще раз.")


    if __name__ == '__main__':
        conn = init_db()
        insert_event_types(conn)
        main_menu(conn)
        conn.close()

    # print(get_login_failed_last_24h(conn))
    # print(detect_brute_force_attempts(conn))
    # print(get_critical_events_last_week(conn))
    # print(search_events_by_keyword(conn, "failed"))