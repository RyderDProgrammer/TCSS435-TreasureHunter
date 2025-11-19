from Core import Grid, GUIManager, AlgorithmRunner, SinglePlayerMode
from Algorithms import BFS, DFS, UCS, A_Star, Greedy_BFS, MiniMax, Alpha_Beta


class TreasureHunterGame:
    def __init__(self):
        # Initialize core components
        self.grid = Grid(n=15)
        self.gui = GUIManager(grid_size=15)
        self.algorithm_runner = AlgorithmRunner(self.grid)
        self.game_mode = SinglePlayerMode(self.grid, self.gui, self.algorithm_runner)

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
            'new_grid': self.create_grid
        }
        self.gui.create_buttons(callbacks)

    def create_grid(self, event=None):
        self.grid.generate_grid()
        self.algorithm_runner.reset()
        self.gui.n = self.grid.n
        self.gui.reset_for_new_grid()
        self.gui.render_grid(self.grid.grid)
        self.gui.update_title(self.algorithm_runner.get_current_state())

    def increase_size(self, event):
        self.grid.n += 1
        self.create_grid()

    def decrease_size(self, event):
        if self.grid.n > 8:
            self.grid.n -= 1
            self.create_grid()

    # Algorithm execution methods
    def do_BFS(self, event=None):
        result = self.algorithm_runner.run_algorithm('BFS', BFS.BFS)
        self.algorithm_helper(result)

    def do_DFS(self, event=None):
        result = self.algorithm_runner.run_algorithm('DFS', DFS.DFS)
        self.algorithm_helper(result)

    def do_UCS(self, event=None):
        result = self.algorithm_runner.run_algorithm('UCS', UCS.UCS)
        self.algorithm_helper(result)

    def do_A_Star(self, event=None):
        result = self.algorithm_runner.run_algorithm('A*', A_Star.A_Star)
        self.algorithm_helper(result)

    def do_Greedy_BFS(self, event=None):
        result = self.algorithm_runner.run_algorithm('Greedy BFS', Greedy_BFS.Greedy_BFS)
        self.algorithm_helper(result)

    def do_MiniMax(self, event=None):
        result = self.algorithm_runner.run_algorithm('MiniMax', MiniMax.MiniMax)
        self.algorithm_helper(result)

    def do_Alpha_Beta(self, event=None):
        result = self.algorithm_runner.run_algorithm('Alpha-Beta', Alpha_Beta.Alpha_Beta)
        self.algorithm_helper(result)
        
    def algorithm_helper(self, result):
        self.gui.mark_algorithm_executed()
        self.gui.render_grid(self.grid.grid, result['path'])
        self.gui.update_title(result)

if __name__ == "__main__":
    TreasureHunterGame()