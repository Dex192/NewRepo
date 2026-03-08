import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

DB = "music_store.db"


def get_all_instruments():
    """Получаем все товары для выбора"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, quantity FROM instruments ORDER BY name")
    data = cursor.fetchall()
    conn.close()
    return data


def open_supplies_window():
    window = tk.Toplevel()
    window.title("Учёт поставок")
    window.geometry("520x420")
    window.resizable(False, False)

    tk.Label(window, text="Приём новой поставки", font=("Arial", 16, "bold")).pack(pady=15)

    instruments = get_all_instruments()
    product_dict = {f"{row[1]} (ID: {row[0]})": row for row in instruments}

    tk.Label(window, text="Выберите товар:").pack(anchor="w", padx=30, pady=(10, 5))
    product_combo = ttk.Combobox(window, values=list(product_dict.keys()), width=45, state="readonly")
    product_combo.pack(padx=30)

    tk.Label(window, text="Количество в поставке:").pack(anchor="w", padx=30, pady=(15, 5))
    qty_entry = tk.Entry(window, width=20, font=("Arial", 12))
    qty_entry.pack(padx=30)

    tk.Label(window, text="Дата поставки:").pack(anchor="w", padx=30, pady=(15, 5))
    supply_date = DateEntry(window, width=20, background="darkblue", foreground="white", borderwidth=2)
    supply_date.pack(padx=30)

    result_label = tk.Label(window, text="", font=("Arial", 11), fg="green")
    result_label.pack(pady=15)

    def accept_supply():
        if not product_combo.get():
            messagebox.showerror("Ошибка", "Выберите товар")
            return

        try:
            qty = int(qty_entry.get())
            if qty <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Количество должно быть числом больше 0")
            return

        # Получаем данные товара
        product = product_dict[product_combo.get()]
        product_id = product[0]
        current_qty = product[3]

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        new_qty = current_qty + qty

        cursor.execute("""
            UPDATE instruments
            SET quantity = ?,
                supply_date = ?,
                status = 'Не продан'
            WHERE id = ?
        """, (new_qty, supply_date.get(), product_id))

        conn.commit()
        conn.close()

        result_label.config(text=f"✅ Поставка принята! Новый остаток: {new_qty} шт.")
        messagebox.showinfo("Успех", f"Поставка успешно добавлена!\nОстаток: {new_qty} шт.")

        # Очищаем поля
        qty_entry.delete(0, tk.END)

    tk.Button(
        window,
        text="Принять поставку",
        command=accept_supply,
        width=25,
        height=2,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 11, "bold")
    ).pack(pady=20)

    tk.Button(window, text="Закрыть", command=window.destroy, width=20).pack()