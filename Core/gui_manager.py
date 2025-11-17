import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button


class GUIManager:
    def __init__(self, grid_size=15):
        self.n = grid_size
        self.fog_of_war = False  # For human mode

        # Create figure and main axes
        self.fig = plt.figure(figsize=(12, 10))
        self.fig.canvas.manager.set_window_title("435 GUI")

        # Center window and set to 70% of screen size
        self._setup_window()

        # Main grid axes
        self.ax = self.fig.add_axes([0.05, 0.15, 0.9, 0.8])
        self.ax.axis("off")

        # Button references
        self.buttons = {}

    def _setup_window(self):
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

    def create_buttons(self, callbacks):
        BUTTON_Y = 0.05
        BUTTON_HEIGHT = 0.06
        BUTTON_WIDTH_SMALL = 0.065
        BUTTON_WIDTH_MEDIUM = 0.10
        BUTTON_SPACING = 0.020

        x_pos = 0.02

        # Size control buttons
        ax_decrease = self.fig.add_axes([x_pos, BUTTON_Y, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT])
        self.buttons['decrease'] = Button(ax_decrease, 'Decrease')
        self.buttons['decrease'].on_clicked(callbacks.get('decrease'))
        x_pos += BUTTON_WIDTH_MEDIUM + BUTTON_SPACING

        ax_increase = self.fig.add_axes([x_pos, BUTTON_Y, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT])
        self.buttons['increase'] = Button(ax_increase, 'Increase')
        self.buttons['increase'].on_clicked(callbacks.get('increase'))
        x_pos += BUTTON_WIDTH_MEDIUM + BUTTON_SPACING

        # Algorithm buttons
        algorithm_buttons = [
            ('BFS', 'bfs'),
            ('DFS', 'dfs'),
            ('UCS', 'ucs'),
            ('A*', 'a_star'),
            ('Greedy', 'greedy'),
            ('MiniMax', 'minimax'),
            ('Alpha-Beta', 'alpha_beta')
        ]

        for label, key in algorithm_buttons:
            ax = self.fig.add_axes([x_pos, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
            self.buttons[key] = Button(ax, label)
            self.buttons[key].on_clicked(callbacks.get(key))
            x_pos += BUTTON_WIDTH_SMALL + BUTTON_SPACING

        # New grid button
        ax_new_grid = self.fig.add_axes([x_pos, BUTTON_Y, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT])
        self.buttons['new_grid'] = Button(ax_new_grid, 'New Grid')
        self.buttons['new_grid'].on_clicked(callbacks.get('new_grid'))

    def render_grid(self, grid, solution_path=None):
        self.ax.clear()
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.axis("off")

        for i in range(self.n):
            for j in range(self.n):
                val = grid[i][j]

                # Apply fog of war for human mode
                if self.fog_of_war and val not in ['S']:
                    display_val = '?'
                    color = 'lightgray'
                    fg = 'black'
                else:
                    display_val = val
                    color = {'T': 'gold', 'X': 'red', '#': 'gray', 'S': 'blue'}.get(val, 'white')
                    fg = 'white' if val in ['T', 'X', '#'] else 'black'

                # Highlight solution path
                if solution_path and (i, j) in solution_path[1:-1]:
                    if grid[i][j] == 'X':
                        color = 'purple'
                    elif grid[i][j] == 'T':
                        color = 'green'
                    elif grid[i][j] not in ['S']:
                        color = 'lightblue'

                rect = patches.Rectangle((j, self.n - i - 1), 1, 1,
                                        facecolor=color, edgecolor='black', linewidth=1.3)
                self.ax.add_patch(rect)

                if display_val.strip():
                    self.ax.text(j + 0.5, self.n - i - 0.5, display_val, ha='center', va='center',
                               color=fg, fontsize=max(10, 180 // self.n), fontweight='bold')

        self.fig.canvas.draw_idle()

    def update_title(self, info):
        runtime_str = f"{info.get('runtime', 0):.4f}s" if info.get('runtime', 0) > 0 else "N/A"
        heuristic_str = f"{info.get('heuristic'):.2f}" if info.get('heuristic') is not None else "N/A"

        self.fig.suptitle(
            f"Grid Size: {self.n}x{self.n} " +
            f"| Algorithm: {info.get('algorithm', 'None')} " +
            f"| Cost: {info.get('cost', 0)} " +
            f"| Runtime: {runtime_str} " +
            f"| Expanded Nodes: {info.get('expanded_nodes', 0)} " +
            f"| Heuristic Value: {heuristic_str}",
            fontsize=14, fontweight='bold')
        self.fig.canvas.draw_idle()

    def set_fog_of_war(self, enabled):
        self.fog_of_war = enabled

    def show(self):
        plt.show()
