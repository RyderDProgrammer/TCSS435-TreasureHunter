# Python3 program for the above approach
from collections import deque 

# Direction vectors
dRow = [ -1, 0, 1, 0]
dCol = [ 0, 1, 0, -1]

# size of grid
n = 8

# Function to check if a cell
# is be visited or not
def isValid(vis, row, col):
  
    # If cell lies out of bounds
    if (row < 0 or col < 0 or row >= n or col >= n):
        return False

    # If cell is already visited
    if (vis[row][col]):
        return False

    # Otherwise
    return True

# Function to perform the BFS traversal
def BFS(grid, vis, row, col):

    # get size of grid
    n = len(grid[0])

    # number of visited nodes
    count = 0
    # Stores indices of the matrix cells
    q = deque()

    # Mark the starting cell as visited
    # and push it into the queue
    q.append(( row, col ))
    vis[row][col] = True

    # Iterate while the queue
    # is not empty
    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        #print(grid[x][y], end = " ")
        print(f'({x}, {y})', end=' ')

        count += 1


        #q.pop()

        # Go to the adjacent cells
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (isValid(vis, adjx, adjy)):
                q.append((adjx, adjy))
                vis[adjx][adjy] = True

    print(f'Number of visited nodes: {count}')

def bfs_path(matrix, start, end):

    n = len(matrix)
    directions = [(1,0), (-1,0), (0,1), (0,-1)]  # Down, Up, Right, Left
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
                if (matrix[nr][nc] == ' ' or matrix[nr][nc] == 'T') and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    return None  # No path found


# Example usage:
# if __name__ == "__main__":
#     grid = [
#         [0, 0, 1, 0],
#         [1, 0, 1, 0],
#         [0, 0, 0, 0],
#         [0, 1, 1, 0]
#     ]

#     start = (0, 0)
#     end = (3, 3)

#     path = bfs_path(grid, start, end)
#     if path:
#         print("Path found:")
#         for step in path:
#             print(step)
#     else:
#         print("No path found.")