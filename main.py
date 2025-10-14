import tkinter as tk
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import BFS, DFS, UCS
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class GridGame:
    def __init__(self, gui):
        self.root = gui
        self.root.title("435 GUI")

        SCREEN_WIDTH = gui.winfo_screenwidth()
        SCREEN_HEIGHT = gui.winfo_screenheight()
        WINDOW_WIDTH = int(SCREEN_WIDTH * 0.75)
        WINDOW_HEIGHT = int(SCREEN_HEIGHT * 0.75)

        x = (SCREEN_WIDTH - WINDOW_WIDTH) // 2
        y = (SCREEN_HEIGHT - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        self.root.minsize(900, 700)

        self.n = 8
        self.PADDING_RATIO = 0.05  # 5% margin around edges

        # Configure layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

        # --- Controls ---
        control_frame = tk.Frame(gui)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        for i in range(5):
            control_frame.columnconfigure(i, weight=1)

        self.decrease_button = tk.Button(control_frame, text="Decrease Size", command=self.decrease_size)
        self.decrease_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.increase_button = tk.Button(control_frame, text="Increase Size", command=self.increase_size)
        self.increase_button.grid(row=0, column=1, padx=5, sticky="ew")

        self.size_label = tk.Label(control_frame, text=f"Grid Size: {self.n}x{self.n}", font=("Arial", 12, "bold"))
        self.size_label.grid(row=0, column=2, padx=5, sticky="ew")

        self.algorithm_var = tk.StringVar(value="BFS")
        self.algorithm_menu = tk.OptionMenu(control_frame, self.algorithm_var, "BFS", "DFS", "UCS")
        self.algorithm_menu.grid(row=0, column=3, padx=5, sticky="ew")
        self.algorithms = {"BFS": BFS, "DFS": DFS, "UCS": UCS}

        self.new_grid_button = tk.Button(control_frame, text="New Grid", command=self.create_new_grid)
        self.new_grid_button.grid(row=0, column=4, padx=5, sticky="ew")

        # --- Canvas Frame ---
        self.canvas_frame = tk.Frame(gui, bg="white", highlightthickness=0, bd=0)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew")
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        # Matplotlib figure
        self.fig = plt.Figure(dpi=100)
        self.ax = self.fig.add_axes([0, 0, 1, 1])  # use full canvas
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        self.canvas_frame.bind("<Configure>", self._on_resize)

        self.create_grid()

    def _on_resize(self, event):
        width, height = max(1, event.width), max(1, event.height)
        dpi = self.fig.get_dpi()
        self.fig.set_size_inches(width / dpi, height / dpi, forward=True)

        pad = self.PADDING_RATIO
        self.ax.set_position([pad, pad, 1 - 2 * pad, 1 - 2 * pad])
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.canvas.draw_idle()

    def create_grid(self):
        self.ax.clear()

        pad = self.PADDING_RATIO
        self.ax.set_position([pad, pad, 1 - 2 * pad, 1 - 2 * pad])
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.axis("off")

        grid = [[' ' for _ in range(self.n)] for _ in range(self.n)]
        treasure = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
        grid[treasure[0]][treasure[1]] = 'T'

        while True:
            trap = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            if trap != treasure:
                grid[trap[0]][trap[1]] = 'X'
                break

        num_walls = random.randint(int(self.n ** 2 * 0.1), int(self.n ** 2 * 0.15))
        placed = 0
        while placed < num_walls:
            i, j = random.randint(0, self.n - 1), random.randint(0, self.n - 1)
            if grid[i][j] == ' ':
                grid[i][j] = '#'
                placed += 1

        for i in range(self.n):
            for j in range(self.n):
                val = grid[i][j]
                color = {'T': 'gold', 'X': 'red', '#': 'gray'}.get(val, 'white')
                fg = 'white' if val in ['T', 'X', '#'] else 'black'

                rect = patches.Rectangle((j, self.n - i - 1), 1, 1,
                                         facecolor=color, edgecolor='black', linewidth=1.3)
                self.ax.add_patch(rect)

                if val.strip():
                    self.ax.text(j + 0.5, self.n - i - 0.5, val, ha='center', va='center',
                                 color=fg, fontsize=max(10, 180 // self.n), fontweight='bold')

        self.canvas.draw()
        self.size_label.config(text=f"Grid Size: {self.n}x{self.n}")

    def increase_size(self):
        self.n += 1
        self.create_grid()

    def decrease_size(self):
        if self.n > 8:
            self.n -= 1
            self.create_grid()

    def create_new_grid(self):
        self.create_grid()


if __name__ == "__main__":
    root = tk.Tk()
    GridGame(root)
    root.mainloop()
