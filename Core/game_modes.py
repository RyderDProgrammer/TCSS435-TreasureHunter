
class GameMode:

    def __init__(self, grid, gui_manager, algorithm_runner):
        self.grid = grid
        self.gui_manager = gui_manager
        self.algorithm_runner = algorithm_runner

    def start(self):
        raise NotImplementedError("Subclasses must implement start()")


class SinglePlayerMode(GameMode):

    def start(self):
        # This is the current mode - no special setup needed
        pass


class AIvsAIMode(GameMode):

    def __init__(self, grid, gui_manager, algorithm_runner):
        super().__init__(grid, gui_manager, algorithm_runner)
        self.player1_algorithm = None
        self.player2_algorithm = None
        self.current_player = 1

    def set_algorithms(self, player1_algo, player2_algo):
        self.player1_algorithm = player1_algo
        self.player2_algorithm = player2_algo

    def start(self):
        # TODO: Implement turn-based AI vs AI gameplay
        pass

    def take_turn(self):
        # TODO: Implement turn logic
        pass


class HumanvsAIMode(GameMode):

    def __init__(self, grid, gui_manager, algorithm_runner):
        super().__init__(grid, gui_manager, algorithm_runner)
        self.ai_algorithm = None
        self.current_player = 'human'  # 'human' or 'ai'

    def set_ai_algorithm(self, algorithm):
        self.ai_algorithm = algorithm

    def start(self):
        # Enable fog of war for human player
        self.gui_manager.set_fog_of_war(True)
        # TODO: Implement turn-based Human vs AI gameplay
        pass

    def take_turn(self):
        # TODO: Implement turn logic
        # - Human turn: manual movement/input
        # - AI turn: run algorithm
        pass
