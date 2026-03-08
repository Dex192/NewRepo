import json

current_language = "ru"

translations = {
    "ru": {
        "title": "Музыкальный магазин",
        "search": "Поиск",
        "category": "Категория",
        "find": "Найти",
        "add": "Добавить",
        "edit": "Редактировать",
        "delete": "Удалить",
        "export": "Экспорт",
        "backup": "Резервная копия",
        "add_product": "Добавление товара",
        "stats": "Статистика",
        "supply_date": "Дата поставки",
        "sale_date": "Дата продажи",
        "supplies": "Поставки",
        "sales": "Продажи",
        "saler": "Продавец",
        "reports": "Отчёты",
        "load_demo": "Загрузить демо-данные",
        "theme": "Тема",
        "exit": "Выход",
        "id": "ID",
        "name": "Название",
        "manufacturer": "Производитель",
        "type": "Категория",
        "year": "Год",
        "price": "Цена",
        "country": "Страна",
        "quantity": "Количество",
        "status": "Статус",
        "attention": "Внимание",
        "no_items": "Товаров нет или ничего не выбрано ❌",
        "success": "Успех",
        "demo_loaded": "15 товаров загружено!"
    },
    "en": {
        "title": "Music Store",
        "search": "Search",
        "category": "Category",
        "find": "Find",
        "add": "Add",
        "add_product": "Add Product",
        "supply_date": "Supply Date",
        "sale_date": "Sale Date",
        "seller": "Seller",
        "save": "Save Product",
        "edit": "Edit",
        "delete": "Delete",
        "export": "Export",
        "backup": "Backup",
        "stats": "Statistics",
        "supplies": "Supplies",
        "sales": "Sales",
        "reports": "Reports",
        "load_demo": "Load demo data",
        "theme": "Theme",
        "exit": "Exit",
        "id": "ID",
        "name": "Name",
        "manufacturer": "Manufacturer",
        "type": "Category",
        "year": "Year",
        "price": "Price",
        "country": "Country",
        "quantity": "Quantity",
        "status": "Status",
        "attention": "Attention",
        "no_items": "No items or nothing selected ❌",
        "success": "Success",
        "demo_loaded": "15 items loaded!"
    }
}

def set_language(lang):
    global current_language
    current_language = lang
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        config["language"] = lang
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except:
        pass

def load_language():
    global current_language
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            current_language = config.get("language", "ru")
    except:
        current_language = "ru"

def t(key):
    return translations[current_language].get(key, key)

def get_current_language():
    return current_language