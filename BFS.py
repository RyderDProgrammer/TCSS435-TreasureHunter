from collections import deque
import time

# Number of expanded nodes
BFS_EXPANDED = 0

# Runtime
BFS_RUNTIME = 0

def BFS(grid, start, end):
    n = len(grid)
    directions = [(-1,0), (0,1), (0,-1), (1,0)]  # Up, Right, Left, Down
    BFS_EXPANDED = 0

    queue = deque([start])
    visited = set([start])
    parent = {start: None}  # To reconstruct path

    while queue:
        current = queue.popleft()
        BFS_EXPANDED += 1

        # Check if we've reached the goal
        if current == end:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        # Explore neighbors
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:  # Within bounds
                if (grid[nr][nc] == ' ' or grid[nr][nc] == 'T') and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    return None  # No path found