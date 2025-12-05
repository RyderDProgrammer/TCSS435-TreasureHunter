import time
import numpy
from Core.bayesian_belief import BayesianBeliefMap
from Core.path_calculator import PathCostCalculator


class BayesianAlgorithmRunner:
    
    

    def __init__(self, grid_instance, use_start2=False, sensor_model=None):
        self.grid = grid_instance
        self.use_start2 = use_start2
        self.sensor_model = sensor_model
        self.solution_path = []
        self.expanded_nodes = 0
        self.heuristic_value = None
        self.pruned_branches = None
        self.current_cost = 0
        self.current_runtime = 0.0
        self.current_algorithm = "None"
        self.total_steps = 0
        self.total_scans = 0

        #bayesian belief tracking
        self.belief_map = None
        self.treasures_found = 0
        self.total_treasures = 0

        #metrics
        self.belief_metrics = {}

    def run_algorithm_with_beliefs(self, algorithm_name, algorithm_func):
        
        #run algorithm with Bayesian belief guidance.
       
        start_time = time.time()

        #reset state
        self.expanded_nodes = 0
        self.solution_path = []
        self.heuristic_value = None
        self.pruned_branches = None
        self.current_algorithm = f"{algorithm_name} (Bayesian)"
        self.total_steps = 0
        self.total_scans = 0
        self.treasures_found = 0

        #reset sensor scan count
        if self.sensor_model:
            self.sensor_model.reset_scan_count()

        #determine start position
        if self.use_start2:
            ai_start = self.grid.start2 if hasattr(self.grid, 'start2') and self.grid.start2 else self.grid.start
        else:
            ai_start = self.grid.start1 if hasattr(self.grid, 'start1') and self.grid.start1 else self.grid.start

        #get total number of treasures
        self.total_treasures = len(self.grid.end)

        #initializ bayesian belief map
        self.belief_map = BayesianBeliefMap(
            grid_size=self.grid.n,
            sensor_model=self.sensor_model,
            num_treasures=self.total_treasures
        )
        self.belief_map.set_grid(self.grid)

        #initialize belief with known walls and start position
        self.belief_map.initialize_beliefs(ai_start, self.grid.walls)

        # --- Heatmap at t = 0 ---
        self.belief_map.print_belief_grid(title = f"Belief at t = 0 scans")

        #perform initial scan around start position
        scan_radius = 2
        self.belief_map.scan_neighborhood_and_update(ai_start, radius=scan_radius)

        #add start to path
        current_pos = ai_start
        self.solution_path.append(current_pos)

        #addup heuristic values
        total_heuristic = 0
        heuristic_count = 0

        #continue until all treasures found
        iteration = 0
        max_iterations = self.grid.n * self.grid.n * 2  #just in case limit

        while self.belief_map.should_continue_search() and iteration < max_iterations:
            iteration += 1

            #get best target based on beliefs
            target = self.belief_map.get_best_target(current_pos)

            if target is None:
                #if no target found scan new cells
                target = self._find_unscanned_cell(current_pos)
                if target is None:
                    break

            #find path to target using algorithm
            result = algorithm_func(self.grid.grid, current_pos, target)
            path, expanded, *extra = result

            if path is None:
                self.belief_map.confirm_empty(target)
                continue

            #track metrics
            self.expanded_nodes += expanded

            if extra:
                total_heuristic += extra[0]
                heuristic_count += 1

            if len(extra) >= 2:
                if self.pruned_branches is None:
                    self.pruned_branches = 0
                self.pruned_branches += extra[1]

            #add path to solution skip first to avoid dupes
            for coord in path[1:]:
                self.solution_path.append(coord)

            #move to target
            current_pos = target

            # Record prediction outcome based on actual grid content
            actual_tile = self.grid.get_tile(target[0], target[1])
            self.belief_map.record_prediction(target, actual_tile)

            #scan around target
            observations = self.belief_map.scan_neighborhood_and_update(target, radius=scan_radius)

            # --- Heatmap after each scan ---
            self.belief_map.print_belief_grid(title = f"Belief after t = {iteration} scans")

            #check found treasure at target
            actual_tile = self.grid.get_tile(target[0], target[1])
            if actual_tile == 'T':
                self.belief_map.confirm_treasure_found(target)
                self.treasures_found += 1
                
                # --- Heatmap at detection ---
                self.belief_map.print_belief_grid(title = f"Belief at detection")

                #stop if all treasures found
                if self.treasures_found >= self.total_treasures:
                    break
            else:
                #not treasure update belief
                self.belief_map.confirm_empty(target)

        #calculate final metrics
        if heuristic_count > 0:
            self.heuristic_value = total_heuristic / heuristic_count

        end_time = time.time()
        self.current_runtime = end_time - start_time
        self.current_cost = PathCostCalculator.calculate_cost(self.solution_path, self.grid.grid)
        self.total_steps = len(self.solution_path) - 1 if len(self.solution_path) > 0 else 0

        if self.sensor_model:
            self.total_scans = self.sensor_model.get_scan_count()

        #get belief metrics
        self.belief_metrics = self.belief_map.get_metrics()

        #print summary
        print(f"Runtime {algorithm_name}: {self.current_runtime:.4f}s")
        print(f"Treasures Found: {self.treasures_found}/{self.total_treasures}")
        print(f"Nodes Expanded: {self.expanded_nodes}")
        print(f"Total Cost: {self.current_cost}")
        print(f"Total Steps: {self.total_steps}")
        print(f"Total Scans: {self.total_scans}")
        print(f"Belief Updates: {self.belief_metrics['belief_updates']}")
        print(f"Final Entropy: {self.belief_metrics['current_entropy']:.4f}")
        print(f"Solution Path: {self.solution_path}")
        print(f"Detection Accuracy: {self.belief_metrics['detection_accuracy']:.3f}")
        print(f"Correct Predictions: {self.belief_metrics['correct_predictions']}/{self.belief_metrics['predictions']}")    
        print(f"Entropy at each detection: {self.belief_metrics['entropy_at_detection']}")
        print(f"Average Entropy at Detection: {self.belief_metrics['avg_entropy_at_detection']:.4f}")



        return {
            'path': self.solution_path,
            'cost': self.current_cost,
            'runtime': self.current_runtime,
            'expanded_nodes': self.expanded_nodes,
            'heuristic': self.heuristic_value,
            'pruned_branches': self.pruned_branches,
            'algorithm': self.current_algorithm,
            'total_steps': self.total_steps,
            'total_scans': self.total_scans,
            'treasures_found': self.treasures_found,
            'total_treasures': self.total_treasures,
            'belief_metrics': self.belief_metrics
        }

    def _find_unscanned_cell(self, current_pos):
        """Find the nearest unscanned cell"""
        min_distance = float('inf')
        nearest_cell = None

        for i in range(self.grid.n):
            for j in range(self.grid.n):
                pos = (i, j)
                if pos not in self.belief_map.observed_cells:
                    if pos not in self.belief_map.confirmed_walls:
                        distance = abs(i - current_pos[0]) + abs(j - current_pos[1])
                        if distance < min_distance:
                            min_distance = distance
                            nearest_cell = pos

        return nearest_cell

    def get_current_state(self):
        """Get current state including belief metrics"""
        state = {
            'algorithm': self.current_algorithm,
            'cost': self.current_cost,
            'runtime': self.current_runtime,
            'expanded_nodes': self.expanded_nodes,
            'heuristic': self.heuristic_value,
            'pruned_branches': self.pruned_branches,
            'total_steps': self.total_steps,
            'total_scans': self.total_scans,
            'treasures_found': self.treasures_found,
            'total_treasures': self.total_treasures
        }

        if self.belief_metrics:
            state['belief_entropy'] = self.belief_metrics.get('current_entropy', 0)
            state['belief_updates'] = self.belief_metrics.get('belief_updates', 0)

        return state

    def reset(self):
        """Reset runner state"""
        self.solution_path = []
        self.expanded_nodes = 0
        self.heuristic_value = None
        self.pruned_branches = None
        self.current_cost = 0
        self.current_runtime = 0.0
        self.current_algorithm = "None"
        self.total_steps = 0
        self.total_scans = 0
        self.treasures_found = 0
        self.total_treasures = 0
        self.belief_map = None
        self.belief_metrics = {}
