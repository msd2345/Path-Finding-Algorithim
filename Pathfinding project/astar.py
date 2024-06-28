import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path finding algorithim")

RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    #Method for Variables
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    #Method for position
    def get_pos(self):
        return self.row, self.col
    
    #Method for closed node
    def is_closed(self):
        return self.colour == RED
    
    #Method for open node
    def is_open(self):
        return self.colour == GREEN
    
    #Method for obstacle node    
    def is_barrier(self):
        return self.colour == BLACK
    
    #Method for starting node colour
    def is_start(self):
        return self.colour == ORANGE
    
    #Method for end node colour
    def is_end(self):
        return self.colour == PURPLE
    
    #Method for restting
    def reset(self):
        self.colour == WHITE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN
    
    def make_barrier(self):
        self.colour = BLACK
    
    def make_end(self):
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = PURPLE
    
    #Method for the pygame window
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        pass
    
    #Method to compare the values for patthing
    def __lt__(self, other):
        return False

#Hueristic function    
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#Grid making function
def make_grid(rows, width):
    grid = [ ]
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.file(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()