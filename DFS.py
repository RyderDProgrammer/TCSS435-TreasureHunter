from collections import deque

def DFS(grid, start, end):
    n = len(grid)
    directions = [(-1,0), (0,1), (0,-1), (1,0)]  # Up, Right, Left, Down
    nodes_expanded = 0

    queue = deque([start])
    visited = set([start])
    parent = {start: None}  # To reconstruct path

    while queue:
        current = queue.popleft()
        nodes_expanded += 1

        # Check if we've reached the goal
        if current == end:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            print(f'Nodes Expanded: {nodes_expanded}')
            return path

        # Explore neighbors
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:  # Within bounds
                if (grid[nr][nc] == ' ' or grid[nr][nc] == 'T') and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.appendleft((nr, nc))

    return None  # No path found
