"""
Главный модуль приложения.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from database import (
    initialize_db,
    search_instruments,
    delete_instrument,
    get_category_statistics,
)

from auth import open_login_window
from instruments_module import open_instruments_window
from sales_module import open_sales_window
from supplies_module import open_supplies_window
from reports_module import open_reports_window
from database import seed_employees, authenticate_user
from storage import backup_database
from app_logger import log_action

from languages import (
    t,
    set_language,
    load_language,
    get_current_language
)


# Инициализация базы, языка и сотрудников
initialize_db()
load_language()
seed_employees()

# ==========================================
# ГЛАВНОЕ ОКНО
# ==========================================

def open_main_window(username, role, position):


    root = tk.Tk()
    root.title(t("title"))
    root.geometry("1200x700")

    theme_var = tk.StringVar(value="dark")
    tk.Label(
    root,
    text=f"Здравствуйте, {username} ({position})",
    font=("Arial", 14, "bold")).pack(pady=10)
    if role == "seller":

        for btn in btn_frame.winfo_children():

            if btn.cget("text") in ["Удалить", "Backup"]:
                btn.config(state="disabled")


    # ==========================================
    # ТЕМА
    # ==========================================

    def apply_theme():

        if theme_var.get() == "dark":

            bg = "#2b2b2b"
            fg = "white"
            btn_bg = "#404040"

        else:

            bg = "#f0f0f0"
            fg = "black"
            btn_bg = "#e0e0e0"


        root.configure(bg=bg)

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            rowheight=25
        )

        style.configure(
            "Treeview.Heading",
            background=btn_bg,
            foreground=fg
        )

        # Красим все элементы
        for widget in root.winfo_children():

            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass

            for child in widget.winfo_children():

                try:
                    child.configure(bg=bg, fg=fg)
                except:
                    pass

        # Красим кнопки отдельно
        for btn in btn_frame.winfo_children():

            btn.configure(
                bg=btn_bg,
                fg=fg,
                activebackground=btn_bg
            )


    # ==========================================
    # ТАБЛИЦА
    # ==========================================

    columns = (
        "id",
        "name",
        "manufacturer",
        "category",
        "year",
        "price",
        "country",
        "quantity",
        "status"
    )

    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=20
    )

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    headings = [
        "ID",
        "Название",
        "Производитель",
        "Категория",
        "Год",
        "Цена",
        "Страна",
        "Количество",
        "Статус"
    ]

    for col, text in zip(columns, headings):

        tree.heading(col, text=text)
        tree.column(col, width=130)


    # ==========================================
    # ПОИСК
    # ==========================================

    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)


    tk.Label(search_frame, text="Поиск").pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)


    tk.Label(search_frame, text="Категория").pack(side=tk.LEFT)

    category_combo = ttk.Combobox(
        search_frame,
        values=[
            "Все",
            "Струнные",
            "Клавишные",
            "Ударные",
            "Звук",
            "Аксессуары"
        ],
        width=20
    )

    category_combo.current(0)
    category_combo.pack(side=tk.LEFT, padx=5)


    def refresh_table():

        tree.delete(*tree.get_children())

        data = search_instruments(
            search_entry.get(),
            category_combo.get()
        )

        for row in data:

            tree.insert("", tk.END, values=row)


    tk.Button(
        search_frame,
        text="Найти",
        command=refresh_table
    ).pack(side=tk.LEFT, padx=5)


    # ==========================================
    # КНОПКИ
    # ==========================================

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)


    def delete_selected():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Ошибка",
                "Выберите товар"
            )
            return


        item_id = tree.item(selected[0])["values"][0]

        delete_instrument(item_id)

        refresh_table()


    def show_stats():

        data = get_category_statistics()

        if not data:
            return

        categories = [x[0] for x in data]
        counts = [x[1] for x in data]

        plt.bar(categories, counts)
        plt.title("Статистика")
        plt.show()


    def change_language():
        new_lang = "en" if get_current_language() == "ru" else "ru"
        set_language(new_lang)

        root.destroy()
        open_main_window(username, position, role)


    def change_theme():

        if theme_var.get() == "dark":

            theme_var.set("light")

        else:

            theme_var.set("dark")

        apply_theme()


    buttons = [

        (t("add"), open_instruments_window),

        (t("delete"), delete_selected),

        (t("sales"), open_sales_window),

        (t("supplies"), open_supplies_window),

        (t("reports"), open_reports_window),

        (t("stats"), show_stats),

        (t("backup"), backup_database),

        ("RU/EN", change_language),

        (t("theme"), change_theme),

        (t("exit"), root.destroy)

    ]


    for text, cmd in buttons:

        tk.Button(
            btn_frame,
            text=text,
            width=14,
            height=2,
            command=cmd
        ).pack(side=tk.LEFT, padx=5)


    # ВАЖНО — применять тему ПОСЛЕ создания кнопок
    apply_theme()

    refresh_table()

    root.mainloop()



# ==========================================
# Логин
# ==========================================

def on_login_success(username, role):

    log_action(f"Login: {username} ({role})")

    open_main_window(username, role, position=None)



# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    open_login_window(on_login_success)