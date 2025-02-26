import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Modern Calculator")
        master.geometry("500x550")  # Increased width for extra buttons
        master.configure(bg="#2C3E50")
        master.resizable(False, False)
        
        self.result_var = tk.StringVar()
        self.error_var = tk.StringVar()
        self.history = []
        self.theme = "dark"

        # Entry field
        self.entry = ttk.Entry(master, textvariable=self.result_var, font=('Arial', 22), justify='right')
        self.entry.grid(row=0, column=0, columnspan=6, ipadx=8, ipady=8, pady=10, padx=10, sticky='nsew')
        
        # Error label
        self.error_label = tk.Label(master, textvariable=self.error_var, font=('Arial', 12), fg='red', bg='#2C3E50')
        self.error_label.grid(row=1, column=0, columnspan=6, pady=5)
        
        self.create_buttons()
        self.create_theme_toggle()
        self.create_history_button()
        self.bind_keys()

    def create_buttons(self):
        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('+', 5, 2), ('=', 5, 3),
            ('C', 6, 0, 4), ('(', 2, 4), (')', 2, 5),
            ('sin', 3, 4), ('cos', 3, 5), ('tan', 4, 4), ('√', 4, 5),
            ('^', 5, 4), ('log', 5, 5)
        ]
        
        for button in buttons:
            text, row, col = button[:3]
            colspan = button[3] if len(button) == 4 else 1
            
            btn = tk.Button(self.master, text=text, font=('Arial', 16, 'bold'), bg="#3498DB", fg="white",
                            padx=20, pady=20, borderwidth=3, relief='raised',
                            command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=5, pady=5)
            
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2980B9"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#3498DB"))
            btn.bind("<ButtonPress>", lambda e, b=btn: b.config(bg="#1F618D"))
            btn.bind("<ButtonRelease>", lambda e, b=btn: b.config(bg="#3498DB"))
        
        for i in range(7):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.master.grid_columnconfigure(i, weight=1)

    def create_theme_toggle(self):
        self.theme_button = tk.Button(self.master, text="Change Theme", font=('Arial', 12), bg="#34495E", fg="white",
                                      padx=10, pady=5, command=self.toggle_theme)
        self.theme_button.grid(row=7, column=0, columnspan=6, pady=10, sticky='nsew')
    
    def create_history_button(self):
        self.history_button = tk.Button(self.master, text="Show History", font=('Arial', 12), bg="#34495E", fg="white",
                                        padx=10, pady=5, command=self.show_history)
        self.history_button.grid(row=8, column=0, columnspan=6, pady=10, sticky='nsew')
    
    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Calculation History")
        history_window.geometry("300x300")
        history_text = tk.Text(history_window, font=('Arial', 12))
        history_text.pack(expand=True, fill='both')
        history_text.insert('1.0', '\n'.join(self.history))
        history_text.config(state='disabled')
    
    def toggle_theme(self):
        themes = {
            "dark": ("#2C3E50", "#34495E", "white"),
            "light": ("#ECF0F1", "#BDC3C7", "black"),
            "blue_light": ("#D6EAF8", "#85C1E9", "black"),
            "high_contrast": ("#000000", "#FFD700", "white")
        }
        theme_keys = list(themes.keys())
        self.theme = theme_keys[(theme_keys.index(self.theme) + 1) % len(theme_keys)]
        bg, btn_bg, fg = themes[self.theme]
        self.master.configure(bg=bg)
        self.error_label.config(bg=bg, fg="red")
        self.theme_button.config(bg=btn_bg, fg=fg)
        self.history_button.config(bg=btn_bg, fg=fg)
    
    def bind_keys(self):
        self.master.bind("<Return>", lambda event: self.calculate())
        self.master.bind("<BackSpace>", lambda event: self.result_var.set(self.result_var.get()[:-1]))
        self.master.bind("<Control-c>", lambda event: self.master.clipboard_append(self.result_var.get()))
        self.master.bind("<Control-v>", lambda event: self.result_var.set(self.master.clipboard_get()))

    def button_click(self, value):
        if value == '=':
            self.calculate()
        elif value == 'C':
            self.result_var.set("")
            self.error_var.set("")
        elif value == '√':
            try:
                result = math.sqrt(float(self.result_var.get()))
                self.result_var.set(result)
            except ValueError:
                self.error_var.set("Invalid Input")
        elif value == '^':
            self.result_var.set(self.result_var.get() + '**')
        else:
            self.result_var.set(self.result_var.get() + str(value))
    
    def calculate(self):
        try:
            result = eval(self.result_var.get())
            self.history.append(f"{self.result_var.get()} = {result}")
            self.result_var.set(result)
            self.error_var.set("")
        except Exception:
            self.error_var.set("Error: Invalid Expression")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
