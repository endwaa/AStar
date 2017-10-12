import bisect
import math
import collections

# Result from A*, able to return multiple variables
Result = collections.namedtuple('Result', ['path', 'frontier', 'closed'])


# Reconstruct shortest path from start to goal node
def reconstruct_path(node, start):
    path = []
    path.append(node)
    while node != start:
        node = node.parent
        path.append(node)
    return path


# Calculate shortest path form start to goal
def bfs(start, goal):
    frontier = [start]
    closed = []

    while frontier:
        current = frontier[0] # Get node with least cost

        if current == goal:
            path = reconstruct_path(current, start)
            return Result(path, frontier, closed)

        # Remove current from frontier and add it to closed list
        del frontier[0]
        closed.append(current)

        for neighbor in current.neighbors:
            if neighbor.content is '#': # Blocked node
                closed.append(neighbor)
                continue
            
            if neighbor in closed or neighbor in frontier:
                continue

            neighbor.parent = current
            neighbor.cost = current.cost + neighbor.cell_cost
            neighbor.estimated_cost = neighbor.cost

            if neighbor not in frontier:
                frontier.append(neighbor) # Adds node in frontier list


                

