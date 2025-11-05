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
                if (grid[nr][nc] != '#') and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))

    return None, expanded_nodes  # No path found

# def DFS(grid, start, end: list):
#     n = len(grid)
#     directions = [(-1,0), (0,1), (0,-1), (1,0)]  # Up, Right, Left, Down
#     expanded_nodes = 0

#     # map all treasure positions to bitmask indices

#     treasure_index = {pos: i for i, pos in enumerate(end)}
#     collected = (1 << len(end)) - 1

#     start_mask = 0
#     if start in treasure_index:
#         start_mask |= (1 << treasure_index[start])

#     queue = [(start, start_mask)]
#     visited = set([(start, start_mask)])
#     parent = {(start, start_mask): None}  # To reconstruct path

#     while queue:
#         (r, c), mask = queue.pop()
#         expanded_nodes += 1
        
#         # Check if we've reached the goal
#         if mask == collected:
#             # Reconstruct path
#             path = []
#             curr = ((r, c), mask)
#             while curr is not None:
#                 pos, _ = curr
#                 path.append(pos)
#                 curr = parent[curr]
#             path.reverse()
#             return path, expanded_nodes

#         # Explore neighbors
#         for dr, dc in directions:
#             nr, nc = r + dr, c + dc
#             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != '#':  # Within bounds
#                 new_mask = mask
#                 if (nr, nc) in treasure_index:
#                     new_mask |= (1 << treasure_index[(nr, nc)])
#                 new_state = ((nr, nc), new_mask)
#                 if new_state not in visited:
#                     visited.add(new_state)
#                     parent[new_state] = ((r, c), mask)
#                     queue.append(new_state)

#     return None, expanded_nodes  # No path found
