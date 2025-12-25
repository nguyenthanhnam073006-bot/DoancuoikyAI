import tkinter as tk
from tkinter import ttk
import random
import time

from greedy import solve_tsp_greedy
from astar import solve_tsp_astar

WIDTH, HEIGHT = 720, 600
GRID_SIZE = 40
ANIM_DELAY = 120  # ms


class TSPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bài toán Người Du Lịch (TSP)")
        self.root.configure(bg="#e0f2fe")

        self.cities = []
        self.weights = []

        self.path_greedy = []
        self.path_astar = []

        self.anim_index_g = 0
        self.anim_index_a = 0

        self.setup_style()
        self.create_layout()

    # ================= STYLE =================
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", background="#e0f2fe",
                        foreground="#1e3a8a", font=("Arial", 10))
        style.configure("Title.TLabel",
                        font=("Arial", 20, "bold"),
                        foreground="#1e40af")
        style.configure("CardTitle.TLabel",
                        font=("Arial", 13, "bold"),
                        foreground="#2563eb",
                        background="#bbf7d0")
        style.configure("Info.TLabel",
                        foreground="#374151",
                        font=("Arial", 10))
        style.configure("TButton",
                        font=("Arial", 10),
                        padding=8)

    # ================= LAYOUT =================
    def create_layout(self):
        header = tk.Frame(self.root, bg="#bbf7d0", padx=20, pady=15)
        header.pack(fill="x")

        ttk.Label(header, text="BÀI TOÁN NGƯỜI DU LỊCH (TSP)",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="So sánh Greedy và A* Algorithm",
                  background="#bbf7d0").pack(anchor="w")

        ttk.Separator(self.root).pack(fill="x", padx=20, pady=10)

        main = tk.Frame(self.root, bg="#e0f2fe")
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Sidebar
        sidebar = tk.Frame(main, bg="#bbf7d0", width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        settings = tk.Frame(sidebar, bg="#ffffff", padx=15, pady=15)
        settings.pack(fill="x")

        ttk.Label(settings, text="Thiết lập",
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(settings, text="Số thành phố").pack(anchor="w")
        self.n_var = tk.IntVar(value=10)
        ttk.Entry(settings, textvariable=self.n_var,
                  width=10).pack(pady=5)

        ttk.Label(settings, text="Chế độ chạy").pack(anchor="w", pady=(10, 0))
        self.mode = tk.StringVar(value="So sánh")
        ttk.Combobox(settings, textvariable=self.mode,
                     values=["Greedy", "A*", "So sánh"],
                     state="readonly",
                     width=12).pack(pady=5)

        ttk.Button(settings, text="Chạy",
                   command=self.run).pack(fill="x", pady=(15, 5))
        ttk.Button(settings, text="Làm lại",
                   command=self.reset).pack(fill="x")

        result = tk.Frame(sidebar, bg="#ffffff", padx=15, pady=15)
        result.pack(fill="x", pady=(10, 0))

        ttk.Label(result, text="Kết quả",
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        self.info = ttk.Label(result, text="Chưa chạy thuật toán",
                              style="Info.TLabel",
                              wraplength=230,
                              justify="left")
        self.info.pack(anchor="w")

        # Canvas
        canvas_frame = tk.Frame(main, bg="#bbf7d0", padx=10, pady=10)
        canvas_frame.pack(side="right", fill="both", expand=True)

        self.canvas_container = tk.Frame(canvas_frame, bg="#bbf7d0")
        self.canvas_container.pack(fill="both", expand=True)

        self.canvas_greedy = tk.Canvas(
            self.canvas_container, bg="#ffffff",
            highlightthickness=1, highlightbackground="#93c5fd")

        self.canvas_astar = tk.Canvas(
            self.canvas_container, bg="#ffffff",
            highlightthickness=1, highlightbackground="#fca5a5")

    # ================= DRAW =================
    def draw_grid(self, canvas):
        for x in range(0, WIDTH // 2, GRID_SIZE):
            canvas.create_line(x, 0, x, HEIGHT, fill="#e5e7eb")
        for y in range(0, HEIGHT, GRID_SIZE):
            canvas.create_line(0, y, WIDTH // 2, y, fill="#e5e7eb")

    def draw_cities(self, canvas):
        for i, ((x, y), w) in enumerate(zip(self.cities, self.weights)):
            r = 6
            canvas.create_oval(x-r, y-r, x+r, y+r, fill="#000000")
            canvas.create_text(x, y-15,
                               text=f"{chr(65+i)}({w})",
                               font=("Arial", 9, "bold"))

    def animate_path(self, canvas, path, index, color):
        if index < len(path) - 1:
            x1, y1 = self.cities[path[index]]
            x2, y2 = self.cities[path[index + 1]]
            canvas.create_line(x1, y1, x2, y2,
                               fill=color, width=2)
            self.root.after(
                ANIM_DELAY,
                lambda: self.animate_path(canvas, path, index + 1, color)
            )

    # ================= LOGIC =================
    def generate_cities(self):
        self.cities.clear()
        self.weights.clear()
        for _ in range(self.n_var.get()):
            x = random.randint(40, WIDTH//2 - 40)
            y = random.randint(40, HEIGHT - 40)
            self.cities.append((x, y))
            self.weights.append(random.randint(1, 9))

    def run(self):
        for w in self.canvas_container.winfo_children():
            w.pack_forget()

        self.generate_cities()
        mode = self.mode.get()

        if mode == "So sánh":
            self.canvas_greedy.pack(side="left", fill="both", expand=True)
            self.canvas_astar.pack(side="right", fill="both", expand=True)

            for c in (self.canvas_greedy, self.canvas_astar):
                c.delete("all")
                self.draw_grid(c)
                self.draw_cities(c)

            start_g = time.time()
            self.path_greedy, dist_g = solve_tsp_greedy(self.cities, 0)
            time_g = time.time() - start_g

            start_a = time.time()
            self.path_astar, dist_a = solve_tsp_astar(self.cities)
            time_a = time.time() - start_a

            self.animate_path(self.canvas_greedy,
                              self.path_greedy, 0, "#2563eb")
            self.animate_path(self.canvas_astar,
                              self.path_astar, 0, "#dc2626")

            self.info.config(
                text=(
                    "So sánh Greedy và A*\n"
                    f"Greedy:\n  Quãng đường: {dist_g:.2f}\n"
                    f"  Thời gian: {time_g:.5f}s\n\n"
                    f"A*:\n  Quãng đường: {dist_a:.2f}\n"
                    f"  Thời gian: {time_a:.5f}s"
                )
            )

        else:
            self.canvas_greedy.pack(fill="both", expand=True)
            self.canvas_greedy.delete("all")
            self.draw_grid(self.canvas_greedy)
            self.draw_cities(self.canvas_greedy)

            start = time.time()
            if mode == "Greedy":
                path, dist = solve_tsp_greedy(self.cities, 0)
                color = "#2563eb"
            else:
                path, dist = solve_tsp_astar(self.cities)
                color = "#dc2626"
            elapsed = time.time() - start

            self.animate_path(self.canvas_greedy, path, 0, color)
            self.info.config(
                text=f"{mode}\nQuãng đường: {dist:.2f}\n"
                     f"Thời gian chạy: {elapsed:.5f}s"
            )

    def reset(self):
        for w in self.canvas_container.winfo_children():
            w.pack_forget()
        self.info.config(text="Chưa chạy thuật toán")


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = TSPGUI(root)
    root.mainloop()
