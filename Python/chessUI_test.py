import pygame
from chessUI import ChessUI  # Import the ChessUI class from chessUI.py

# Initialize Pygame
pygame.init()

# Initial screen setup
screen_width, screen_height = 1000, 500
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Chess UI Test")

# Colors for the chessboard and info panel
light_color = (238, 238, 210)
dark_color = (118, 150, 86)
info_panel_color = (50, 50, 50)

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

# Variables for settings
play_with_white = False  # Default to playing with white
chess_game_mode = "Classic"  # Default game mode

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

    # Render the settings panel
    chess_ui.settings(play_with_white, chess_game_mode)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

