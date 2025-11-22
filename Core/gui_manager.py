import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from Algorithms.Human import HumanPlayer
from Core.path_walking import PathWalking
from Core.tile_renderer import TileRenderer
from Core.title_formatter import TitleFormatter
from Core.mode_selector import ModeSelector


class GUIManager:
    def __init__(self, grid_size=15):
        self.n = grid_size
        self.fog_of_war = False  # For human mode
        self.player_mode = None  # Will be set by mode selection
        self.human_player = HumanPlayer(grid_size)
        self.current_grid = None
        self.algorithm_executed = False
        self.ai_solution_path = []
        self.ai_full_path = []
        self.ai_step_index = 0
        self.ai_solution_path_p2 = []  # Player 2 AI path
        self.ai_full_path_p2 = []
        self.ai_step_index_p2 = 0
        self.grid_instance = None
        self.last_ai_info = None
        self.path_walking = PathWalking(self)

        # Create figure and main axes
        self.fig = plt.figure(figsize=(12, 10))
        self.fig.canvas.manager.set_window_title("435 GUI")

        # Center window and set to 70% of screen size
        self._setup_window()

        # Main grid axes (adjusted to make room for two title bars)
        self.ax = self.fig.add_axes([0.05, 0.15, 0.9, 0.75])
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
        BUTTON_SPACING = 0.007

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

        # buttons to control alpha-beta pruning max depth
        depth_decrease = self.fig.add_axes([x_pos, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
        self.buttons['decrease_depth'] = Button(depth_decrease, 'Depth -')
        self.buttons['decrease_depth'].on_clicked(callbacks.get('decrease_depth'))
        x_pos += BUTTON_WIDTH_SMALL + BUTTON_SPACING

        depth_increase = self.fig.add_axes([x_pos, BUTTON_Y, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT])
        self.buttons['increase_depth'] = Button(depth_increase, 'Depth +')
        self.buttons['increase_depth'].on_clicked(callbacks.get('increase_depth'))
        x_pos += BUTTON_WIDTH_SMALL + BUTTON_SPACING

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
                display_val, color, fg = TileRenderer.get_tile_appearance(
                    val, i, j, self.grid_instance, self.fog_of_war,
                    self.human_player, self.ai_solution_path, self.ai_solution_path_p2
                )

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

    def _update_ai_path_state(self, solution_path, solution_path_p2=None):
        if solution_path is not None and len(solution_path) > 0:
            self.ai_full_path = solution_path
            if self.fog_of_war:
                self.ai_step_index = 1
                self.ai_solution_path = solution_path[:2] if len(solution_path) > 1 else solution_path
            elif self.player_mode == 'ai':
                # AI vs AI mode: start with empty paths, animation will fill them
                self.ai_step_index = -1
                self.ai_solution_path = []
            else:
                self.ai_step_index = 1
                self.ai_solution_path = solution_path
        elif not solution_path:
            self.ai_solution_path = []

        # Handle Player 2 path (AI vs AI mode)
        if solution_path_p2 is not None and len(solution_path_p2) > 0:
            self.ai_full_path_p2 = solution_path_p2
            # AI vs AI mode: start with empty path, animation will fill it
            self.ai_step_index_p2 = -1
            self.ai_solution_path_p2 = []
        elif solution_path_p2 is not None:
            self.ai_solution_path_p2 = []

        if self.player_mode == 'ai' and solution_path_p2 is not None:
            self.path_walking.start()

    def _update_human_player_state(self, grid, solution_path):
        if solution_path is None or len(solution_path) == 0:
            if len(self.human_player.current_path) == 0:
                self.human_player.reset()
                self.human_player.set_grid(grid, self.grid_instance)

                if self.fog_of_war:
                    self.human_player.reveal_initial_tiles(self.grid_instance)
            else:
                self.human_player.set_grid(grid, self.grid_instance)
        else:
            self.human_player.set_grid(grid, self.grid_instance)

    def render_grid(self, grid, solution_path=None, grid_instance=None, solution_path_p2=None):
        self.current_grid = grid
        if grid_instance:
            self.grid_instance = grid_instance
        self._update_ai_path_state(solution_path, solution_path_p2)
        self._update_human_player_state(grid, solution_path)
        # Skip initial draw in AI vs AI mode - animation will handle it
        if not (self.player_mode == 'ai' and solution_path_p2 is not None):
            self._clear_and_setup_axes()
            self._draw_grid_tiles()
            self.fig.canvas.draw_idle()

    def update_title(self, info, player2_info=None):
        if info.get('algorithm') not in ['Human', 'None']:
            self.last_ai_info = info

        ai_info = self.last_ai_info if self.last_ai_info else info
        title = TitleFormatter.format_dual_title(ai_info, player2_info, self.player_mode, self.human_player.human_cost)
        self.fig.suptitle(title, fontsize=12, fontweight='bold', y=0.98)
        self.fig.canvas.draw_idle()

    def set_fog_of_war(self, enabled):
        self.fog_of_war = enabled

    def mark_algorithm_executed(self):
        self.algorithm_executed = True

    def reset_for_new_grid(self):
        self.algorithm_executed = False
        self.ai_solution_path = []
        self.ai_full_path = []
        self.ai_step_index = 0
        self.ai_solution_path_p2 = []
        self.ai_full_path_p2 = []
        self.ai_step_index_p2 = 0
        self.last_ai_info = None
        self.path_walking.stop()
        self.human_player.reset()
        if self.fog_of_war:
            # Re-reveal initial tiles for human mode
            if self.current_grid:
                self.human_player.set_grid(self.current_grid, self.grid_instance)
                self.human_player.reveal_initial_tiles(self.grid_instance)

    def _on_click(self, event):
        if event.inaxes != self.ax:
            return

        if not self.algorithm_executed:
            return

        # AI vs AI mode: animation handles advancement automatically
        if self.player_mode == 'ai':
            return

        # Human vs AI mode: fog of war enabled, click on specific tiles
        if not self.fog_of_war:
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
        mode_selector = ModeSelector(self.fig, self.ax)

        def on_mode_selected(player_mode, fog_of_war):
            self.player_mode = player_mode
            self.fog_of_war = fog_of_war
            on_selection_callback()

        mode_selector.show_selection(on_mode_selected)

    def show(self):
        plt.show()
