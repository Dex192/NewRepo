"""
Модуль работы с базой данных.
"""

import sqlite3

DB_NAME = "music_store.db"



def add_password_column():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE employees ADD COLUMN password TEXT")
    except:
        pass  # если колонка уже есть

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            manufacturer TEXT,
            category TEXT,
            year INTEGER,
            price INTEGER,
            country TEXT,
            quantity INTEGER DEFAULT 1,
            supply_date TEXT,
            sale_date TEXT,
            seller TEXT,
            status TEXT DEFAULT 'Не продан'
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        middle_name TEXT,
        position TEXT,
        phone TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manufacturers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    manufacturers = ["Fender","Gibson","Yamaha","Roland","Korg","Ibanez","Ludwig","Casio","Shure","Behringer","Marshall","Pearl","D'Addario","On-Stage"]
    cursor.executemany("INSERT OR IGNORE INTO manufacturers(name) VALUES (?)", [(m,) for m in manufacturers])
    conn.commit()
    conn.close()


def get_manufacturers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT manufacturer FROM instruments")

    data = [row[0] for row in cursor.fetchall() if row[0]]

    conn.close()

    if not data:
        return ["Fender", "Gibson", "Yamaha", "Roland"]

    return data


def get_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM instruments")

    data = [row[0] for row in cursor.fetchall() if row[0]]

    conn.close()

    if not data:
        return ["Струнные", "Клавишные", "Ударные"]

    return data


def get_countries():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT country FROM instruments")

    data = [row[0] for row in cursor.fetchall() if row[0]]

    conn.close()

    if not data:
        return ["США", "Япония", "Германия"]

    return data

def get_sales_staff():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT last_name || ' ' || first_name || ' ' || middle_name
    FROM employees
    WHERE role IN ('seller', 'manager')
    """)

    staff = [row[0] for row in cursor.fetchall()]

    conn.close()

    return staff

def get_sellers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT full_name FROM sellers")

    sellers = [row[0] for row in cursor.fetchall()]

    conn.close()

    return sellers

def seed_sellers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sellers")

    if cursor.fetchone()[0] == 0:

        default_sellers = [
            "Иванов Иван Иванович",
            "Смирнова Светлана Алексеевна",
            "Кузнецов Николай Васильевич"
        ]

        for s in default_sellers:
            cursor.execute(
                "INSERT INTO sellers(full_name) VALUES (?)",
                (s,)
            )

    conn.commit()
    conn.close()


def seed_employees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")

    if cursor.fetchone()[0] == 0:

        employees = [

            (1, "Иван", "Иванов", "Петрович", "Менеджер  заказов",
             "+7-910-123-45-67", "ivan@email.com", "1234", "manager"),

            (2, "Светлана", "Смирнова", "Алексеевна", "Продавец-консультант",
             "+7-925-234-56-78", "svetlana@email.com", "1234", "seller"),

            (3, "Николай", "Кузнецов", "Васильевич", "Руководитель",
             "+7-912-456-78-90", "admin@email.com", "admin", "admin"),
        ]

        cursor.executemany("""
        INSERT INTO employees
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, employees)

    conn.commit()
    conn.close()    

def authenticate_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT last_name || ' ' || first_name || ' ' || middle_name,
           position,
           role
    FROM employees
    WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user

def fill_test_data():
    """Загружает 15 тестовых товаров"""
    data = [
        ("Fender Stratocaster", "Fender", "Струнные", 2006, 12000, "США"),
        ("Gibson Les Paul", "Gibson", "Струнные", 2006, 15000, "США"),
        ("Yamaha Acoustic Guitar", "Yamaha", "Струнные", 2015, 8000, "Япония"),
        ("Ibanez Bass Guitar", "Ibanez", "Струнные", 2014, 11000, "Япония"),
        ("Yamaha Grand Piano", "Yamaha", "Клавишные", 2013, 20000, "Япония"),
        ("Casio Digital Piano", "Casio", "Клавишные", 2016, 9000, "Япония"),
        ("Roland Synthesizer", "Roland", "Клавишные", 2018, 14000, "Япония"),
        ("Ludwig Drums", "Ludwig", "Ударные", 2010, 5000, "США"),
        ("Pearl Drum Set", "Pearl", "Ударные", 2017, 7000, "Япония"),
        ("Shure SM58 Microphone", "Shure", "Звук", 2018, 4000, "США"),
        ("Behringer Audio Interface", "Behringer", "Звук", 2012, 6000, "Германия"),
        ("Marshall Combo Amplifier", "Marshall", "Звук", 2010, 13000, "Великобритания"),
        ("Guitar Strings D'Addario", "D'Addario", "Аксессуары", 2018, 800, "Франция"),
        ("Guitar Picks Set", "D'Addario", "Аксессуары", 2016, 300, "Франция"),
        ("Keyboard Stand", "On-Stage", "Аксессуары", 2019, 1200, "Германия"),
    ]

    conn = get_connection()
    cursor = conn.cursor()
    for row in data:
        cursor.execute("""
            INSERT OR IGNORE INTO instruments 
            (name, manufacturer, category, year, price, country, quantity, status)
            VALUES (?,?,?,?,?,?,1,'Не продан')
        """, row)
    conn.commit()
    conn.close()
    print("✅ 15 тестовых товаров загружено")

def search_instruments(keyword="", category="Все"):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, manufacturer, category, year, price, country, quantity, status FROM instruments WHERE 1=1"
    params = []
    if keyword:
        query += " AND (name LIKE ? OR manufacturer LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if category != "Все":
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    return cursor.fetchall()

def delete_instrument(instrument_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM instruments WHERE id=?", (instrument_id,))
    conn.commit()
    conn.close()

def get_category_statistics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) FROM instruments GROUP BY category ORDER BY COUNT(*) DESC")
    return cursor.fetchall()

def get_all_instruments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM instruments ORDER BY id")
    return cursor.fetchall()

def add_instrument(
        name,
        manufacturer,
        category,
        year,
        price,
        country,
        quantity,
        supply_date,
        sale_date,
        status,
        seller
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO instruments(
        name,
        manufacturer,
        category,
        year,
        price,
        country,
        quantity,
        supply_date,
        sale_date,
        status,
        seller
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        manufacturer,
        category,
        year,
        price,
        country,
        quantity,
        supply_date,
        sale_date,
        status,
        seller
    ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    seed_sellers()
    seed_employees()