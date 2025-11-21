import copy
import random
import math

#counter for nodes expanded
nodes_expanded = 0

#configurable search depth
MAX_DEPTH = 2

def Alpha_Beta(grid, start, end):
    global nodes_expanded
    nodes_expanded = 0

    #place opponent
    opponent_start = place_opponent_strategic(grid, start, end)

    #initialize game state
    initial_state = {
        'agent_a_pos': start,
        'agent_b_pos': opponent_start,
        'treasure_pos': end,
        'grid': grid,
        'agent_a_path': [start],
        'treasure_collected': False
    }

    #run the game simulation using minimax
    final_state = simulate_game_with_minimax(initial_state, MAX_DEPTH)

    #return results
    path = final_state['agent_a_path']

    #make sure to reach treasure
    if not final_state['treasure_collected'] and path[-1] != end:
        #add path to treasure if minimax failed
        assert isinstance(path, list)
        path.extend(get_simple_path(path[-1], end, grid))

    #return negative distance as heuristic
    if final_state['treasure_collected']:
        heuristic_value = -len(path)
    else:
        heuristic_value = -manhattan_distance(path[-1], end) - len(path)

    return path, nodes_expanded, heuristic_value


def get_simple_path(start, end, grid):
    """
    Greedy pathfinding that always moves closer to the goal.
    Uses BFS as fallback if greedy approach fails.
    """
    path = []
    current = start
    visited = {start}

    for _ in range(200):  #max iterations (increased limit)
        if current == end:
            break

        legal = get_legal_moves_simple(grid, current)
        legal = [m for m in legal if m not in visited]

        if not legal:
            # No unvisited moves - try BFS to find a path
            bfs_path = bfs_fallback(current, end, grid)
            if bfs_path:
                path.extend(bfs_path)
            break

        #move closer to treasure
        next_pos = min(legal, key=lambda m: manhattan_distance(m, end))
        path.append(next_pos)
        visited.add(next_pos)
        current = next_pos

    return path


def bfs_fallback(start, end, grid):
    from collections import deque

    queue = deque([(start, [])])
    visited = {start}

    max_iterations = 500
    iterations = 0

    while queue and iterations < max_iterations:
        iterations += 1
        current, path = queue.popleft()

        if current == end:
            return path

        legal = get_legal_moves_simple(grid, current)

        for move in legal:
            if move not in visited:
                visited.add(move)
                new_path = path + [move]
                queue.append((move, new_path))

    return []  #no path found


def simulate_game_with_minimax(initial_state, max_depth):
    state = dict(initial_state)
    state['agent_a_path'] = copy.deepcopy(initial_state['agent_a_path'])

    max_turns = 50
    turn = 0
    path_set = set(state['agent_a_path'])
    consecutive_no_progress = 0
    recent_positions = []  #track recent positions to detect loops

    while turn < max_turns and not state['treasure_collected']:
        last_pos = state['agent_a_path'][-1] if state['agent_a_path'] else None

        #agent A turn - use minimax
        best_move, _ = minimax_decision(state, max_depth, True, path_set)

        if best_move is None:
            best_move = get_best_greedy_move(state, path_set)

        #avoid immediate backtrack if there is an alternative
        if best_move == last_pos:
            alt = get_best_greedy_move(state, path_set)
            if alt is not None and alt != last_pos:
                best_move = alt

        if best_move is None:
            break

        #check for progress
        current_dist = manhattan_distance(state['agent_a_pos'], state['treasure_pos'])
        new_dist = manhattan_distance(best_move, state['treasure_pos'])

        if new_dist >= current_dist and best_move in path_set:
            consecutive_no_progress += 1
        else:
            consecutive_no_progress = 0

        #force greedy if stuck
        if consecutive_no_progress >= 2:
            forced = get_best_greedy_move(state, path_set)
            if forced is not None and forced != last_pos:
                best_move = forced
            consecutive_no_progress = 0

        if best_move is None:
            break

        #apply move
        state['agent_a_pos'] = best_move
        assert isinstance(state['agent_a_path'], list)
        state['agent_a_path'].append(best_move)
        path_set.add(best_move)

        #track recent positions to detect loops
        recent_positions.append(best_move)
        if len(recent_positions) > 8:
            recent_positions.pop(0)

        #check if stuck in loop
        if len(recent_positions) >= 8:
            unique_positions = len(set(recent_positions))
            if unique_positions <= 3:
                #stuck in loop break out; let fallback handle it
                break

        #check treasure
        if best_move == state['treasure_pos']:
            assert isinstance(state, dict)
            state['treasure_collected'] = True
            break

        #agent B move
        opp_move = get_opponent_move(state)
        if opp_move:
            state['agent_b_pos'] = opp_move

        turn += 1

    return state



