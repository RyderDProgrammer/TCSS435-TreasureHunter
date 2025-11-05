import random
import time
import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import BFS, DFS, UCS
import A_Star, Greedy_BFS

class GridGame:
    def __init__(self):
        self.n = 20
        self.traps = 2
        self.treasures = 3
        self.PADDING_RATIO = 0.05
        self.current_algorithm = "None"
        self.current_cost = 0
        self.current_runtime = 0.0
        self.solution_path = []
        self.expanded_nodes = 0
        
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
        BUTTON_Y = 0.05
        BUTTON_HEIGHT = 0.06
        BUTTON_WIDTH_SMALL = 0.08
        BUTTON_WIDTH_MEDIUM = 0.15
        BUTTON_WIDTH_LARGE = 0.25
        
        ax_decrease = self.fig.add_axes([0.05, BUTTON_Y, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT])
        self.btn_decrease = Button(ax_decrease, 'Decrease Size')
        self.btn_decrease.on_clicked(self.decrease_size)
        
        ax_increase = self.fig.add_axes([0.21, BUTTON_Y, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT])
        self.btn_increase = Button(ax_increase, 'Increase Size')
        self.btn_increase.on_clicked(self.increase_size)
        
        ax_bfs = self.fig.add_axes([0.37, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
        self.btn_bfs = Button(ax_bfs, 'BFS')
        self.btn_bfs.on_clicked(self.do_BFS)
        
        ax_dfs = self.fig.add_axes([0.46, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
        self.btn_dfs = Button(ax_dfs, 'DFS')
        self.btn_dfs.on_clicked(self.do_DFS)
        
        ax_ucs = self.fig.add_axes([0.55, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
        self.btn_ucs = Button(ax_ucs, 'UCS')
        self.btn_ucs.on_clicked(self.do_UCS)

        ax_a_star = self.fig.add_axes([0.64, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
        self.btn_a_star = Button(ax_a_star, 'A*')
        self.btn_a_star.on_clicked(self.do_A_Star)

        ax_greedy = self.fig.add_axes([0.73, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
        self.btn_greedy = Button(ax_greedy, 'Greedy BFS')
        self.btn_greedy.on_clicked(self.do_Greedy_BFS)
        
        ax_new_grid = self.fig.add_axes([0.82, BUTTON_Y, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT])
        self.btn_new_grid = Button(ax_new_grid, 'New Grid')
        self.btn_new_grid.on_clicked(self.create_grid)
        
        self.create_grid()
        plt.show()

    def set_algorithm(self, algo):
        self.current_algorithm = algo
        self.update_title()

    def update_title(self):
        runtime_str = f"{self.current_runtime:.4f}s" if self.current_runtime > 0 else "N/A"
        self.fig.suptitle(
            f"Grid Size: {self.n}x{self.n} " +
            f"| Algorithm: {self.current_algorithm} " + 
            f"| Cost: {self.current_cost} " +
            f"| Runtime: {runtime_str} " +
            f"| Expanded Nodes: {self.expanded_nodes}",
            fontsize=14, fontweight='bold')
        self.fig.canvas.draw_idle()

    def create_grid(self, event=None):
        self.ax.clear()
        self.solution_path = []
        self.current_cost = 0
        self.current_runtime = 0.0
        self.set_algorithm("None")
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.axis("off")

        grid = [[' ' for _ in range(self.n)] for _ in range(self.n)]

        # add treasures to an 'end' list
        self.end = []
        for i in range(self.treasures):
            while True:
                treasure = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
                if treasure not in self.end:
                    break

            grid[treasure[0]][treasure[1]] = 'T'
            self.end.append(treasure)
        
        # create starting position
        while True:
            start = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            if start not in self.end:
                grid[start[0]][start[1]] = 'S'

                # record start position for searching
                self.start = (start[0], start[1])
                break

        # create traps
        traps = []
        for i in range(self.traps):
            while True:
                trap = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
                if trap not in self.end and trap != start and trap not in traps:
                    grid[trap[0]][trap[1]] = 'X'
                    self.Trap = trap
                    break

            traps.append(trap)

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
        
    def solution_path_helper(self, color: str) -> None:
        for (i, j) in self.solution_path[1:-1]:  # Exclude start and end
            rect = patches.Rectangle((j, self.n - i - 1), 1, 1,
                                    facecolor=color, edgecolor='black', linewidth=1.3)
            if (self.grid[i][j] == 'X' ):
                rect.set_color('purple')
            if(self.grid[i][j] == 'X' and color == 'white'):
                rect.set_color('red')
            self.ax.add_patch(rect)
        self.fig.canvas.draw_idle()
    
    def highlight_solution_path(self):
        self.solution_path_helper('lightblue')
        
    def reset_solution_highlight(self):
        self.solution_path_helper('white')
        
    # --- Uninformed searches ---
    def algorithm_helper(self, algorithm_name: str, algorithm_func) -> None:
        self.reset_solution_highlight()
        self.set_algorithm(algorithm_name)
        start_time = time.time()

        # self.solution_path, self.expanded_nodes = algorithm_func(self.grid, self.start, self.end)

        # below is a method that I've tried, but I dont think is correct
        # (im keepign this here for safe measures)

        self.expanded_nodes = 0
        self.solution_path = []

        # use dictionary and Euclidean distance to find closest treasures
        dict = {}
        for t in self.end:
            dict[t] = math.sqrt((t[0] - self.start[0]) ** 2 + (t[1] - self.start[1]) ** 2)

        # sort values of dictionary
        keys = list(dict.keys())
        values = list(dict.values())
        sorted_value_index = numpy.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index} 

        # perform searches
        start = self.start
        for t in sorted_dict:
            path, expanded = algorithm_func(self.grid, start, t)
            self.expanded_nodes += expanded
            for c in path:
                self.solution_path.append(c)
            start = t

        end_time = time.time()
        self.current_runtime = end_time - start_time
        self.algorithm_updates()
        print(f"Runtime {algorithm_name}: {self.current_runtime:.4f}s")
        print(f"Nodes Expanded: {self.expanded_nodes}")
        print(f"Total Cost: {self.current_cost}")
        
    def do_BFS(self, event=None) -> None:
        self.algorithm_helper('BFS', BFS.BFS)
        
    def do_DFS(self, event=None) -> None:
        self.algorithm_helper('DFS', DFS.DFS)

    def do_UCS(self, event=None) -> None:
        self.algorithm_helper('UCS', UCS.UCS)

    # --- Informed Searches ---
    def do_A_Star(self, event=None) -> None:
        self.algorithm_helper('A*', A_Star.A_Star)

    def do_Greedy_BFS(self, event=None) -> None:
        self.algorithm_helper('Greedy BFS', Greedy_BFS.Greedy_BFS)
        
    def algorithm_updates(self) -> None:
        self.current_cost = len(self.solution_path) - 1 if self.solution_path else 0
        self.update_title()
        self.highlight_solution_path()
        print(self.solution_path)

if __name__ == "__main__":
    GridGame()