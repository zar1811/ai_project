import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (0, 0, 0)

# Fonts
RESULT_FONT = pygame.font.SysFont('Arial', 40, bold=True)
RULES_FONT = pygame.font.SysFont('Arial', 20)
font = pygame.font.SysFont('Arial', 25)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Reverse Tic Tac Toe')

# Board
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

difficulty = None
player_choice = None

def draw_lines():
    screen.fill(BG_COLOR)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                # Draw X
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
            elif board[row][col] == -1:
                # Draw O
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in board:
        if 0 in row:
            return False
    return True

def check_loss(player):
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return True
    if all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

def minimax(is_ai_turn, depth=0, alpha=-float('inf'), beta=float('inf'), max_depth=6):
    if check_loss(-1):
        return -1, None
    if check_loss(1):
        return 1, None
    if is_board_full() or depth >= max_depth:
        return 0, None

    if is_ai_turn:
        max_eval = -float('inf')
        best_move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = -1
                    eval, _ = minimax(False, depth+1, alpha, beta, max_depth)
                    board[row][col] = 0
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (row, col)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 1
                    eval, _ = minimax(True, depth+1, alpha, beta, max_depth)
                    board[row][col] = 0
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (row, col)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, best_move

def display_result(result_text):
    result_screen = pygame.display.set_mode((400, 250))
    result_screen.fill((255, 255, 255))
    pygame.draw.rect(result_screen, (0, 150, 136), (20, 60, 360, 130), border_radius=15)
    text = RESULT_FONT.render(result_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 125))
    result_screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def show_rules():
    screen.fill((255, 255, 255))
    rules = [
        "Reverse Tic Tac Toe Rules:",
        "- First to make 3 in a row LOSES.",
        "- Play to avoid making 3 in a row.",
        "- AI gets smarter with harder levels.",
        "- Select difficulty before starting."
    ]
    for i, line in enumerate(rules):
        rendered = RULES_FONT.render(line, True, (0, 0, 0))
        screen.blit(rendered, (20, 60 + i * 30))
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    waiting_for_input = False
                    start_menu()
                    return

def choose_difficulty():
    global difficulty
    difficulty_options = ["Easy", "Medium", "Hard"]
    current_option = 0
    choosing = True

    while choosing:
        screen.fill((255, 255, 255))
        title_text = font.render('Select Difficulty:', True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        for i, option in enumerate(difficulty_options):
            color = (0, 128, 255) if i == current_option else (0, 0, 0)
            option_text = font.render(option, True, color)
            x = WIDTH // 2 - option_text.get_width() // 2
            y = HEIGHT // 2 + i * 40
            screen.blit(option_text, (x, y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_option = (current_option + 1) % len(difficulty_options)
                elif event.key == pygame.K_UP:
                    current_option = (current_option - 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    difficulty = difficulty_options[current_option]
                    choosing = False

def start_menu():
    global player_choice
    menu_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    menu_screen.fill((255, 255, 255))

    pygame.draw.rect(menu_screen, (0, 150, 136), (20, 60, 360, 130), border_radius=15)
    text = RESULT_FONT.render('Reverse Tic Tac Toe', True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 125))
    menu_screen.blit(text, text_rect)

    instructions = RULES_FONT.render('1: Player First | 2: AI First | r: Rules', True, (0, 0, 0))
    menu_screen.blit(instructions, (20, 200))
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_choice = 1
                    waiting_for_input = False
                elif event.key == pygame.K_2:
                    player_choice = -1
                    waiting_for_input = False
                elif event.key == pygame.K_r:
                    show_rules()

    choose_difficulty()
    pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BG_COLOR)
    draw_lines()
    pygame.display.update()

    return player_choice

# ========== MAIN GAME LOOP ==========

player = start_menu()
game_over = False

# Set difficulty depth
if difficulty == "Easy":
    max_depth = 1
elif difficulty == "Medium":
    max_depth = 3
else:
    max_depth = 6  # Hard

# If AI goes first, make the first move immediately
if player == -1:
    pygame.time.delay(500)
    _, move = minimax(True, depth=0, max_depth=max_depth)
    if move:
        mark_square(move[0], move[1], player)
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        pygame.display.update()

        if check_loss(player):
            time.sleep(1)
            display_result('AI Loses!')
        elif is_board_full():
            time.sleep(1)
            display_result('It\'s a Draw!')

        player *= -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if player == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0] // SQUARE_SIZE
                    mouseY = event.pos[1] // SQUARE_SIZE

                    if available_square(mouseY, mouseX):
                        mark_square(mouseY, mouseX, player)

                        # Redraw board and pieces after move
                        screen.fill(BG_COLOR)
                        draw_lines()
                        draw_figures()
                        pygame.display.update()

                        if check_loss(player):
                            time.sleep(1)
                            display_result('Player X Loses!')
                        elif is_board_full():
                            time.sleep(1)
                            display_result('It\'s a Draw!')

                        player *= -1
            else:
                pygame.time.delay(500)
                _, move = minimax(True, depth=0, max_depth=max_depth)
                if move:
                    mark_square(move[0], move[1], player)

                    # Redraw board and pieces after AI move
                    screen.fill(BG_COLOR)
                    draw_lines()
                    draw_figures()
                    pygame.display.update()

                    if check_loss(player):
                        time.sleep(1)
                        display_result('AI Loses!')
                    elif is_board_full():
                        time.sleep(1)
                        display_result('It\'s a Draw!')

                    player *= -1
