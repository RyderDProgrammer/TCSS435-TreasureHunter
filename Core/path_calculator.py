class PathCostCalculator:
    @staticmethod
    def calculate_cost(solution_path, grid):
        if not solution_path:
            return 0

        total_cost = 0
        for i, (row, col) in enumerate(solution_path):
            if i == 0:
                continue

            tile = grid[row][col]
            if tile in ['S', 'T']:
                total_cost += 0
            elif tile == 'X':
                total_cost += 5
            else:
                total_cost += 1

        return total_cost
