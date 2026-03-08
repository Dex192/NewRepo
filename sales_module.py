import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

DB = "music_store.db"


def format_price(value):
    return f"{value:,}₽".replace(",", " ")

def create_receipt(name, qty, price, total, seller):

    import os
    from datetime import datetime

    if not os.path.exists("receipts"):
        os.makedirs("receipts")

    filename = f"receipts/receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:

        f.write("МУЗЫКАЛЬНЫЙ МАГАЗИН\n")
        f.write("====================\n\n")

        f.write(f"Товар: {name}\n")
        f.write(f"Количество: {qty}\n")
        f.write(f"Цена: {format_price(price)}\n")
        f.write(f"Итого: {format_price(total)}\n")
        f.write(f"Продавец: {seller}\n")

        f.write("\nСпасибо за покупку!")
        

def open_sales_window():

    window = tk.Toplevel()
    window.title("Создание продажи")
    window.geometry("500x500")

    tk.Label(window, text="Создание продажи",
             font=("Arial", 16)).pack(pady=10)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, price, quantity
        FROM instruments
        WHERE status='Не продан'
    """)

    products = cursor.fetchall()
    conn.close()

    product_dict = {
        f"{p[1]} ({format_price(p[2])})": p
        for p in products
    }

    tk.Label(window, text="Выберите товар").pack()
    product_combo = ttk.Combobox(
        window,
        values=list(product_dict.keys()),
        state="readonly",
        width=40
    )
    product_combo.pack()

    tk.Label(window, text="Количество").pack()
    quantity_entry = tk.Entry(window)
    quantity_entry.pack()

    tk.Label(window, text="Дата продажи").pack()
    sale_date = DateEntry(window)
    sale_date.pack()

    tk.Label(window, text="Продавец").pack()
    seller_entry = tk.Entry(window)
    seller_entry.pack()

    result_label = tk.Label(window, text="")
    result_label.pack(pady=10)

    def calculate():

        product_key = product_combo.get()
        qty = int(quantity_entry.get())

        if product_key not in product_dict:
            return

        product = product_dict[product_key]
        price = product[2]
        total = price * qty

        result_label.config(
            text=f"Итого: {format_price(total)}"
        )

    def confirm_sale():
       product_key = product_combo.get()
       qty = int(quantity_entry.get())

       if product_key not in product_dict:
           messagebox.showerror("Ошибка", "Выберите товар")
           return

       product = product_dict[product_key]

       product_id = product[0]
       name = product[1]
       price = product[2]
       current_qty = product[3]

       if qty > current_qty:
           messagebox.showerror("Ошибка", "Недостаточно товара")
           return

       total = price * qty

       conn = sqlite3.connect(DB)
       cursor = conn.cursor()

       new_qty = current_qty - qty

       status = "Продан" if new_qty == 0 else "Не продан"

       cursor.execute("""
            UPDATE instruments
            SET quantity=?,
                sale_date=?,
                seller=?,
                status=?
            WHERE id=?
        """, (
            new_qty,
            sale_date.get(),
            seller_entry.get(),
            status,
            product_id
        ))

       conn.commit()
       conn.close()

        
       create_receipt(
            name,
            qty,
            price,
            total,
            seller_entry.get()
        )

       messagebox.showinfo("Успех", "Продажа оформлена")

       window.destroy()

