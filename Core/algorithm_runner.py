import time
from Core.treasure_sorter import TreasureSorter
from Core.path_calculator import PathCostCalculator


class AlgorithmRunner:
    def __init__(self, grid_instance, use_start2=False, sensor_model=None):
        self.grid = grid_instance
        self.use_start2 = use_start2  # If True, use start2 instead of start1
        self.sensor_model = sensor_model  # For noisy observations
        self.solution_path = []
        self.expanded_nodes = 0
        self.heuristic_value = None
        self.pruned_branches = None
        self.current_cost = 0
        self.current_runtime = 0.0
        self.current_algorithm = "None"
        self.total_steps = 0  # Total steps in the solution path
        self.total_scans = 0  # Total scans performed

    def run_algorithm(self, algorithm_name, algorithm_func):
        start_time = time.time()

        self.expanded_nodes = 0
        self.solution_path = []
        self.heuristic_value = None
        self.pruned_branches = None
        self.current_algorithm = algorithm_name
        self.total_steps = 0
        self.total_scans = 0

        # Reset sensor scan count if sensor model exists
        if self.sensor_model:
            self.sensor_model.reset_scan_count()

        if self.use_start2:
            ai_start = self.grid.start2 if hasattr(self.grid, 'start2') and self.grid.start2 else self.grid.start
        else:
            ai_start = self.grid.start1 if hasattr(self.grid, 'start1') and self.grid.start1 else self.grid.start

        # Always search for all known treasures
        sorted_treasures = TreasureSorter.sort_by_distance(self.grid.end, ai_start)

        # If sensor model exists, perform initial scan around start position
        if self.sensor_model:
            scan_radius = 3
            self.sensor_model.scan_neighborhood(self.grid, ai_start[0], ai_start[1], radius=scan_radius)

        # Perform searches to each treasure in order
        start = ai_start
        total_heuristic = 0
        heuristic_count = 0

        for treasure in sorted_treasures:
            result = algorithm_func(self.grid.grid, start, treasure)
            path, expanded, *extra = result

            if path is None:
                print(f"Unreachable Treasure")
                continue

            # Handle heuristic (3rd return value)
            if extra:
                total_heuristic += extra[0]
                heuristic_count += 1

            # Handle pruned_branches (4th return value, only for Alpha-Beta)
            if len(extra) >= 2:
                if self.pruned_branches is None:
                    self.pruned_branches = 0
                self.pruned_branches += extra[1]

            self.expanded_nodes += expanded

            # Skip first element of sub-paths to avoid duplicates
            if self.solution_path:  # If this is not the first path
                for coord in path[1:]:  # Skip path[0] since already in solution path
                    self.solution_path.append(coord)
            else:  # First path - include everything
                for coord in path:
                    self.solution_path.append(coord)

            # If sensor model exists, scan around the treasure we just reached
            if self.sensor_model:
                self.sensor_model.scan_neighborhood(self.grid, treasure[0], treasure[1], radius=scan_radius)

            start = treasure

        if heuristic_count > 0:
            self.heuristic_value = total_heuristic / heuristic_count

        end_time = time.time()
        self.current_runtime = end_time - start_time
        self.current_cost = PathCostCalculator.calculate_cost(self.solution_path, self.grid.grid)

        # Calculate total steps (length of solution path minus 1, since path includes start position)
        self.total_steps = len(self.solution_path) - 1 if len(self.solution_path) > 0 else 0

        # Get total scans from sensor model
        if self.sensor_model:
            self.total_scans = self.sensor_model.get_scan_count()

        print(f"Runtime {algorithm_name}: {self.current_runtime:.4f}s")
        print(f"Nodes Expanded: {self.expanded_nodes}")
        print(f"Total Cost: {self.current_cost}")
        print(f"Total Steps: {self.total_steps}")
        print(f"Total Scans: {self.total_scans}")
        print(f"Solution Path: {self.solution_path}")

        return {
            'path': self.solution_path,
            'cost': self.current_cost,
            'runtime': self.current_runtime,
            'expanded_nodes': self.expanded_nodes,
            'heuristic': self.heuristic_value,
            'pruned_branches': self.pruned_branches,
            'algorithm': self.current_algorithm,
            'total_steps': self.total_steps,
            'total_scans': self.total_scans
        }

    def get_current_state(self):
        return {
            'algorithm': self.current_algorithm,
            'cost': self.current_cost,
            'runtime': self.current_runtime,
            'expanded_nodes': self.expanded_nodes,
            'heuristic': self.heuristic_value,
            'pruned_branches': self.pruned_branches,
            'total_steps': self.total_steps,
            'total_scans': self.total_scans
        }

    def reset(self):
        self.solution_path = []
        self.expanded_nodes = 0
        self.heuristic_value = None
        self.pruned_branches = None
        self.current_cost = 0
        self.current_runtime = 0.0
        self.current_algorithm = "None"
        self.total_steps = 0
        self.total_scans = 0
