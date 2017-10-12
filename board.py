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
        self.cell_cost = cell_costs(content)
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


# Get cell cost based on content
def cell_costs(content):
    # Water
    if content is 'w':
        return 100

    # Mountains
    if content is 'm':
        return 50

    # Forests
    if content is 'f':
        return 10

    # Grassland
    if content is 'g':
        return 5

    # Roads
    if content is 'r':
        return 1

    # Default
    return 1


# Get board color based on content
def get_color(content):
    # Water
    if content is 'w':
        return '#0000ff' # Blue

    # Mountains 
    if content is 'm':
        return '#808080' # Gray

    # Forests
    if content is 'f':
        return '#004d00' # Dark green

    # Grassland
    if content is 'g':
        return '#00e600' # Light green

    # Roads
    if content is 'r':
        return '#c68c53' # Light brown

    # Start
    if content is 'A':
        return '#ffffff' # Black

    # Goal
    if content is 'B':
        return '#ffff00' # Yellow

    # BLocked node
    if content is '#':
        return 'gray'

    # Default
    return 'white'

# Draw board with path, frontier and closed nodes.
def draw_board(path, frontier, closed, node_graph, filename):
    im = Image.new('RGB', (BOARD_WIDTH*100,BOARD_HEIGHT*100), (255,255,255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("Arial.ttf", 25)
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            node = list(filter(lambda n: n.x == i and n.y == j, node_graph))[0]
            dr.rectangle([(0+j*100,0+i*100),(100+j*100,100+i*100)], fill=get_color(node.content), outline = "black")

            # White circle indicates that this node was in frontier list
            if node in frontier and node not in path:
                dr.ellipse((0+j*100+30,0+i*100+30,100+j*100-30,100+i*100-30), fill='black')

            # Red circle indicates that this node was in closed list
            elif node in closed and node not in path:
                dr.ellipse((0+j*100+30,0+i*100+30,100+j*100-30,100+i*100-30), fill='red')

            # Draw text for start node
            if node.content is 'A':
                dr.text((0+j*100+10,0+i*100+10), "START", (0,0,0), font=font)

            # Draw text for goal node
            if node.content is 'B':
                dr.text((0+j*100+10,0+i*100+10), "GOAL", (0,0,0), font=font)
    

    # Line from start to goal
    dr.line([(n.y*100 + 50, n.x*100 + 50) for n in path], fill="pink", width=15)

    # Save image
    im.save("img/{0}.png".format(filename), "PNG")   
    
