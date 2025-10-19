def UCS(grid, start, end):
    n = len(grid)
    directions = [(-1,0), (0,1), (0,-1), (1,0)]  # Up, Right, Left, Down
    expanded_nodes = 0

    pq = [(0, start)]  # (total_cost, position)
    visited = set([start])
    parent = {start: None}
    cost_so_far = {start: 0}

    while pq:
        pq.sort()  # smallest cost comes first
        current_cost, current = pq.pop(0)
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
                new_cost = current_cost + 1  # cost of each move is 1
                if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                    visited.add((nr, nc))
                    cost_so_far[(nr, nc)] = new_cost
                    parent[(nr, nc)] = current
                    pq.append((new_cost, (nr, nc)))

    return None, expanded_nodes  # No path found
