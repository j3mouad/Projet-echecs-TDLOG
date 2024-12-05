import pygame
import sys

# Initialize Pygame
pygame.init()

# Base dimensions for scaling
BASE_WIDTH = 300
BASE_HEIGHT = 200
base_font_size = 30  # Base font size for reference resolution

# Create a resizable screen
screen_width, screen_height = BASE_WIDTH, BASE_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Responsive Text Scaling")

# Function to dynamically calculate font size
def get_font_size(base_size, width_ratio, height_ratio):
    # Average scaling factor to maintain proportions
    scaling_factor = (width_ratio + height_ratio) / 2
    return int(base_size * scaling_factor)

# Function to draw text on the screen
def draw_text(surface, text, font, color, center_position):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_position)
    surface.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Calculate scaling ratios
    width_ratio = screen_width / BASE_WIDTH
    height_ratio = screen_height / BASE_HEIGHT

    # Calculate dynamic font size
    font_size = get_font_size(base_font_size, width_ratio, height_ratio)
    font = pygame.font.Font(None, font_size)

    # Draw text
    text = "Responsive Text"
    text_color = (255, 255, 255)
    center_position = (screen_width // 2, screen_height // 2)
    draw_text(screen, text, font, text_color, center_position)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
