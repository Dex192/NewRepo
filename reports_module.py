import tkinter as tk
from tkinter import messagebox
import os
from openpyxl import Workbook
from database import get_all_instruments


def export_to_excel():

    if not os.path.exists("exports"):
        os.makedirs("exports")

    wb = Workbook()
    ws = wb.active

    ws.append([
        "ID",
        "Название",
        "Производитель",
        "Категория",
        "Год",
        "Цена",
        "Страна",
        "Количество",
        "Дата поставки",
        "Дата продажи",
        "Статус",
        "Продавец"
    ])

    for item in get_all_instruments():

        ws.append([
            item[0],
            item[1],
            item[2],
            item[3],
            item[4],
            f"{item[5]:,} ₽".replace(",", " "),
            item[6],
            item[7],
            item[8],
            item[9],
            item[10],
            item[11]
        ])

    wb.save("exports/report.xlsx")


def export_to_txt():

    if not os.path.exists("exports"):
        os.makedirs("exports")

    with open("exports/report.txt", "w", encoding="utf-8") as f:

        f.write("ОТЧЁТ ПО МУЗЫКАЛЬНЫМ ИНСТРУМЕНТАМ\n\n")

        for item in get_all_instruments():

            price = f"{item[5]:,} ₽".replace(",", " ")

            f.write(
                f"{item[1]} | "
                f"{item[2]} | "
                f"{item[3]} | "
                f"{price} | "
                f"{item[10]} | "
                f"{item[11]}\n"
            )


def open_reports_window():

    window = tk.Toplevel()
    window.title("Отчёты")
    window.geometry("400x300")

    tk.Label(
        window,
        text="Формирование отчетов",
        font=("Arial", 14)
    ).pack(pady=20)

    def excel():

        export_to_excel()

        messagebox.showinfo(
            "Успех",
            "Excel отчет создан"
        )

    def txt():

        export_to_txt()

        messagebox.showinfo(
            "Успех",
            "TXT отчет создан"
        )

    tk.Button(
        window,
        text="Экспорт Excel",
        width=20,
        command=excel
    ).pack(pady=10)

    tk.Button(
        window,
        text="Экспорт TXT",
        width=20,
        command=txt
    ).pack(pady=10)

    tk.Button(
        window,
        text="Закрыть",
        width=20,
        command=window.destroy
    ).pack(pady=10)