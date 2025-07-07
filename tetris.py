import pygame
import random
import sys
import os
from colorama import Fore, Style
import json

# Constants
WIDTH, HEIGHT = 300, 600
ROWS, COLS = 20, 10
BLOCK_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
COLORS = [
    (0, 255, 255), (0, 0, 255), (255, 165, 0),
    (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)
]

# Tetromino Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def valid_space(piece, grid):
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                x = piece.x + j
                y = piece.y + i
                if x < 0 or x >= COLS or y >= ROWS or (y >= 0 and grid[y][x] != BLACK):
                    return False
    return True

def check_lines(grid, locked):
    cleared = 0
    for y in range(ROWS-1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            for x in range(COLS):
                locked.pop((x, y), None)
            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                x, y2 = key
                if y2 < y:
                    locked[(x, y2+1)] = locked.pop((x, y2))
    return cleared

def draw_grid(win, grid):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(win, grid[y][x], (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    for x in range(COLS):
        pygame.draw.line(win, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(win, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))

def draw_window(win, grid, score):
    win.fill(BLACK)
    draw_grid(win, grid)
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render(f"Score: {score}", 1, (255,255,255))
    win.blit(label, (10, 10))
    pygame.display.update()

def load_saved_score():
    if os.path.exists("score.json"):
        with open("score.json", "r") as file:
            data = json.load(file)
            return data.get("score", 0)
    return 0

def save_high_score(score):
    with open("score.json", "w") as file:
        json.dump({"score": score}, file, indent=4)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Piece(random.choice(SHAPES), random.choice(COLORS))
    next_piece = Piece(random.choice(SHAPES), random.choice(COLORS))
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        for _ in range(3):  # Rotate back
                            current_piece.rotate()

        for i, row in enumerate(current_piece.shape):
            for j, val in enumerate(row):
                if val:
                    x = current_piece.x + j
                    y = current_piece.y + i
                    if y >= 0:
                        grid[y][x] = current_piece.color

        if change_piece:
            for i, row in enumerate(current_piece.shape):
                for j, val in enumerate(row):
                    if val:
                        locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color
            current_piece = next_piece
            next_piece = Piece(random.choice(SHAPES), random.choice(COLORS))
            score += check_lines(grid, locked_positions) * 10
            change_piece = False

        draw_window(win, grid, score)

        if any((x, 0) in locked_positions for x in range(COLS)):
            run = False

    pygame.quit()

    print("\n" + Style.BRIGHT + Fore.GREEN + f"Game Over. Final Score: {score}\n")

    # Load saved score and compare
    saved_score = load_saved_score()
    if score > saved_score:
        print(Fore.YELLOW + "New High Score!")
        save_high_score(score)
    else:
        print(Fore.CYAN + f"Highest Score: {saved_score}")

    # Ask to restart
    restart = input(Fore.CYAN + "Restart? (yes/no): ").strip().lower()
    if restart == "yes":
        os.system(f"python {sys.argv[0]}")
    else:
        print(Fore.WHITE + "Thanks for playing!")


if __name__ == "__main__":
    main()
