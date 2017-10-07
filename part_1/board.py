import os
from PIL import Image, ImageFont, ImageDraw


# Board dimensions
BOARD_HEIGHT = 0
BOARD_WIDTH = 0


# Structure for a node
class Node:

    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content
        self.cost = 0
        self.estimated_cost = 0
        self.neighbors = []
        self.parent = None
    
    def add_neighbor(self, node):
        self.neighbors.append(node)

    def __lt__(self, other):
        return self.estimated_cost < other.estimated_cost

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)


# Read board config from txt file and returns a list with all nodes
def read_from_txt(filename):
    global BOARD_HEIGHT     
    global BOARD_WIDTH

    # List with all nodes
    node_graph = []
    # Numbder of words in file
    num_words = 0
    # Number of lines in file
    num_lines = 0

    with open(filename, 'r') as file:
        for x, line in enumerate(file):
            num_lines += 1
            for y, char in enumerate(line):
                if char is not '\n':
                    num_words += 1
                    insert_node(x, y, char, node_graph)

    BOARD_HEIGHT = num_lines                
    BOARD_WIDTH = num_words // num_lines
    return node_graph


# Add node to node list
def insert_node(x, y, char, node_graph):
    node_graph.append(Node(x, y, char))


# Creates neighbors list for a node
def create_neighbors(node, node_graph):
    dirs = [[1,0], [0,1], [-1, 0], [0, -1]]

    for dir in dirs:
        neighbor = list(filter(lambda n: n.x == node.x + dir[0] and n.y == node.y + dir[1], node_graph))
        if neighbor:
            node.add_neighbor(neighbor[0])


# Draw board with path, frontier and closed nodes.
def draw_board(path, frontier, closed, node_graph):
    im = Image.new('RGB', (BOARD_WIDTH*100,BOARD_HEIGHT*100), (255,255,255))
    dr = ImageDraw.Draw(im)
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            node = list(filter(lambda n: n.x == i and n.y == j, node_graph))[0]
            if node.content == '#':
                dr.rectangle([(0+j*100,0+i*100),(100+j*100,100+i*100)], fill="gray", outline = "black")
            else: 
                dr.rectangle([(0+j*100,0+i*100),(100+j*100,100+i*100)], fill="white", outline = "black")

                # Start node
                if node.content == 'A':
                    dr.rectangle([(0+j*100+30,0+i*100+30),(100+j*100-30,100+i*100-30)], fill='black')

                # Goal node
                elif node.content == 'B':
                    dr.rectangle([(0+j*100+30,0+i*100+30),(100+j*100-30,100+i*100-30)], fill='yellow')
                elif node in path:
                    dr.rectangle([(0+j*100+30,0+i*100+30),(100+j*100-30,100+i*100-30)], fill='green')
                elif node in frontier:
                    dr.rectangle([(0+j*100+30,0+i*100+30),(100+j*100-30,100+i*100-30)], fill='blue')
                elif node in closed:
                    dr.rectangle([(0+j*100+30,0+i*100+30),(100+j*100-30,100+i*100-30)], fill='red')
    
    # Display image        
    im.show()       
    
