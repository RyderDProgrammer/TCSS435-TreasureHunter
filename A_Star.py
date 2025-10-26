def A_Star(grid, start, end):
    n = len(grid)
    directions = [(-1,0), (0,1), (0,-1), (1,0)]  # Up, Right, Left, Down
    expanded_nodes = 0

    # Manhattan distance heuristic
    def heuristic(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

    pq = [(heuristic(start), start)]  # (f_cost, position) where f = g + h
    visited = set([start])
    parent = {start: None}
    cost_so_far = {start: 0}

    while pq:
        pq.sort()  # smallest f_cost comes first
        current_f, current = pq.pop(0)
        expanded_nodes += 1

        # Check if we've reached the goal
        if current == end:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, expanded_nodes
        
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == '#':  # Obstacle
                    continue
                new_cost = cost_so_far[current] + 1  # cost of each move is 1
                if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                    visited.add((nr, nc))
                    cost_so_far[(nr, nc)] = new_cost
                    parent[(nr, nc)] = current
                    f_cost = new_cost + heuristic((nr, nc))  # f = g + h
                    pq.append((f_cost, (nr, nc)))

    return None, expanded_nodes  # No path found