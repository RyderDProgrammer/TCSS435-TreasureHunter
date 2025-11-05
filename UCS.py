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

# def UCS(grid, start, end: list):
#     n = len(grid)
#     directions = [(-1,0), (0,1), (0,-1), (1,0)]  # Up, Right, Left, Down
#     expanded_nodes = 0

#     # map all treasure positions to bitmask indices

#     treasure_index = {pos: i for i, pos in enumerate(end)}
#     collected = (1 << len(end)) - 1

#     start_mask = 0
#     if start in treasure_index:
#         start_mask |= (1 << treasure_index[start])

#     pq = [(0, start, start_mask)]  # (total_cost, position)
#     visited = set([(start, start_mask)])
#     parent = {(start, start_mask): None}
#     cost_so_far = {start: 0}

#     while pq:
#         pq.sort()  # smallest cost comes first
#         current_cost, (r, c), mask = pq.pop(0)
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
        
#         # explore neighbors
#         for dr, dc in directions:
#             nr, nc = r + dr, c + dc
#             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != '#':  # within bounds
#                 new_cost = current_cost + 1  # cost of each move is 1
#                 new_mask = mask
#                 if (nr, nc) in treasure_index:
#                     new_mask |= (1 << treasure_index[(nr, nc)])
#                 new_state = ((nr, nc), new_mask)
#                 if new_state not in visited and (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
#                     visited.add(new_state)
#                     cost_so_far[(nr, nc)] = new_cost
#                     parent[new_state] = ((r, c), mask)
#                     pq.append((new_cost, new_state[0], new_state[1]))

#     return None, expanded_nodes  # No path found