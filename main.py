import pygame
from pygame.locals import *
from maze import Maze
from utils import draw_arrow

def start_screen(screen, WIDTH, HEIGHT):
    font_title = pygame.font.SysFont(None, 80)
    font_subtitle = pygame.font.SysFont(None, 40)
    font_instruction = pygame.font.SysFont(None, 30)  
    title = font_title.render("Maze Escape", True, (0, 0, 0))
    subtitle = font_subtitle.render("Find your way out of the labyrinth!", True, (250, 50, 50))
    instruction = font_instruction.render("Press SPACE to start", True, (100, 100, 100))
    screen.fill((255, 255, 255))
    screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 3))
    screen.blit(subtitle, ((WIDTH - subtitle.get_width()) // 2, HEIGHT // 3 + 80))
    screen.blit(instruction, ((WIDTH - instruction.get_width()) // 2, HEIGHT - 100))

    pygame.display.flip()

    waiting = True  
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  
                    waiting = False

def game_over_screen(screen, WIDTH, HEIGHT, final_time):
    font_title = pygame.font.SysFont(None, 60)
    font_time = pygame.font.SysFont(None, 40)
    total_seconds = final_time // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    game_over_text = font_title.render("GAME OVER", True, (255, 0, 0))  
    info_text = font_title.render(" Press any key to exit", True, (0, 0, 0))
    time_text = font_time.render(f"Time: {minutes:02d}:{seconds:02d}", True, (100, 100, 100))
    screen.fill((255, 255, 255))
    screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 80))
    screen.blit(info_text, ((WIDTH - info_text.get_width()) // 2, HEIGHT // 2 - 20))
    screen.blit(time_text, ((WIDTH - time_text.get_width()) // 2, HEIGHT // 2 + 40))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                waiting = False

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 800
    CELL_SIZE = 25
    maze_cols = WIDTH // CELL_SIZE
    maze_rows = HEIGHT // CELL_SIZE

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Labirinto com Navegação")

    start_screen(screen, WIDTH, HEIGHT)

    maze = Maze(maze_cols, maze_rows)
    maze.dijkstra()

    running = True
    clock = pygame.time.Clock()
    
    start_time = pygame.time.get_ticks()
    won = False
    
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                moved = False
                if event.key == K_UP:
                    moved = maze.move_player((-1, 0))
                elif event.key == K_DOWN:
                    moved = maze.move_player((1, 0))
                elif event.key == K_LEFT:
                    moved = maze.move_player((0, -1))
                elif event.key == K_RIGHT:
                    moved = maze.move_player((0, 1))
                if moved and maze.player_pos == maze.target_pos:
                    running = False
                    won = True

        screen.fill((255, 255, 255))
        
        for row in range(maze.height):
            for col in range(maze.width):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                key = maze.grid[row][col]

                if (row - 1 < 0) or (maze.grid[row - 1][col] not in maze.portals[key]):
                    pygame.draw.line(screen, (0, 0, 0), (x, y), (x + CELL_SIZE, y), 2)
                if (col + 1 >= maze.width) or (maze.grid[row][col + 1] not in maze.portals[key]):
                    pygame.draw.line(screen, (0, 0, 0), (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
                if (row + 1 >= maze.height) or (maze.grid[row + 1][col] not in maze.portals[key]):
                    pygame.draw.line(screen, (0, 0, 0), (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
                if (col - 1 < 0) or (maze.grid[row][col - 1] not in maze.portals[key]):
                    pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + CELL_SIZE), 2)

        tr, tc = maze.target_pos
        pygame.draw.rect(screen, (255, 60, 60), (tc * CELL_SIZE + 4, tr * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))

        pr, pc = maze.player_pos
        player_rect = pygame.Rect(pc * CELL_SIZE + 4, pr * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(screen, (0, 150, 255), player_rect)
        
        arrow_size = CELL_SIZE // 3
        center_x = pc * CELL_SIZE + CELL_SIZE // 2
        center_y = pr * CELL_SIZE + CELL_SIZE // 2
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for direction in directions:
            color = maze.get_direction_color(direction)
            dr, dc = direction
            arrow_x = center_x + dc * (CELL_SIZE // 3)
            arrow_y = center_y + dr * (CELL_SIZE // 3)
            draw_arrow(screen, color, (arrow_x, arrow_y), direction, arrow_size)

        pygame.display.flip()
    
    if won:
        end_time = pygame.time.get_ticks()
        final_time = end_time - start_time  
        game_over_screen(screen, WIDTH, HEIGHT, final_time)

    pygame.quit()

if __name__ == "__main__":
    main()