import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from Algorithms.Human import HumanPlayer


class GUIManager:
    def __init__(self, grid_size=15):
        self.n = grid_size
        self.fog_of_war = False  # For human mode
        self.player_mode = None  # Will be set by mode selection
        self.mode_selected = False
        self.human_player = HumanPlayer(grid_size)
        self.current_grid = None
        self.algorithm_executed = False
        self.ai_solution_path = []
        self.ai_full_path = []
        self.ai_step_index = 0

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

        # Connect click event
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)

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

    def _draw_grid_tiles(self):
        for i in range(self.n):
            for j in range(self.n):
                val = self.current_grid[i][j]
                display_val, color, fg = self._get_tile_appearance(val, i, j, self.human_player.current_path, self.ai_solution_path)

                rect = patches.Rectangle((j, self.n - i - 1), 1, 1,
                                        facecolor=color, edgecolor='black', linewidth=1.3)
                self.ax.add_patch(rect)

                if display_val.strip():
                    self.ax.text(j + 0.5, self.n - i - 0.5, display_val, ha='center', va='center',
                               color=fg, fontsize=max(10, 180 // self.n), fontweight='bold')

    def _clear_and_setup_axes(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.axis("off")

    def _redraw_grid(self):
        self._clear_and_setup_axes()
        self._draw_grid_tiles()
        self.fig.canvas.draw_idle()

    def _update_ai_path_state(self, solution_path):
        if solution_path is not None and len(solution_path) > 0:
            self.ai_full_path = solution_path
            self.ai_step_index = 1
            if self.fog_of_war:
                self.ai_solution_path = solution_path[:2] if len(solution_path) > 1 else solution_path
            else:
                self.ai_solution_path = solution_path
        elif not solution_path:
            self.ai_solution_path = []

    def _update_human_player_state(self, grid, solution_path):
        if solution_path is None or len(solution_path) == 0:
            if len(self.human_player.current_path) == 0:
                self.human_player.reset()
                self.human_player.set_grid(grid)

                if self.fog_of_war:
                    self.human_player.reveal_initial_tiles(grid)
            else:
                self.human_player.set_grid(grid)
        else:
            self.human_player.set_grid(grid)

    def render_grid(self, grid, solution_path=None):
        self.current_grid = grid
        self._update_ai_path_state(solution_path)
        self._update_human_player_state(grid, solution_path)
        self._clear_and_setup_axes()
        self._draw_grid_tiles()
        self.fig.canvas.draw_idle()

    def update_title(self, info):
        runtime_str = f"{info.get('runtime', 0):.4f}s" if info.get('runtime', 0) > 0 else "N/A"
        heuristic_str = f"{info.get('heuristic'):.2f}" if info.get('heuristic') is not None else "N/A"

        if self.player_mode == 'human':
            cost_display = self.human_player.human_cost
        else:
            cost_display = info.get('cost', 0)

        self.fig.suptitle(
            f"Grid Size: {self.n}x{self.n} " +
            f"| Algorithm: {info.get('algorithm', 'None')} " +
            f"| Cost: {cost_display} " +
            f"| Runtime: {runtime_str} " +
            f"| Expanded Nodes: {info.get('expanded_nodes', 0)} " +
            f"| Heuristic Value: {heuristic_str}",
            fontsize=14, fontweight='bold')
        self.fig.canvas.draw_idle()

    def set_fog_of_war(self, enabled):
        self.fog_of_war = enabled

    def mark_algorithm_executed(self):
        self.algorithm_executed = True

    def _get_tile_appearance(self, val, i, j, human_path, ai_path):
        is_on_ai_path = ai_path and (i, j) in ai_path
        is_on_human_path = human_path and (i, j) in human_path

        if self.fog_of_war and val not in ['S'] and (i, j) not in self.human_player.revealed_tiles:
            if is_on_ai_path:
                return val, '#3544CA', 'white' if val in ['T', 'X', '#'] else 'black'
            return '?', 'lightgray', 'black'

        display_val = val
        color = {'T': 'gold', 'X': 'red', '#': 'gray', 'S': 'blue'}.get(val, 'white')
        fg = 'white' if val in ['T', 'X', '#'] else 'black'

        if is_on_human_path and is_on_ai_path:
            color = self._get_mixed_path_color(val)
        elif is_on_human_path:
            color = self._get_path_color(val, is_human=True)
        elif is_on_ai_path:
            color = self._get_path_color(val, is_human=False)

        return display_val, color, fg

    def _get_mixed_path_color(self, tile_val):
        if tile_val == 'X':
            return 'cyan'
        elif tile_val == 'T':
            return 'green'
        elif tile_val not in ['S']:
            return '#5B6FC9'
        return 'blue'

    def _get_path_color(self, tile_val, is_human=False):
        if tile_val == 'X':
            return 'cyan'
        elif tile_val == 'T':
            if is_human:
                return 'green'
            else:
                return '#3544CA'
        elif tile_val not in ['S']:
            if is_human:
                return 'lightblue'
            else:
                return '#3544CA'
        return 'blue'

    def _on_click(self, event):
        if not self.fog_of_war or event.inaxes != self.ax:
            return

        if not self.algorithm_executed:
            return

        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        col = int(x)
        row = self.n - int(y) - 1

        if 0 <= row < self.n and 0 <= col < self.n:
            if self.human_player.handle_tile_click(row, col):
                self.ai_step_index += 1
                if self.ai_step_index < len(self.ai_full_path):
                    self.ai_solution_path = self.ai_full_path[:self.ai_step_index + 1]

                self._redraw_grid()
                self.update_title(self.human_player.get_state())

    def show_mode_selection(self, on_selection_callback):
        # Clear the main axes and display the question
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis("off")

        # Display question text
        self.ax.text(5, 7, 'Select Player Mode',
                    ha='center', va='center',
                    fontsize=24, fontweight='bold')

        # Create Human button
        self.ax_human = self.fig.add_axes([0.25, 0.4, 0.2, 0.1])
        self.btn_human = Button(self.ax_human, 'Human', color='lightblue', hovercolor='#3544CA')

        # Create AI button
        self.ax_ai = self.fig.add_axes([0.55, 0.4, 0.2, 0.1])
        self.btn_ai = Button(self.ax_ai, 'AI', color='#3544CA', hovercolor='#CABB35')

        def on_human_click(event):
            human_or_ai('human', True)

        def on_ai_click(event):
            human_or_ai('ai', False)

        def human_or_ai(player_mode, fog_of_war):
            self.player_mode = player_mode
            self.fog_of_war = fog_of_war
            self.mode_selected = True
            # Disconnect button events before removing
            self.btn_human.disconnect_events()
            self.btn_ai.disconnect_events()
            self.ax_human.remove()
            self.ax_ai.remove()
            on_selection_callback()
            self.fig.canvas.draw_idle()
        
        self.btn_human.on_clicked(on_human_click)
        self.btn_ai.on_clicked(on_ai_click)

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()
