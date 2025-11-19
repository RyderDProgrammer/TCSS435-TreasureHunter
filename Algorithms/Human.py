class HumanPlayer:
    def __init__(self, grid_size):
        self.n = grid_size
        self.revealed_tiles = set()
        self.stepped_on_tiles = set()  # Tiles the player has actually stepped on
        self.current_path = []
        self.current_grid = None
        self.all_treasures_found = False
        self.human_cost = 0

    def reset(self):
        self.all_treasures_found = False
        self.revealed_tiles.clear()
        self.stepped_on_tiles.clear()
        self.human_cost = 0
        self.current_path = []

    def set_grid(self, grid):
        self.current_grid = grid
        if grid is not None:
            self.n = len(grid)

    def reveal_initial_tiles(self, grid):
        for i in range(self.n):
            for j in range(self.n):
                if grid[i][j] == 'S':
                    self.stepped_on_tiles.add((i, j))
                    self._reveal_adjacent_tiles(i, j)
                    break

    def handle_tile_click(self, row, col):
        if self.all_treasures_found:
            return False

        if not self.current_grid:
            return False

        if self.current_grid[row][col] == '#':
            if self._is_adjacent_to_path(row, col):
                self.revealed_tiles.add((row, col))
                return True
            return False

        if self._is_adjacent_to_path(row, col):
            self.revealed_tiles.add((row, col))
            if (row, col) not in self.current_path and self.current_grid[row][col] != '#':
                self.current_path.append((row, col))
                self.stepped_on_tiles.add((row, col))  # Mark this tile as stepped on
                self._calculate_human_cost(row, col)
                self._reveal_adjacent_tiles(row, col)

            self._check_all_treasures_found()
            return True

        return False

    def _calculate_human_cost(self, row, col):
        tile = self.current_grid[row][col]
        if tile in ['S', 'T']:
            cost = 0
        elif tile == 'X':
            cost = 5
        else:
            cost = 1
        self.human_cost += cost

    def _reveal_adjacent_tiles(self, row, col):
        adjacent_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in adjacent_offsets:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < self.n and 0 <= adj_col < self.n:
                self.revealed_tiles.add((adj_row, adj_col))

    def _check_all_treasures_found(self):
        if not self.current_grid:
            return

        for i in range(self.n):
            for j in range(self.n):
                if self.current_grid[i][j] == 'T':
                    if (i, j) not in self.stepped_on_tiles:
                        return

        self.all_treasures_found = True

    def _is_adjacent_to_path(self, row, col):
        if not self.current_path and not self.current_grid:
            return False

        path_to_check = list(self.current_path) if self.current_path else []

        if self.current_grid:
            for i in range(self.n):
                for j in range(self.n):
                    if self.current_grid[i][j] == 'S':
                        path_to_check.append((i, j))
                        break

        if (row, col) in path_to_check:
            return True

        for path_row, path_col in path_to_check:
            row_diff = abs(path_row - row)
            col_diff = abs(path_col - col)

            if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
                return True

        return False

    def get_state(self):
        return {
            'algorithm': 'Human',
            'cost': self.human_cost,
            'runtime': 0,
            'expanded_nodes': 0,
            'heuristic': None
        }
