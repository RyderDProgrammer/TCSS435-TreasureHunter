import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button, RadioButtons
import BFS, DFS, UCS



class GridGame:
    def __init__(self):
        
        self.n = 8
        self.PADDING_RATIO = 0.05
        self.current_algorithm = "None"
        self.algorithms = {"BFS": BFS, "DFS": DFS, "UCS": UCS}
        
        # Create figure and main axes
        self.fig = plt.figure(figsize=(12, 10))
        self.fig.canvas.manager.set_window_title("435 GUI")
        
        # Center window and set to 70% of screen size
        manager = plt.get_current_fig_manager()
        try:
            # Get screen dimensions
            screen_width = manager.window.winfo_screenwidth()
            screen_height = manager.window.winfo_screenheight()
            
            # Calculate 70% dimensions
            window_width = int(screen_width * 0.7)
            window_height = int(screen_height * 0.7)
            
            # Calculate position to center
            x_pos = int((screen_width - window_width) / 2)
            y_pos = int((screen_height - window_height) / 2)
            
            # Set geometry
            manager.window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        except:
            # Fallback for non-Tkinter backends
            pass
        
        # Main grid axes
        self.ax = self.fig.add_axes([0.05, 0.15, 0.9, 0.8])
        self.ax.axis("off")
        
        # Create buttons
        button_y = 0.05
        button_height = 0.06
        
        ax_decrease = self.fig.add_axes([0.05, button_y, 0.15, button_height])
        self.btn_decrease = Button(ax_decrease, 'Decrease Size')
        self.btn_decrease.on_clicked(self.decrease_size)
        
        ax_increase = self.fig.add_axes([0.21, button_y, 0.15, button_height])
        self.btn_increase = Button(ax_increase, 'Increase Size')
        self.btn_increase.on_clicked(self.increase_size)
        
        ax_bfs = self.fig.add_axes([0.37, button_y, 0.08, button_height])
        self.btn_bfs = Button(ax_bfs, 'BFS')
        self.btn_bfs.on_clicked(lambda event: self.set_algorithm('BFS'))
        
        ax_dfs = self.fig.add_axes([0.46, button_y, 0.08, button_height])
        self.btn_dfs = Button(ax_dfs, 'DFS')
        self.btn_dfs.on_clicked(lambda event: self.set_algorithm('DFS'))
        
        ax_ucs = self.fig.add_axes([0.55, button_y, 0.08, button_height])
        self.btn_ucs = Button(ax_ucs, 'UCS')
        self.btn_ucs.on_clicked(lambda event: self.set_algorithm('UCS'))
        
        ax_new_grid = self.fig.add_axes([0.70, button_y, 0.25, button_height])
        self.btn_new_grid = Button(ax_new_grid, 'New Grid')
        self.btn_new_grid.on_clicked(self.create_new_grid)
        
        self.create_grid()
        plt.show()

    def set_algorithm(self, algo):
        self.current_algorithm = algo
        self.update_title()

    def update_title(self):
        self.fig.suptitle(f"Grid Size: {self.n}x{self.n} | Algorithm: {self.current_algorithm} | Cost: 0", 
                         fontsize=14, fontweight='bold')
        self.fig.canvas.draw_idle()

    def create_grid(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.axis("off")

        grid = [[' ' for _ in range(self.n)] for _ in range(self.n)]
        treasure = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
        grid[treasure[0]][treasure[1]] = 'T'

        while True:
            start = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            if start != treasure:
                grid[start[0]][start[1]] = 'S'
                break

        while True:
            trap = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            if trap != treasure and trap != start:
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
                color = {'T': 'gold', 'X': 'red', '#': 'gray', 'S': 'blue'}.get(val, 'white')
                fg = 'white' if val in ['T', 'X', '#'] else 'black'

                rect = patches.Rectangle((j, self.n - i - 1), 1, 1,
                                         facecolor=color, edgecolor='black', linewidth=1.3)
                self.ax.add_patch(rect)

                if val.strip():
                    self.ax.text(j + 0.5, self.n - i - 0.5, val, ha='center', va='center',
                                 color=fg, fontsize=max(10, 180 // self.n), fontweight='bold')
        self.grid = grid

        self.update_title()
        self.fig.canvas.draw_idle()

    def increase_size(self, event):
        self.n += 1
        self.create_grid()

    def decrease_size(self, event):
        if self.n > 8:
            self.n -= 1
            self.create_grid()

    def create_new_grid(self, event):
        self.create_grid()


if __name__ == "__main__":
    GridGame()