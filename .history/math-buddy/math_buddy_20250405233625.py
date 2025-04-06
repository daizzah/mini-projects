import tkinter as tk
from tkinter import ttk
import random
import sympy as sp
import math
import ttkbootstrap as ttk
from ttkbootstrap import Window
from ttkbootstrap.widgets import Button

class MathBuddyApp:
    def __init__(self, root):
        self.style = ttk.Style()

        self.style.configure("TButton", font=("Comic Sans MS", 14, "bold"))
        self.style.configure("TFrame", background="#f8c2f4")


        self.root = root
        self.root.title("Math Buddy")
        self.root.geometry("600x500")
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # or use a default if available


        self.x = sp.Symbol('x')
        self.current_equation = None

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.algebra_tab = ttk.Frame(self.notebook, style="TFrame")
        self.trig_tab = ttk.Frame(self.notebook, style="TFrame")
        self.geo_tab = ttk.Frame(self.notebook, style="TFrame")

        self.notebook.add(self.algebra_tab, text="Algebra")
        self.notebook.add(self.trig_tab, text="Trigonometry")
        self.notebook.add(self.geo_tab, text="Geometry")

        self.setup_algebra_tab()
        self.setup_trig_tab()
        self.setup_geo_tab()

    def styled_container(self, tab):
        container = ttk.Frame(tab, style="TFrame")
        container.pack(expand=True, fill="both", pady=0)
        return container

    def styled_label(self, container, text, size=16, bold=False):
        style_name = f"My.TLabel{size}{'Bold' if bold else ''}"
        font = ("Comic Sans MS", size, "bold" if bold else "normal")

        if not self.style.lookup(style_name, "font"):
            self.style.layout(style_name, self.style.layout("TLabel"))
            self.style.configure(style_name, font=font, foreground="#3c2c66", background="#f8c2f4")
            self.style.map(style_name, background=[("!disabled", "#f8c2f4")])

        return ttk.Label(container, text=text, style=style_name, anchor="center", justify="center")


    def styled_button(self, container, text, command, color):
        return Button(
            container,
            text=text,
            command=command,
            bootstyle=f"{color}-outline rounded-pill",
            padding=10,
            takefocus=False  # <-- this line disables the focus border
        )

    def setup_algebra_tab(self):
        container = self.styled_container(self.algebra_tab)

        self.styled_label(container, "Algebra Practice", size=20, bold=True).pack(pady=10)
        self.algebra_generate_button = self.styled_button(container, "🎲 Generate Another Equation", self.generate_algebra, "info")
        self.algebra_generate_button.pack(pady=10)

        self.algebra_equation_label = self.styled_label(container, "", size=18, bold=True)
        self.algebra_equation_label.pack(pady=10)

        self.algebra_solve_button = self.styled_button(container, "✅ Solve", self.solve_algebra, "danger")
        self.algebra_solve_button.pack(pady=10)

        self.algebra_solution_label = self.styled_label(container, "", size=16)
        self.algebra_solution_label.pack(pady=10)

    def setup_trig_tab(self):
        container = self.styled_container(self.trig_tab)

        self.styled_label(container, "Trigonometry Practice", size=20, bold=True).pack(pady=10)
        self.trig_generate_button = self.styled_button(container, "🎲 Generate Another Problem", self.generate_trig, "info")
        self.trig_generate_button.pack(pady=10)

        self.trig_question_label = self.styled_label(container, "", size=16)
        self.trig_question_label.pack(pady=10)

        self.trig_solve_button = self.styled_button(container, "✅ Solve", self.solve_trig, "danger")
        self.trig_solve_button.pack(pady=10)

        self.trig_solution_label = self.styled_label(container, "", size=16)
        self.trig_solution_label.pack(pady=10)

    def setup_geo_tab(self):
        container = self.styled_container(self.geo_tab)

        self.styled_label(container, "Geometry Practice", size=20, bold=True).pack(pady=10)
        self.geo_generate_button = self.styled_button(container, "🎲 Generate Another Problem", self.generate_geometry, "info")
        self.geo_generate_button.pack(pady=10)

        self.geo_question_label = self.styled_label(container, "", size=16)
        self.geo_question_label.pack(pady=10)

        self.geo_solve_button = self.styled_button(container, "✅ Solve", self.solve_geometry, "danger")
        self.geo_solve_button.pack(pady=10)

        self.geo_solution_label = self.styled_label(container, "", size=16)
        self.geo_solution_label.pack(pady=10)

    def generate_algebra(self):
        while True:
            equation_type = random.choice(["linear", "quadratic", "complex_linear"])
            if equation_type == "linear":
                a, b = random.randint(1, 10), random.randint(-10, 10)
                equation = sp.Eq(a * self.x + b, 0)
            elif equation_type == "complex_linear":
                a, b, c, d = random.randint(1, 10), random.randint(-10, 10), random.randint(1, 10), random.randint(-10, 10)
                equation = sp.Eq(a * self.x + b, c * self.x + d)
            else:
                a, b, c = random.randint(1, 5), random.randint(-10, 10), random.randint(-10, 10)
                discriminant = (b ** 2) - (4 * a * c)
                if discriminant < 0:
                    continue
                equation = sp.Eq(a * self.x**2 + b * self.x + c, 0)
            if isinstance(equation, (bool, type(None))) or equation == False:
                continue
            self.current_equation = equation
            break
        self.algebra_equation_label.config(text=f"Solve: {sp.latex(self.current_equation)}")
        self.algebra_solution_label.config(text="")

    def solve_algebra(self):
        if self.current_equation is not None:
            solutions = sp.solve(self.current_equation.lhs - self.current_equation.rhs, self.x)
            formatted_solutions = []
            for sol in solutions:
                if sol.is_real:
                    fraction = str(sol)
                    decimal = round(float(sp.N(sol, 5)), 2)
                    if '/' in fraction or 'sqrt' in fraction:
                        formatted_solutions.append(f"{fraction} ≈ {decimal}")
                    elif fraction.isdigit() or (fraction.startswith('-') and fraction[1:].isdigit()):
                        formatted_solutions.append(f"{fraction}")
                    else:
                        formatted_solutions.append(f"{fraction} ≈ {decimal}")
            solution_text = f"Solution: {', '.join(formatted_solutions)}" if formatted_solutions else "Solution: No Real Solution"
            self.algebra_solution_label.config(text=solution_text)

    def generate_trig(self):
        angle = random.choice([30, 45, 60, 90])
        side = random.randint(5, 15)
        self.trig_question_label.config(text=f"Find the opposite side if angle is {angle}° and adjacent = {side}")
        self.trig_solution_label.config(text="")
        self.trig_calc_value = round(math.tan(math.radians(angle)) * side, 2)

    def solve_trig(self):
        self.trig_solution_label.config(text=f"Solution: Opposite ≈ {self.trig_calc_value}")

    def generate_geometry(self):
        radius = random.randint(1, 10)
        self.geo_question_label.config(text=f"Find the area of a circle with radius {radius}")
        self.geo_solution_label.config(text="")
        self.geo_area = round(math.pi * radius**2, 2)

    def solve_geometry(self):
        self.geo_solution_label.config(text=f"Solution: Area ≈ {self.geo_area}")

if __name__ == "__main__":
    root = Window(themename="minty")
    app = MathBuddyApp(root)
    root.mainloop()
