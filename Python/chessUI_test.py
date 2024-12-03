import pygame
from chessUI import ChessUI  # Import the ChessUI class from chessUI.py

# Initialize Pygame
pygame.init()

# Initial screen setup
screen_width, screen_height = 560,350
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Chess UI Test")

# Colors for the chessboard and info panel
light_color = (238, 238, 210)
dark_color = (118, 150, 86)
info_panel_color = (50, 50, 50)

# Test chessboard setup
chess_board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Load images for chess pieces
pieces_images = {
    'bR': pygame.image.load('black_rook.png'),
    'bN': pygame.image.load('black_knight.png'),
    'bB': pygame.image.load('black_bishop.png'),
    'bQ': pygame.image.load('black_queen.png'),
    'bK': pygame.image.load('black_king.png'),
    'bP': pygame.image.load('black_pawn.png'),
    'wR': pygame.image.load('white_rook.png'),
    'wN': pygame.image.load('white_knight.png'),
    'wB': pygame.image.load('white_bishop.png'),
    'wQ': pygame.image.load('white_queen.png'),
    'wK': pygame.image.load('white_king.png'),
    'wP': pygame.image.load('white_pawn.png')
}

# Initialize ChessUI
chess_ui = ChessUI(screen, light_color, dark_color, info_panel_color)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resizing
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            chess_ui.screen = screen

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the chessboard, pieces, and info panel
    chess_ui.draw_board()
    chess_ui.draw_pieces(chess_board)
    chess_ui.draw_info_panel()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
