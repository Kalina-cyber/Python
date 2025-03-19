#Інвентаризація продуктів
inventory = {"яблука": 10, "банани": 3, "груші": 7, "апельсини": 2, "виноград": 6}


# Функція для оновлення інвентарю
def update_inventory(product, quantity):
    if product in inventory:
        inventory[product] += quantity  # Оновлюємо кількість продукту
        if inventory[product] < 0:
            inventory[product] = 0  # Запобігаємо від'ємній кількості
    else:
        if quantity > 0:
            inventory[product] = quantity  # Додаємо новий продукт
    print("Змінений інвентар:", inventory)

# Функція для отримання списку продуктів з кількістю менше ніж 5
def low_stock_items():
    low_stock = []  # Створюємо порожній список для збереження продуктів із низьким запасом
    for product, qty in inventory.items():  # Проходимося по кожному продукту та його кількості в інвентарі
        if qty < 5:  # Перевіряємо, чи кількість продукту менше 5
            low_stock.append(product)  # Додаємо продукт у список, якщо умова виконується
    return low_stock  # Повертаємо список продуктів із низьким запасом


# Приклад використання
if __name__ == "__main__":
    print("Актуальний інвентар:", inventory)

    update_inventory("банани", 5)  # Додаємо 5 бананів
    update_inventory("апельсини", -1)  # Видаляємо 1 апельсин
    update_inventory("персики", 4)  # Додаємо новий продукт

    print("Продукти з низьким запасом:", low_stock_items())
