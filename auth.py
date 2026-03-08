import tkinter as tk
from tkinter import messagebox
from database import authenticate_user


def open_login_window(on_success):

    login = tk.Tk()
    login.title("Авторизация")
    login.geometry("400x350")
    login.resizable(False, False)

    bg = "#1e1e1e"
    fg = "white"
    btn_bg = "#3a3a3a"

    login.configure(bg=bg)

    frame = tk.Frame(login, bg=bg)
    frame.pack(expand=True)

    tk.Label(frame, text="Вход в систему",
             font=("Arial", 16, "bold"),
             bg=bg, fg=fg).pack(pady=20)

    tk.Label(frame, text="Email",
             bg=bg, fg=fg).pack()

    email_entry = tk.Entry(frame, width=30)
    email_entry.pack(pady=5)

    tk.Label(frame, text="Пароль",
             bg=bg, fg=fg).pack()

    password_entry = tk.Entry(frame, width=30, show="*")
    password_entry.pack(pady=5)

    def login_action():

        user = authenticate_user(
            email_entry.get(),
            password_entry.get()
        )

        if user:
            full_name, position, role = user
            login.destroy()
            on_success(full_name, role)
        else:
            messagebox.showerror(
                "Ошибка",
                "Неверный email или пароль"
            )

    tk.Button(frame,
              text="Войти",
              bg=btn_bg,
              fg=fg,
              width=20,
              command=login_action).pack(pady=10)

    tk.Button(frame,
              text="Выход",
              bg=btn_bg,
              fg=fg,
              width=20,
              command=login.destroy).pack()

    login.mainloop()