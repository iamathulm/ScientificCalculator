import tkinter as tk
from tkinter import ttk
from calculator_logic import CalculatorLogic


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("420x600")
        self.root.resizable(False, False)

        self.logic = CalculatorLogic(angle_mode="DEG")

        # Expression variable for display
        self.expr_var = tk.StringVar()
        self.expr_var.set("")

        # ---------------- Display ----------------
        display_frame = tk.Frame(root, padx=10, pady=10)
        display_frame.pack(fill="x")

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expr_var,
            font=("Arial", 22),
            justify="right",
            bd=10,
            relief="sunken"
        )
        self.display.pack(fill="x", ipady=10)

        # ---------------- Mode Toggle ----------------
        mode_frame = tk.Frame(root, padx=10)
        mode_frame.pack(fill="x")

        self.mode_btn = ttk.Button(mode_frame, text="Mode: DEG", command=self.toggle_mode)
        self.mode_btn.pack(fill="x", pady=5)

        # ---------------- Buttons ----------------
        btn_frame = tk.Frame(root, padx=10, pady=10)
        btn_frame.pack(expand=True, fill="both")

        buttons = [
            ["C", "⌫", "(", ")"],
            ["sin", "cos", "tan", "^"],
            ["ln", "log", "sqrt", "root"],
            ["fact", "nPr", "nCr", "exp"],
            ["pi", "e", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", ""],
        ]

        for r in range(len(buttons)):
            btn_frame.rowconfigure(r, weight=1)
            for c in range(4):
                btn_frame.columnconfigure(c, weight=1)

                text = buttons[r][c]
                if text == "":
                    continue

                btn = tk.Button(
                    btn_frame,
                    text=text,
                    font=("Arial", 16),
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        # ---------------- Keyboard Support ----------------
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.clear())

    # ---------------- Button Actions ----------------
    def on_button_click(self, text):
        if text == "C":
            self.clear()
        elif text == "⌫":
            self.backspace()
        elif text == "=":
            self.calculate()
        elif text in ("sin", "cos", "tan", "ln", "log", "sqrt", "fact", "nPr", "nCr", "exp"):
            self.append_text(f"{text}(")
        elif text == "root":
            # root(x,n) needs comma, so give user a template
            self.append_text("root(")
        elif text == "pi":
            self.append_text("pi")
        elif text == "e":
            self.append_text("e")
        else:
            self.append_text(text)

    def append_text(self, value):
        current = self.expr_var.get()
        self.expr_var.set(current + str(value))

    def clear(self):
        self.expr_var.set("")

    def backspace(self):
        current = self.expr_var.get()
        self.expr_var.set(current[:-1])

    def calculate(self):
        expr = self.expr_var.get()
        result = self.logic.evaluate(expr)
        self.expr_var.set(result)

    def toggle_mode(self):
        if self.logic.angle_mode == "DEG":
            self.logic.set_angle_mode("RAD")
            self.mode_btn.config(text="Mode: RAD")
        else:
            self.logic.set_angle_mode("DEG")
            self.mode_btn.config(text="Mode: DEG")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
