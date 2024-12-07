from Board import Board
def test_hover_and_resize():
    """
    Test function to dynamically observe hover behavior and responsiveness to resizing the screen.
    """
    import pygame

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

        # Redraw the board and handle hover effects
        board.draw_board()
        board.draw_pieces()
        board.hover_rectangle()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

