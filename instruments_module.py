import tkinter as tk
from tkinter import ttk, messagebox, Spinbox
from tkcalendar import DateEntry
from languages import t
from database import get_manufacturers, get_categories, get_countries, get_sellers, get_sales_staff, add_instrument

# Список продавцов из  таблицы сотрудников

def open_instruments_window():
    window = tk.Toplevel()
    window.title("Добавление товара")
    window.geometry("580x820")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text=t("add_instrument"), font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=20)

    frame = tk.Frame(window, bg="#f8f9fa")
    frame.pack(padx=40, pady=10)

    # Поля
    row = 0

    # Название
    tk.Label(frame, text=t("name"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    name_entry = tk.Entry(frame, width=40, font=("Arial", 10))
    name_entry.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    # Производитель
    tk.Label(frame, text=t("manufacturer"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    manufacturer_combo = ttk.Combobox(frame, values=get_manufacturers(), width=37, state="readonly")
    manufacturer_combo.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    # Категория
    tk.Label(frame, text=t("category"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    category_combo = ttk.Combobox(frame, values=get_categories(), width=37, state="readonly")
    category_combo.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    # Год
    tk.Label(frame, text=t("year"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    year_spin = Spinbox(frame, from_=1950, to=2026, width=37, font=("Arial", 10))
    year_spin.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    # Цена
    tk.Label(frame, text=t("price"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    price_entry = tk.Entry(frame, width=40, font=("Arial", 10))
    price_entry.grid(row=row, column=1, pady=8, padx=10)
    def live_format(e):
        try:
            val = price_entry.get().replace(" ", "").replace("₽", "")
            if val.isdigit():
                price_entry.delete(0, tk.END)
                price_entry.insert(0, f"{int(val):,} ₽".replace(",", " "))
        except:
            pass
    price_entry.bind("<KeyRelease>", live_format)
    row += 1

    # Страна
    tk.Label(frame, text=t("country"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    country_combo = ttk.Combobox(frame, values=get_countries(), width=37, state="readonly")
    country_combo.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    # Количество
    tk.Label(frame, text=t("quantity"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    qty_entry = tk.Entry(frame, width=40, font=("Arial", 10))
    qty_entry.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    # Даты
    tk.Label(frame, text=t("supply_date"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    supply_date = DateEntry(frame, width=37, background="#4CAF50")
    supply_date.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    tk.Label(frame, text=t("sale_date"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    sale_date = DateEntry(frame, width=37, background="#4CAF50")
    sale_date.grid(row=row, column=1, pady=8, padx=10)
    row += 1

    # Продавец (справочник)
    tk.Label(frame, text=t("seller"), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    seller_combo = ttk.Combobox(
        frame,
        values=get_sales_staff(),
        width=37,
        state="readonly"
)
    seller_combo.grid(row=row, column=1, pady=8, padx=10)
    row += 1
    tk.Label(frame, text="Статус товара", font=("Arial", 11, "bold")).grid(row=row, column=0, sticky="w")
    row += 1
    # Статус
    tk.Label(frame, text=t(""), bg="#f8f9fa", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=8)
    status_combo = ttk.Combobox(frame, values=["Не продан", "Продан"], width=37, state="readonly")
    status_combo.current(0)
    status_combo.grid(row=row, column=1, pady=8, padx=10)

    def save():
        try:
            price = int(price_entry.get().replace(" ", "").replace("₽", "")
            )

            add_instrument(
                name_entry.get(),
                manufacturer_combo.get(),
                category_combo.get(),
                int(year_spin.get()),
                price,
                country_combo.get(),
                int(qty_entry.get()),
                supply_date.get(),
                sale_date.get(),
                status_combo.get(),
                seller_combo.get()
            )

            messagebox.showinfo(
                "Успех",
                "Товар добавлен"
            )

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Ошибка",
                str(e)
            )