def get_best_greedy_move(state, visited_set):
    legal = get_legal_moves_simple(state['grid'], state['agent_a_pos'])
    goal = state['treasure_pos']

    #prefer unvisited
    unvisited = [m for m in legal if m not in visited_set or m == goal]

    if unvisited:
        return min(unvisited, key=lambda m: manhattan_distance(m, goal))

    #all visited so pick closest
    if legal:
        return min(legal, key=lambda m: manhattan_distance(m, goal))

    return None

'''
Updated to include alpha-beta pruning
'''
def minimax_decision(state, max_depth, is_maximizing, visited_set):
    alpha = -math.inf
    beta = math.inf

    legal_moves = get_legal_moves_simple(
        state['grid'],
        state['agent_a_pos'] if is_maximizing else state['agent_b_pos']
    )

    if not legal_moves:
        return None, evaluate_state(state)

    # Root-only prioritization for A
    if is_maximizing:
        treasure = state['treasure_pos']
        unvisited = [m for m in legal_moves if m not in visited_set or m == treasure]
        if unvisited:
            legal_moves = unvisited

    # Root-only anti-backtracking
    last_pos = state['agent_a_path'][-1] if state.get('agent_a_path') else None
    if is_maximizing and last_pos and len(legal_moves) > 1 and last_pos in legal_moves:
        legal_moves = [m for m in legal_moves if m != last_pos]

    best_move = None

    if is_maximizing:
        best_value = -math.inf
        for move in legal_moves:
            new_state = apply_move(state, move, True)
            value = minimax_value(new_state, 1, max_depth, False, alpha, beta)

            # Add your heuristic bonus
            dist_bonus = -manhattan_distance(move, state['treasure_pos'])
            value += dist_bonus * 0.5

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)
            if alpha >= beta:
                break  # prune at root
    else:
        best_value = math.inf
        for move in legal_moves:
            new_state = apply_move(state, move, False)
            value = minimax_value(new_state, 1, max_depth, True, alpha, beta)

            if value < best_value:
                best_value = value
                best_move = move

            beta = min(beta, best_value)
            if beta <= alpha:
                break

    return best_move, best_value

'''
Updated to include alpha-beta pruning
'''
def minimax_value(state, depth, max_depth, is_maximizing, alpha, beta):
    global nodes_expanded
    nodes_expanded += 1

    # Terminal or depth reached
    if state['treasure_collected']:
        return 10000
    if depth >= max_depth:
        return evaluate_state(state)

    # Determine whose legal moves
    legal_moves = get_legal_moves_simple(
        state['grid'],
        state['agent_a_pos'] if is_maximizing else state['agent_b_pos']
    )

    if not legal_moves:
        return evaluate_state(state)

    # Anti-backtracking for agent A (deeper levels)
    if is_maximizing:
        if state.get('agent_a_path') and len(state['agent_a_path']) >= 2:
            last_pos = state['agent_a_path'][-2]
            if last_pos and len(legal_moves) > 1 and last_pos in legal_moves:
                legal_moves = [m for m in legal_moves if m != last_pos]

    # Max-player branch (Agent A)
    if is_maximizing:
        max_value = -math.inf
        for move in legal_moves:
            new_state = apply_move(state, move, True)
            value = minimax_value(new_state, depth + 1, max_depth, False, alpha, beta)

            max_value = max(max_value, value)
            alpha = max(alpha, max_value)

            if alpha >= beta:   # prune
                break
        return max_value

    # Min-player branch (Agent B)
    else:
        min_value = math.inf
        for move in legal_moves:
            new_state = apply_move(state, move, False)
            value = minimax_value(new_state, depth + 1, max_depth, True, alpha, beta)

            min_value = min(min_value, value)
            beta = min(beta, min_value)

            if beta <= alpha:  # prune
                break
        return min_value




