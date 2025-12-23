import tkinter as tk
from tkinter import ttk
import random
import time

from greedy import solve_tsp_greedy
from pso import solve_tsp_pso

WIDTH, HEIGHT = 720, 600


class TSPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bài toán Người Du Lịch (TSP)")
        self.root.configure(bg="#e0f2fe")

        self.cities = []
        self.path_greedy = []
        self.path_pso = []
        self.anim_index = 0
        self.compare_mode = False

        self.setup_style()
        self.create_layout()

    # ================= STYLE =================
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel",
                        background="#e0f2fe",
                        foreground="#1e3a8a",
                        font=("Arial", 10))

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

        ttk.Label(header,
                  text="BÀI TOÁN NGƯỜI DU LỊCH (TSP)",
                  style="Title.TLabel").pack(anchor="w")

        ttk.Label(header,
                  text="So sánh Greedy và Particle Swarm Optimization",
                  foreground="#374151",
                  background="#bbf7d0").pack(anchor="w")

        ttk.Separator(self.root).pack(fill="x", padx=20, pady=10)

        main = tk.Frame(self.root, bg="#e0f2fe")
        main.pack(fill="both", expand=True, padx=20, pady=10)

        sidebar = tk.Frame(main, bg="#bbf7d0", width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        settings = tk.Frame(sidebar, bg="#ffffff", padx=15, pady=15)
        settings.pack(fill="x")

        ttk.Label(settings, text="Thiết lập",
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(settings, text="Số thành phố").pack(anchor="w")
        self.n_var = tk.IntVar(value=15)
        ttk.Entry(settings, textvariable=self.n_var, width=10).pack(pady=5)

        ttk.Label(settings, text="Chế độ chạy").pack(anchor="w", pady=(10, 0))
        self.mode = tk.StringVar(value="So sánh")
        ttk.Combobox(settings,
                     textvariable=self.mode,
                     values=["Greedy", "PSO", "So sánh"],
                     state="readonly",
                     width=12).pack(pady=5)

        ttk.Button(settings, text="Chạy", command=self.run).pack(fill="x", pady=(15, 5))
        ttk.Button(settings, text="Làm lại", command=self.reset).pack(fill="x")

        result = tk.Frame(sidebar, bg="#ffffff", padx=15, pady=15)
        result.pack(fill="x", pady=(10, 0))

        ttk.Label(result, text="Kết quả",
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        self.info = ttk.Label(result,
                              text="Chưa chạy thuật toán",
                              style="Info.TLabel",
                              wraplength=230,
                              justify="left")
        self.info.pack(anchor="w")

        canvas_frame = tk.Frame(main, bg="#bbf7d0", padx=10, pady=10)
        canvas_frame.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=WIDTH,
            height=HEIGHT,
            bg="#ffffff",
            highlightthickness=1,
            highlightbackground="#93c5fd"
        )
        self.canvas.pack(fill="both", expand=True)

    # ================= DRAWING =================
    def draw_cities(self):
        for i, (x, y) in enumerate(self.cities):
            r = 6
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="#000000",
                outline="",
                tags="city"
            )
            self.canvas.create_rectangle(
                x - 10, y - 26, x + 10, y - 10,
                fill="#ffffff",
                outline="",
                tags="label_bg"
            )
            self.canvas.create_text(
                x, y - 18,
                text=chr(65 + i),
                fill="#1e3a8a",
                font=("Arial", 9, "bold"),
                tags="label"
            )

        self.canvas.tag_raise("label_bg")
        self.canvas.tag_raise("label")
        self.canvas.tag_raise("city")

    def animate_path(self):
        if self.compare_mode:
            if self.anim_index < max(len(self.path_greedy), len(self.path_pso)) - 1:
                # Greedy
                if self.anim_index < len(self.path_greedy) - 1:
                    i = self.anim_index
                    x1, y1 = self.cities[self.path_greedy[i]]
                    x2, y2 = self.cities[self.path_greedy[i + 1]]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#2563eb", width=2)
                # PSO
                if self.anim_index < len(self.path_pso) - 1:
                    i = self.anim_index
                    x1, y1 = self.cities[self.path_pso[i]]
                    x2, y2 = self.cities[self.path_pso[i + 1]]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#dc2626", width=2)

                self.anim_index += 1
                self.root.after(120, self.animate_path)
            else:
                self.draw_cities()
        else:
            if self.anim_index < len(self.path_greedy) - 1:
                i = self.anim_index
                x1, y1 = self.cities[self.path_greedy[i]]
                x2, y2 = self.cities[self.path_greedy[i + 1]]
                color = "#2563eb" if self.mode.get() == "Greedy" else "#dc2626"
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                self.anim_index += 1
                self.root.after(120, self.animate_path)
            else:
                self.draw_cities()

    # ================= LOGIC =================
    def generate_cities(self):
        self.cities = [
            (random.randint(40, WIDTH - 40),
             random.randint(40, HEIGHT - 40))
            for _ in range(self.n_var.get())
        ]

    def run(self):
        self.canvas.delete("all")
        self.generate_cities()
        self.draw_cities()

        mode = self.mode.get()

        if mode == "Greedy":
            start = time.time()
            self.path_greedy, dist = solve_tsp_greedy(self.cities, 0)
            elapsed_greedy = time.time() - start
            self.compare_mode = False
            dist_str = f"{dist:.2f}"
            info_text = f"Chế độ: Greedy\nQuãng đường: {dist_str}\nThời gian chạy: {elapsed_greedy:.4f} giây"

        elif mode == "PSO":
            start = time.time()
            self.path_greedy, dist = solve_tsp_pso(self.cities)
            elapsed_pso = time.time() - start
            self.compare_mode = False
            dist_str = f"{dist:.2f}"
            info_text = f"Chế độ: PSO\nQuãng đường: {dist_str}\nThời gian chạy: {elapsed_pso:.4f} giây"

        else:  # So sánh
            start_g = time.time()
            self.path_greedy, dist_g = solve_tsp_greedy(self.cities, 0)
            elapsed_g = time.time() - start_g

            start_p = time.time()
            self.path_pso, dist_p = solve_tsp_pso(self.cities)
            elapsed_p = time.time() - start_p

            self.compare_mode = True

            # Tính % cải thiện Greedy so với PSO
            if dist_g > dist_p:
                improve = (dist_g - dist_p) / dist_p * 100
                improve_str = f"Greedy dài hơn PSO {improve:.2f}%"
            else:
                improve = (dist_p - dist_g) / dist_p * 100
                improve_str = f"Greedy ngắn hơn PSO {improve:.2f}%"

            dist_str = f"Greedy: {dist_g:.2f}, PSO: {dist_p:.2f} ({improve_str})"
            info_text = (f"Chế độ: So sánh\n{dist_str}\n"
                         f"Thời gian chạy Greedy: {elapsed_g:.4f} giây\n"
                         f"Thời gian chạy PSO: {elapsed_p:.4f} giây\n"
                         f"Tổng thời gian chạy: {elapsed_g + elapsed_p:.4f} giây")

        self.anim_index = 0
        self.animate_path()
        self.info.config(text=info_text)

    def reset(self):
        self.canvas.delete("all")
        self.info.config(text="Chưa chạy thuật toán")


if __name__ == "__main__":
    root = tk.Tk()
    TSPGUI(root)
    root.mainloop()
