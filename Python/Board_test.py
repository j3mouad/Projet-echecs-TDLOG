from Board import Board
import time
import pygame
def test_hover_and_resize():
    """
    Test function to dynamically observe hover behavior ,smooth transitions and responsiveness to resizing the screen.
    """
    

    # Initialize Pygame
    pygame.init()

    # Initial screen dimensions
    initial_width, initial_height = 600, 600
    screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
    pygame.display.set_caption("Test Hover and Resize")

    # Colors for the board
    white_color = (240, 217, 181)  # Light square color
    black_color = (181, 136, 99)   # Dark square color

    # Create Board instance
    rectangle_width = initial_width // 8
    rectangle_height = initial_height // 8
    board = Board(screen, rectangle_width, rectangle_height, white_color, black_color)
    s=0
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle screen resizing
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.w, event.h
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                board.screen = screen
                board.update_dimension()  # Update dimensions for the resized screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.select_rectangle(event, [])

        # Redraw the board and handle hover effects
        if board.last_selected_rectangle == None:
            board.draw_board()
            board.draw_pieces()
        if(s==0):
            clock = pygame.time.Clock()
            board.smooth_transition((4, 6), (4, 3), 30)
            time.sleep(0.5)  # Wait for 2 seconds
            clock.tick(100)

            board.smooth_transition((4, 3), (4, 6), 30)
            time.sleep(0.5)  # Wait for 2 seconds
            clock.tick(100)

            board.smooth_transition((0, 7), (7, 0), 30)
            time.sleep(0.5)  # Wait for 2 seconds
            s += 1

        board.hover_rectangle()
        

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

test_hover_and_resize()