def evaluate_state(state):
    if state['treasure_collected']:
        return 10000

    agent_a_pos = state['agent_a_pos']
    agent_b_pos = state['agent_b_pos']
    treasure_pos = state['treasure_pos']
    grid = state['grid']

    #distances
    dist_a = manhattan_distance(agent_a_pos, treasure_pos)
    dist_b = manhattan_distance(agent_b_pos, treasure_pos)

    #trap penalty
    trap_penalty = 5
    if grid[agent_a_pos[0]][agent_a_pos[1]] == 'X':
        trap_penalty = 100

    #revisit penalty so it discourage being on square already visited multiple times
    revisit_count = state['agent_a_path'].count(agent_a_pos) if state.get('agent_a_path') else 0
    revisit_penalty = max(0, revisit_count - 1) * 50

    utility = (
            -dist_a * 25
            + dist_b * 2
            - trap_penalty
            - revisit_penalty
    )

    return utility



def get_legal_moves_simple(grid, pos):
    n = len(grid)
    row, col = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    legal_moves = []

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < n and 0 <= new_col < n:
            if grid[new_row][new_col] != '#':
                legal_moves.append((new_row, new_col))

    return legal_moves


def apply_move(state, move, is_agent_a):
    #create isolated child state so simulation branches dont share the same path list
    new_state = {
        'agent_a_pos': state['agent_a_pos'],
        'agent_b_pos': state['agent_b_pos'],
        'treasure_pos': state['treasure_pos'],
        'grid': state['grid'],
        'agent_a_path': copy.deepcopy(state['agent_a_path']),
        'treasure_collected': state['treasure_collected']
    }

    if is_agent_a:
        new_state['agent_a_pos'] = move
        #append simulated move to the childs path so eval see realistic paths
        if isinstance(new_state['agent_a_path'], list):
            new_state['agent_a_path'].append(move)
        if move == state['treasure_pos']:
            new_state['treasure_collected'] = True
    else:
        new_state['agent_b_pos'] = move

    return new_state


def get_opponent_move(state):
    legal = get_legal_moves_simple(state['grid'], state['agent_b_pos'])

    if not legal:
        return None

    treasure = state['treasure_pos']
    return min(legal, key=lambda m: manhattan_distance(m, treasure))


def place_opponent_strategic(grid, start, end):
    n = len(grid)
    mid_row = (start[0] + end[0]) // 2
    mid_col = (start[1] + end[1]) // 2

    #try midpoint area
    for radius in range(3):
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                pos = (mid_row + dr, mid_col + dc)
                if (0 <= pos[0] < n and 0 <= pos[1] < n and
                        pos != start and pos != end and
                        grid[pos[0]][pos[1]] not in ['#', 'T', 'X', 'S']):
                    return pos

    #fallback
    for _ in range(20):
        pos = (random.randint(0, n - 1), random.randint(0, n - 1))
        if (pos != start and pos != end and
                grid[pos[0]][pos[1]] not in ['#', 'T', 'X', 'S']):
            return pos

    return (n // 2, n // 2)


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])