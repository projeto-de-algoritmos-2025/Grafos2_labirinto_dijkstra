import pygame

def draw_arrow(surface, color, pos, direction, size):
    x, y = pos
    if direction == (-1, 0):
        points = [(x, y-size), (x-size, y), (x+size, y)]
    elif direction == (1, 0):
        points = [(x, y+size), (x-size, y), (x+size, y)]
    elif direction == (0, -1):
        points = [(x-size, y), (x, y-size), (x, y+size)]
    else:
        points = [(x+size, y), (x, y-size), (x, y+size)]
    pygame.draw.polygon(surface, color, points)