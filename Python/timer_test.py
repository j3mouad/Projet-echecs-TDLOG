import pygame
from timer import TimerUI  # Import your TimerUI class from its file
from Board import Board       # Import your Board class from its file

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 640
BOARD_WIDTH_RATIO = 3 / 5  # Left 3/5 for board
FPS = 60

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess Board with Timer UI")

# Colors
WHITE_COLOR = (238, 238, 210)
BLACK_COLOR = (181, 136, 99)

# Create Board and TimerUI instances
board = Board(
    screen=screen,
    rectangle_width=SCREEN_WIDTH // 8,
    rectangle_height=SCREEN_HEIGHT // 8,
    white_rectangle_color=WHITE_COLOR,
    black_rectangle_color=BLACK_COLOR,
)

timer_ui = TimerUI()

def main():
    clock = pygame.time.Clock()
    running = True
    global screen
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle resizing
                global SCREEN_WIDTH, SCREEN_HEIGHT
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

                # Update dimensions for the board
                board.update_dimension()
            else:
                timer_ui.handle_event(event)

        # Fill background
        screen.fill((238, 238, 210))

        # Draw chessboard on the left
        board_width = int(SCREEN_WIDTH * BOARD_WIDTH_RATIO)
        board.rectangle_width = board_width // 8
        board.rectangle_height = SCREEN_HEIGHT // 8
        board.draw_board()
        board.draw_pieces()

        # Draw timer UI on the right
        timer_rect = (board_width, 0, SCREEN_WIDTH - board_width, SCREEN_HEIGHT)
        timer_ui.draw(screen, timer_rect)

        # Flip display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

