import os

from board import read_from_txt, create_neighbors, draw_board
from a_star import a_star

# Filename for reading board config
file_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(file_dir, '../boards/board-2-4.txt')

# Create list with nodes
node_graph = read_from_txt(filename)

# Create neighbor list for all nodes
for node in node_graph:
    create_neighbors(node, node_graph)

# Get start and goal node
start = list(filter(lambda n: n.content == 'A', node_graph))[0]
goal = list(filter(lambda n: n.content == 'B', node_graph))[0]

# Get shortest path
res = a_star(start, goal)

# Get visualization of shortest path
draw_board(res.path, res.frontier, res.closed, node_graph)