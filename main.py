from Core import Grid, GUIManager, AlgorithmRunner
from Algorithms import BFS, DFS, UCS, A_Star, Greedy_BFS, MiniMax, Alpha_Beta


class TreasureHunterGame:
    def __init__(self):
        # Initialize core components
        self.grid = Grid(n=15)
        self.gui = GUIManager(grid_size=15)
        self.algorithm_runner = AlgorithmRunner(self.grid)  # Player 1
        self.algorithm_runner_p2 = AlgorithmRunner(self.grid, use_start2=True)  # Player 2

        # Show mode selection dialog first
        self.gui.show_mode_selection(self.on_mode_selected)

        # Start the game
        self.gui.show()

    def on_mode_selected(self):
        # Setup GUI buttons with callbacks after mode is selected
        self._setup_callbacks()

        # Generate initial grid after mode is selected
        self.create_grid()

    def _setup_callbacks(self):
        callbacks = {
            'decrease': self.decrease_size,
            'increase': self.increase_size,
            'bfs': self.do_BFS,
            'dfs': self.do_DFS,
            'ucs': self.do_UCS,
            'a_star': self.do_A_Star,
            'greedy': self.do_Greedy_BFS,
            'minimax': self.do_MiniMax,
            'alpha_beta': self.do_Alpha_Beta,
            'new_grid': self.create_grid,
            'increase_depth': self.increase_depth,
            'decrease_depth': self.decrease_depth,
            'switch_mode': self.switch_mode
        }
        self.gui.create_buttons(callbacks)

    def create_grid(self, event=None):
        self.grid.generate_grid()
        self.algorithm_runner.reset()
        self.algorithm_runner_p2.reset()
        self.gui.n = self.grid.n
        self.gui.reset_for_new_grid()
        self.gui.render_grid(self.grid.grid, grid_instance=self.grid)
        # In AI vs AI mode, pass both player states
        if self.gui.player_mode == 'ai':
            self.gui.update_title(self.algorithm_runner.get_current_state(),
                                 self.algorithm_runner_p2.get_current_state())
        else:
            self.gui.update_title(self.algorithm_runner.get_current_state())

    def increase_size(self, event):
        self.grid.n += 1
        self.create_grid()

    def decrease_size(self, event):
        if self.grid.n > 8:
            self.grid.n -= 1
            self.create_grid()

    # Configure MAX_DEPTH for alpha-beta pruning
    def increase_depth(self, event):
        Alpha_Beta.MAX_DEPTH += 1

    def decrease_depth(self, event):
        Alpha_Beta.MAX_DEPTH -= 1

    def switch_mode(self, event=None):
        # Toggle between 'ai' and 'human' modes
        if self.gui.player_mode == 'ai':
            self.gui.player_mode = 'human'
            self.gui.fog_of_war = True
        else:
            self.gui.player_mode = 'ai'
            self.gui.fog_of_war = False
        # Reset and regenerate grid for new mode
        self.create_grid()

    # Algorithm execution methods
    def do_BFS(self, event=None):
        self.algorithm_helper('BFS', BFS.BFS)

    def do_DFS(self, event=None):
        self.algorithm_helper('DFS', DFS.DFS)

    def do_UCS(self, event=None):
        self.algorithm_helper('UCS', UCS.UCS)

    def do_A_Star(self, event=None):
        self.algorithm_helper('A*', A_Star.A_Star)

    def do_Greedy_BFS(self, event=None):
        self.algorithm_helper('Greedy BFS', Greedy_BFS.Greedy_BFS)

    def do_MiniMax(self, event=None):
        self.algorithm_helper('MiniMax', MiniMax.MiniMax)

    def do_Alpha_Beta(self, event=None):
        self.algorithm_helper('Alpha-Beta', Alpha_Beta.Alpha_Beta)

    def algorithm_helper(self, algorithm_name, algorithm_func):
        if self.gui.player_mode == 'human' and self.gui.algorithm_executed:
            # Reset AI and fog of war, but keep the same grid
            self.algorithm_runner.reset()
            self.gui.reset_for_new_grid()

        # Run algorithm for Player 1
        result = self.algorithm_runner.run_algorithm(algorithm_name, algorithm_func)
        self.gui.mark_algorithm_executed()

        # In AI vs AI mode, also run for Player 2
        if self.gui.player_mode == 'ai':
            result_p2 = self.algorithm_runner_p2.run_algorithm(algorithm_name, algorithm_func)
            self.gui.render_grid(self.grid.grid, result['path'], grid_instance=self.grid, solution_path_p2=result_p2['path'])
            self.gui.update_title(result, result_p2)
        else:
            self.gui.render_grid(self.grid.grid, result['path'], grid_instance=self.grid)
            self.gui.update_title(result)

if __name__ == "__main__":
    TreasureHunterGame()