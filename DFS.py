def DFS(grid, start, end):
    n = len(grid)
    directions = [(-1,0), (0,1), (0,-1), (1,0)]  # Up, Right, Left, Down
    expanded_nodes = 0

    stack = [start]
    visited = set([start])
    parent = {start: None}  # To reconstruct path

    while stack:
        current = stack.pop()
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

        # Explore neighbors
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:  # Within bounds
                if (grid[nr][nc] == ' ' or grid[nr][nc] == 'T') and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))

    return None, expanded_nodes  # No path found
