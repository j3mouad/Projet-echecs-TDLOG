import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
from main_screen import main_screen
# Screen dimensions
SCREEN_WIDTH =  1000
SCREEN_HEIGHT = 500

# Colors
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
INFO_PANEL_COLOR = (50, 50, 50)

# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Chess UI Test - Main and Settings Screen")

# Initialize ChessUI
main_screen = main_screen(screen, LIGHT_COLOR, DARK_COLOR, INFO_PANEL_COLOR)

# Main game loop
running = True
while running:
    # Clear the screen
    screen.fill((0, 0, 0))

    # Render the appropriate screen
    main_screen.which_screen_to_render()

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            main_screen.update_dimensions()
        main_screen.handling_events_logic(event)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()