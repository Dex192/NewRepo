"""
Проверяет корректность вводимых данных.
"""

from datetime import datetime


def validate_instrument(name, manufacturer, year, price):
   

    if not name.strip():
        return False, "Название обязательно"

    if not manufacturer.strip() or manufacturer.isdigit():
        return False, "Производитель указан некорректно"

    try:
        year = int(year)
        current_year = datetime.now().year

        if year < 1900 or year > current_year:
            return False, "Год указан некорректно"
    except ValueError:
        return False, "Год должен быть числом"

    try:
        price = float(price)
        if price <= 0:
            return False, "Цена должна быть больше 0"
    except ValueError:
        return False, "Цена должна быть числом"

    return True, ""
