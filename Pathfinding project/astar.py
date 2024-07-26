import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

RED = (255, 0, 0)
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
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.colour == RED
    
    def is_open(self):
        return self.colour == GREEN
    
    def is_barrier(self):
        return self.colour == BLACK
    
    def is_start(self):
        return self.colour == ORANGE
    
    def is_end(self):
        return self.colour == TURQUOISE
    
    def reset(self):
        self.colour = WHITE

    def make_start(self):
        self.colour = ORANGE

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
    
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbours.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        
        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
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
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    draw_buttons(win)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def create_theme_park_template(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i == 0 or j == 0 or i == len(grid) - 1 or j == len(grid[i]) - 1:
                grid[i][j].make_barrier()
    grid[10][10].make_barrier()
    grid[10][11].make_barrier()

def create_subway_map_template(grid):
    for i in range(len(grid)):
        if i % 5 == 0:
            for j in range(len(grid[i])):
                grid[i][j].make_barrier()
    grid[20][20].make_barrier()
    grid[20][21].make_barrier()

def draw_buttons(win):
    font = pygame.font.SysFont('Arial', 20)
    theme_park_button = pygame.Rect(10, 10, 150, 50)
    subway_map_button = pygame.Rect(10, 70, 150, 50)
    reset_button = pygame.Rect(WIDTH - 160, 10, 150, 50)

    pygame.draw.rect(win, GREY, theme_park_button)
    pygame.draw.rect(win, GREY, subway_map_button)
    pygame.draw.rect(win, GREY, reset_button)

    theme_park_text = font.render('Theme Park', True, BLACK)
    subway_map_text = font.render('Subway Map', True, BLACK)
    reset_text = font.render('Reset', True, BLACK)

    win.blit(theme_park_text, (15, 20))
    win.blit(subway_map_text, (15, 80))
    win.blit(reset_text, (WIDTH - 145, 20))

    return theme_park_button, subway_map_button, reset_button

def handle_button_click(pos, buttons):
    theme_park_button, subway_map_button, reset_button = buttons
    if theme_park_button.collidepoint(pos):
        return 'theme_park'
    elif subway_map_button.collidepoint(pos):
        return 'subway_map'
    elif reset_button.collidepoint(pos):
        return 'reset'
    return None

def main(win, width):
    pygame.init()
    pygame.font.init()  # Initialize the font module

    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None 
    end = None
    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        buttons = draw_buttons(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_template = handle_button_click(pos, buttons)
                if clicked_template:
                    if clicked_template == 'theme_park':
                        create_theme_park_template(grid)
                    elif clicked_template == 'subway_map':
                        create_subway_map_template(grid)
                    elif clicked_template == 'reset':
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)
                    continue

                if pygame.mouse.get_pressed()[0]: # Left mouse button
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()
                
                elif pygame.mouse.get_pressed()[2]: # Right mouse button
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
