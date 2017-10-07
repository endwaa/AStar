import bisect
import math
import collections

# Result from A*, able to return multiple variables
Result = collections.namedtuple('Result', ['path', 'frontier', 'closed'])


# Heuristic cost methods (Estimated cost to goal)
############

def manhattan_distance(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)


def euclidean_distance(node, goal):
    return math.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2)

############

# Cost so far and heuristic cost
def total_cost(node, goal):
    return node.cost + manhattan_distance(node, goal)


# Reconstruct shortest path from start to goal node
def reconstruct_path(node, start):
    path = []
    path.append(node)
    while node != start:
        path.append(node)
        node = node.parent
    return path


# Calculate shortest path form start to goal
def a_star(start, goal):
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
            
            if neighbor in closed:
                continue

            neighbor.parent = current
            neighbor.cost = current.cost + 1
            neighbor.estimated_cost = total_cost(neighbor, goal)

            if neighbor not in frontier:
                bisect.insort(frontier, neighbor) # Adds node in frontier list (Ascending order)


                

