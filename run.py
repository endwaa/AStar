import os
import sys

from board import read_from_txt, create_neighbors, draw_board
from a_star import a_star
from djikstra import djikstra
from bfs import bfs

# Read board number from command line
if len(sys.argv) == 3:
    board = sys.argv[1]
    number = sys.argv[2]
else:
    print("Select a board. Example: 'python3 run.py 1 1'")
    sys.exit()

# Filename for reading board config
file_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(file_dir, 'boards/board-{0}-{1}.txt'.format(board, number))

# Create list with nodes
node_graph = read_from_txt(filename)

# Create neighbor list for all nodes
for node in node_graph:
    create_neighbors(node, node_graph)

# Get start and goal node
start = list(filter(lambda n: n.content == 'A', node_graph))[0]
goal = list(filter(lambda n: n.content == 'B', node_graph))[0]

# Get shortest path A star
res_a_star = a_star(start, goal)

# Get shortest path Djikstra
res_djikstra = djikstra(start, goal)

# Get path BFS
res_bfs = bfs(start, goal)

# Get visualization of path
draw_board(res_a_star.path, res_a_star.frontier, res_a_star.closed, node_graph, 'A-star-board-{0}-{1}'.format(board, number))
draw_board(res_djikstra.path, res_djikstra.frontier, res_djikstra.closed, node_graph, 'Djikstra-board-{0}-{1}'.format(board, number))
draw_board(res_bfs.path, res_bfs.frontier, res_bfs.closed, node_graph, 'BFS-board-{0}-{1}'.format(board, number))