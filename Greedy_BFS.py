def Greedy_BFS(grid, start, end):
    n = len(grid)
    directions = [(-1, 0), (0, 1), (0, -1), (1, 0)]
    expanded_nodes = 0

    # manhattan distance heuristic
    def heuristic(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

    pq = [(heuristic(start), start)]
    visited = set([start])
    parent = {start: None}

    while pq:
        pq.sort()  # smallest h_cost is first
        current_h, current = pq.pop(0)
        expanded_nodes += 1

        # check the goal if reached
        if current == end:
            # build path
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
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current
                    h_cost = heuristic((nr, nc))  # Only heuristic, no g cost
                    pq.append((h_cost, (nr, nc)))

    return None, expanded_nodes  # No path found

