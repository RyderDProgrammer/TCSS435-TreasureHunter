import random

class Grid:
    def __init__(self, n=15):
        self.n = n
        self.grid = []
        self.start = None
        self.end = []  # List of treasure positions
        self.traps = []
        self.walls = []

    def generate_grid(self):
        # Regenerate random counts for traps and treasures
        num_traps = random.randint(2, 3)
        num_treasures = random.randint(3, 5)

        # Initialize empty grid
        self.grid = [[' ' for _ in range(self.n)] for _ in range(self.n)]
        self.end = []
        self.traps = []
        self.walls = []

        # Add treasures
        for i in range(num_treasures):
            while True:
                treasure = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
                if treasure not in self.end:
                    break
            self.grid[treasure[0]][treasure[1]] = 'T'
            self.end.append(treasure)

        # Create starting position
        while True:
            start = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            if start not in self.end:
                self.grid[start[0]][start[1]] = 'S'
                self.start = (start[0], start[1])
                break

        # Create traps
        for i in range(num_traps):
            while True:
                trap = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
                if trap not in self.end and trap != self.start and trap not in self.traps:
                    self.grid[trap[0]][trap[1]] = 'X'
                    self.traps.append(trap)
                    break

        # Create walls
        num_walls = random.randint(int(self.n ** 2 * 0.1), int(self.n ** 2 * 0.15))
        placed = 0
        while placed < num_walls:
            i, j = random.randint(0, self.n - 1), random.randint(0, self.n - 1)
            if self.grid[i][j] == ' ':
                self.grid[i][j] = '#'
                self.walls.append((i, j))
                placed += 1

        return self.grid

    def get_tile(self, row, col):
        if 0 <= row < self.n and 0 <= col < self.n:
            return self.grid[row][col]
        return None

    def is_valid_position(self, row, col):
        return 0 <= row < self.n and 0 <= col < self.n and self.grid[row][col] != '#'
