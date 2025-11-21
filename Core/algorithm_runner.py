import time
import math
import numpy

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

        # Use start1 for Player 1 or start2 for Player 2 depending on configuration
        if self.use_start2:
            ai_start = self.grid.start2 if hasattr(self.grid, 'start2') and self.grid.start2 else self.grid.start
        else:
            ai_start = self.grid.start1 if hasattr(self.grid, 'start1') and self.grid.start1 else self.grid.start

        # Use dictionary and Euclidean distance to find closest treasures
        treasure_distances = {}
        for treasure in self.grid.end:
            distance = math.sqrt(
                (treasure[0] - ai_start[0]) ** 2 +
                (treasure[1] - ai_start[1]) ** 2
            )
            treasure_distances[treasure] = distance

        # Sort treasures by distance
        keys = list(treasure_distances.keys())
        values = list(treasure_distances.values())
        sorted_indices = numpy.argsort(values)
        sorted_treasures = {keys[i]: values[i] for i in sorted_indices}

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

        # Calculate cost
        self.current_cost = self._calculate_path_cost()

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

    def _calculate_path_cost(self):
        if not self.solution_path:
            return 0

        total_cost = 0
        for i, (row, col) in enumerate(self.solution_path):
            if i == 0:  # Skip start position
                continue

            tile = self.grid.grid[row][col]
            if tile in ['S', 'T']:  # Starting positions or Treasure
                total_cost += 0
            elif tile == 'X':  # Trap
                total_cost += 5
            else:  # Regular tile
                total_cost += 1

        return total_cost

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
