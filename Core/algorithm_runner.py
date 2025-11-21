import time
from Core.treasure_sorter import TreasureSorter
from Core.path_calculator import PathCostCalculator


class AlgorithmRunner:
    def __init__(self, grid_instance, use_start2=False):
        self.grid = grid_instance
        self.use_start2 = use_start2  # If True, use start2 instead of start1
        self.solution_path = []
        self.expanded_nodes = 0
        self.heuristic_value = None
        self.current_cost = 0
        self.current_runtime = 0.0
        self.current_algorithm = "None"

    def run_algorithm(self, algorithm_name, algorithm_func):
        start_time = time.time()

        self.expanded_nodes = 0
        self.solution_path = []
        self.heuristic_value = None
        self.current_algorithm = algorithm_name

        if self.use_start2:
            ai_start = self.grid.start2 if hasattr(self.grid, 'start2') and self.grid.start2 else self.grid.start
        else:
            ai_start = self.grid.start1 if hasattr(self.grid, 'start1') and self.grid.start1 else self.grid.start

        sorted_treasures = TreasureSorter.sort_by_distance(self.grid.end, ai_start)

        # Perform searches to each treasure in order
        start = ai_start
        total_heuristic = 0
        heuristic_count = 0

        for treasure in sorted_treasures:
            result = algorithm_func(self.grid.grid, start, treasure)
            path, expanded, *heuristic = result

            if path is None:
                print(f"Unreachable Treasure")
                continue

            if heuristic:
                total_heuristic += heuristic[0]
                heuristic_count += 1

            self.expanded_nodes += expanded

            # Skip first element of sub-paths to avoid duplicates
            if self.solution_path:  # If this is not the first path
                for coord in path[1:]:  # Skip path[0] since already in solution path
                    self.solution_path.append(coord)
            else:  # First path - include everything
                for coord in path:
                    self.solution_path.append(coord)

            start = treasure

        if heuristic_count > 0:
            self.heuristic_value = total_heuristic / heuristic_count

        end_time = time.time()
        self.current_runtime = end_time - start_time
        self.current_cost = PathCostCalculator.calculate_cost(self.solution_path, self.grid.grid)

        print(f"Runtime {algorithm_name}: {self.current_runtime:.4f}s")
        print(f"Nodes Expanded: {self.expanded_nodes}")
        print(f"Total Cost: {self.current_cost}")
        print(f"Solution Path: {self.solution_path}")

        return {
            'path': self.solution_path,
            'cost': self.current_cost,
            'runtime': self.current_runtime,
            'expanded_nodes': self.expanded_nodes,
            'heuristic': self.heuristic_value,
            'algorithm': self.current_algorithm
        }

    def get_current_state(self):
        return {
            'algorithm': self.current_algorithm,
            'cost': self.current_cost,
            'runtime': self.current_runtime,
            'expanded_nodes': self.expanded_nodes,
            'heuristic': self.heuristic_value
        }

    def reset(self):
        self.solution_path = []
        self.expanded_nodes = 0
        self.heuristic_value = None
        self.current_cost = 0
        self.current_runtime = 0.0
        self.current_algorithm = "None"
