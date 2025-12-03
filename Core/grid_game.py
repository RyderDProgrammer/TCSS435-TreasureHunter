import random

class Grid:
    def __init__(self, n=20):
        self.n = n
        self.grid = []
        self.start = None
        self.start1 = None  # Player 1 starting position (AI or first player)
        self.start2 = None  # Player 2 starting position (Human or second player)
        self.end = []  # List of treasure positions
        self.traps = []
        self.walls = []

    def generate_grid(self):
        # Regenerate random counts for traps and treasures
        num_traps = random.randint(2, 3)
        num_treasures = random.randint(2, 4)

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

        # Create Start 1 position (Player 1 / AI)
        while True:
            start1 = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            if start1 not in self.end:
                self.grid[start1[0]][start1[1]] = 'S'
                self.start1 = (start1[0], start1[1])
                self.start = self.start1
                break

        # Create Start 2 position (Player 2 / Human)
        while True:
            start2 = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
            if start2 not in self.end and start2 != self.start1:
                self.grid[start2[0]][start2[1]] = 'S'
                self.start2 = (start2[0], start2[1])
                break

        # Create traps
        for i in range(num_traps):
            while True:
                trap = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
                if trap not in self.end and trap != self.start1 and trap != self.start2 and trap not in self.traps:
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
