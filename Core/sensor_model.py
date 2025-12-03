import random


class SensorModel:

    # Noise level configurations
    NOISE_LEVELS = {
        'none': {'false_positive': 0.0, 'false_negative': 0.0},
        'low': {'false_positive': 0.02, 'false_negative': 0.05},
        'medium': {'false_positive': 0.08, 'false_negative': 0.15},
        'high': {'false_positive': 0.15, 'false_negative': 0.30}
    }

    def __init__(self, noise_level='none'):
        self.noise_level = noise_level
        self.set_noise_level(noise_level)
        self.cached_observations = {}  # Cache noisy observations to prevent flickering
        self.cache_valid = False
        self.scan_count = 0  # Track number of scans performed

    def set_noise_level(self, noise_level):
        if noise_level not in self.NOISE_LEVELS:
            noise_level = 'none'

        self.noise_level = noise_level
        config = self.NOISE_LEVELS[noise_level]
        self.false_positive_rate = config['false_positive']
        self.false_negative_rate = config['false_negative']
        self.invalidate_cache()

    def invalidate_cache(self):
        self.cached_observations = {}
        self.cache_valid = False
        self.scan_count = 0  # Reset scan count

    def scan_cell_cached(self, grid_instance, row, col):
        cache_key = (row, col)
        if cache_key not in self.cached_observations:
            # Get the actual tile value first
            actual_value = grid_instance.get_tile(row, col)

            # Return None for out-of-bounds positions
            if actual_value is None:
                return None

            # Increment scan count
            self.scan_count += 1

            # No noise for walls and start positions - these are always visible correctly
            if actual_value in ['#', 'S']:
                self.cached_observations[cache_key] = actual_value
            else:
                self.cached_observations[cache_key] = self._apply_noise(actual_value)

        return self.cached_observations[cache_key]

    def scan_cell(self, grid_instance, row, col):
        # Get the actual tile value first
        actual_value = grid_instance.get_tile(row, col)

        # Return None for out-of-bounds positions
        if actual_value is None:
            return None

        # Increment scan count
        self.scan_count += 1

        # No noise for walls and start positions - these are always visible correctly
        if actual_value in ['#', 'S']:
            return actual_value

        return self._apply_noise(actual_value)

    def scan_neighborhood(self, grid_instance, row, col, radius=1):
        observations = {}

        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                r, c = row + dr, col + dc
                if 0 <= r < grid_instance.n and 0 <= c < grid_instance.n:
                    observations[(r, c)] = self.scan_cell(grid_instance, r, c)

        return observations

    def _apply_noise(self, actual_value):
        if self.noise_level == 'none':
            return actual_value

        # False negative: treasure/trap appears as empty
        if actual_value in ['T', 'X']:
            if random.random() < self.false_negative_rate:
                return ' '

        # False positive: empty space appears as treasure
        if actual_value == ' ':
            if random.random() < self.false_positive_rate:
                # Randomly choose between treasure or trap
                return 'T' if random.random() < 0.7 else 'X'

        return actual_value

    def get_noisy_grid_view(self, grid_instance, revealed_positions=None):
        noisy_view = {}

        if revealed_positions is None:
            # Scan entire grid
            for i in range(grid_instance.n):
                for j in range(grid_instance.n):
                    noisy_view[(i, j)] = self.scan_cell(grid_instance, i, j)
        else:
            # Scan only revealed positions
            for pos in revealed_positions:
                i, j = pos
                noisy_view[(i, j)] = self.scan_cell(grid_instance, i, j)

        return noisy_view

    def create_noisy_grid(self, grid_instance):
        n = grid_instance.n
        noisy_grid = [[' ' for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                noisy_grid[i][j] = self.scan_cell_cached(grid_instance, i, j)

        return noisy_grid

    def get_scan_count(self):
        return self.scan_count

    def reset_scan_count(self):
        self.scan_count = 0
