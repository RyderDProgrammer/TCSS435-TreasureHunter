import numpy as np
import math


class BayesianBeliefMap:
    #maintains belief distribution over grid cells for treasure locations
    

    def __init__(self, grid_size, sensor_model, num_treasures):
        self.n = grid_size
        self.sensor_model = sensor_model
        self.num_treasures = num_treasures

        #initialize uniform prior belief for each cell
        self.beliefs = np.ones((grid_size, grid_size)) / (grid_size * grid_size)

        #track which cells have been observed
        self.observed_cells = set()

        #track found treasures
        self.found_treasures = set()
        self.confirmed_empty = set()
        self.confirmed_walls = set()
        self.confirmed_traps = set()

        #metrics tracking
        self.entropy_history = []
        self.belief_updates = 0

        #grid reference
        self.grid_instance = None

    def set_grid(self, grid_instance):
        self.grid_instance = grid_instance

    def initialize_beliefs(self, start_pos, walls):
        #wet start position to 0 belief
        self.beliefs[start_pos[0]][start_pos[1]] = 0.0

        #set all wall positions to 0 belief
        for wall in walls:
            self.beliefs[wall[0]][wall[1]] = 0.0
            self.confirmed_walls.add(wall)

        #renormalize after setting known positions
        self._normalize_beliefs()

        #record initial entropy
        self._record_entropy()

    def update_belief(self, position, observation):
    
        # bayes rule :P(T|obs) = P(obs|T) * P(T) / P(obs)
        row, col = position

        #skip if already confirmed
        if position in self.found_treasures:
            return
        if position in self.confirmed_walls:
            return

        #marked as observed
        self.observed_cells.add(position)
        self.belief_updates += 1

        #get noise
        fp_rate = self.sensor_model.false_positive_rate
        fn_rate = self.sensor_model.false_negative_rate

        #prior belief
        prior = self.beliefs[row][col]

        #calculate likelihoods based on observation
        if observation == 'T':
            likelihood_treasure = 1.0 - fn_rate
            likelihood_empty = fp_rate
        elif observation == ' ':
            likelihood_treasure = fn_rate
            likelihood_empty = 1.0 - fp_rate
        elif observation == 'X':
            self.confirmed_traps.add(position)
            self.beliefs[row][col] = 0.0
            self._normalize_beliefs()
            self._record_entropy()
            return
        elif observation == '#':
            self.confirmed_walls.add(position)
            self.beliefs[row][col] = 0.0
            self._normalize_beliefs()
            self._record_entropy()
            return
        else:
            return

        #apply Bayes rule
        p_obs = likelihood_treasure * prior + likelihood_empty * (1.0 - prior)

        if p_obs > 0:
            posterior = (likelihood_treasure * prior) / p_obs
        else:
            posterior = prior

        #update belief
        self.beliefs[row][col] = posterior

        #renormalize to make sure beliefs sum correctly
        self._normalize_beliefs()

        #record entropy
        self._record_entropy()

    def scan_and_update(self, position):
        row, col = position
        observation = self.sensor_model.scan_cell(self.grid_instance, row, col)
        self.update_belief(position, observation)
        return observation

    def scan_neighborhood_and_update(self, position, radius=1):
        observations = {}
        row, col = position

        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                r, c = row + dr, col + dc
                if 0 <= r < self.n and 0 <= c < self.n:
                    obs = self.scan_and_update((r, c))
                    observations[(r, c)] = obs

        return observations

    def confirm_treasure_found(self, position):
        self.found_treasures.add(position)
        self.beliefs[position[0]][position[1]] = 0.0

        #if found all treasures zero out all beliefs
        if len(self.found_treasures) >= self.num_treasures:
            self.beliefs.fill(0.0)
        else:
            self._normalize_beliefs()

        self._record_entropy()

    def confirm_empty(self, position):
        if position not in self.found_treasures and position not in self.confirmed_walls:
            self.confirmed_empty.add(position)
            self.beliefs[position[0]][position[1]] = 0.0
            self._normalize_beliefs()
            self._record_entropy()

    def get_best_target(self, current_pos, exclude_positions=None):
        if exclude_positions is None:
            exclude_positions = set()

        best_target = None
        best_utility = -float('inf')

        for i in range(self.n):
            for j in range(self.n):
                pos = (i, j)

                #skip excluded positions
                if pos in exclude_positions:
                    continue

                #skip confirmed non treasures
                if pos in self.confirmed_empty or pos in self.confirmed_walls or pos in self.confirmed_traps:
                    continue

                #skip already found treasures
                if pos in self.found_treasures:
                    continue

                belief = self.beliefs[i][j]

                #skip cells with low belief
                if belief < 0.0001:
                    continue

                #calculate distance
                distance = math.sqrt((i - current_pos[0])**2 + (j - current_pos[1])**2)
                if distance == 0:
                    distance = 1

                #expect utility being belief weighted by inverse distance
                utility = belief * (1.0 / distance)

                if utility > best_utility:
                    best_utility = utility
                    best_target = pos

        return best_target

    def calculate_entropy(self):
        #calculate entropy  belief distribution
        probs = self.beliefs.flatten()
        probs = probs[probs > 0]

        if len(probs) == 0:
            return 0.0

        entropy = -np.sum(probs * np.log(probs + 1e-10))
        return entropy

    def _normalize_beliefs(self):
        #normalize beliefs to sum to expected number of leftover treasure
        remaining_treasures = self.num_treasures - len(self.found_treasures)

        if remaining_treasures <= 0:
            self.beliefs.fill(0.0)
            return

        total = np.sum(self.beliefs)
        if total > 0:
            self.beliefs = self.beliefs * (remaining_treasures / total)

    def _record_entropy(self):
        entropy = self.calculate_entropy()
        self.entropy_history.append(entropy)

    def get_metrics(self):
        return {
            'current_entropy': self.calculate_entropy(),
            'entropy_history': self.entropy_history.copy(),
            'belief_updates': self.belief_updates,
            'observed_cells': len(self.observed_cells),
            'found_treasures': len(self.found_treasures),
            'treasures_remaining': self.num_treasures - len(self.found_treasures)
        }

    def should_continue_search(self):
        return len(self.found_treasures) < self.num_treasures
