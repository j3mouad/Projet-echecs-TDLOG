import pygame
from typing import Literal
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
white_clock = pygame.image.load('white_clock.png')
black_clock = pygame.image.load('black_clock.png')
class Fancy_buttons:
    def __init__(self, screen, fraction_of_x, fraction_of_y, fraction_of_width, fraction_of_height):
        
        assert fraction_of_x + fraction_of_width <= 1, " fraction_of_x + fraction_of_width > 1 " 
        assert fraction_of_y + fraction_of_height <= 1, " fraction_of_y + fraction_of_height > 1 " 
        
        width, height = screen.get_size()
        self.screen = screen
        self.fraction_of_x = fraction_of_x
        self.fraction_of_y = fraction_of_y
        self.fraction_of_width = fraction_of_width
        self.fraction_of_height = fraction_of_height
        self.x = fraction_of_x * width
        self.y = fraction_of_y * height
        self.width = fraction_of_width * width
        self.height = fraction_of_height * height
        self.base_font_size = 24  
              

    def recalculate_dimensions(self):
        width, height = self.screen.get_size()
        self.x = self.fraction_of_x * width
        self.y = self.fraction_of_y * height
        self.width = self.fraction_of_width * width
        self.height = self.fraction_of_height * height

    def draw_timer(self, time: float, player: Literal['white', 'black'], captured_pieces: list[str]):
        # Ensure width and height are integers
        int_width = int(self.width)
        int_height = int(self.height)   

        # Validate dimensions
        if int_width <= 0 or int_height <= 0:
            raise ValueError(f"Invalid Surface dimensions: width={int_width}, height={int_height}")
        if int_width > 2000 or int_height > 2000:  # Arbitrary upper limit for sanity
            raise ValueError(f"Surface dimensions too large: width={int_width}, height={int_height}")

        # Draw a transparent black rectangle with rounded corners
        overlay = pygame.Surface((int_width, int_height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, int_width, int_height), border_radius=20)
        self.screen.blit(overlay, (self.x, self.y))

        # Calculate sizes and positions dynamically
        padding = int(self.height * 0.05)
        font_size = max(12, int(self.height * 0.15))  # Ensure font size doesn't go below 12
        timer_font_size = max(16, int(self.height * 0.2))

        # Fonts
        font = pygame.font.SysFont('Arial', font_size)
        timer_font = pygame.font.SysFont('Arial', timer_font_size, bold=True)
        
        #draw the player turn s
        if player == "white":
            scaled_white_clock = pygame.transform.scale(white_clock, (0.5 * self.width, 0.3 * self.height))
            screen.blit(scaled_white_clock, (self.x - 0.1*self.width , self.y))
        else:
            scaled_black_clock = pygame.transform.scale(black_clock, (0.5 * self.width, 0.3 * self.height))
            screen.blit(scaled_black_clock, (self.x - 0.1*self.width , self.y))
    

        # Draw the timer
        timer_text = f"{time:.1f} s"
        timer_surface = timer_font.render(timer_text, True, (255, 255, 255) if time < 10 else (255, 255, 255))
        self.screen.blit(timer_surface, (self.x + self.width*0.35, self.y + padding - self.height*0.01))

        # Draw captured pieces section


        # Display captured pieces
        piece_size = max(12, int(self.height * 0.15))  # Size of each captured piece symbol
        piece_y = self.y + self.height // 2 + padding  # Position below the "Captured:" label

        for idx, piece in enumerate(captured_pieces):
            piece_surface = font.render(piece, True, (255, 255, 255))
            piece_x = self.x + padding + idx * (piece_size + padding)
            self.screen.blit(piece_surface, (piece_x, piece_y))


# Demo with Full-Screen Background
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Responsive Chess Timer Example")
clock = pygame.time.Clock()

# Load and scale the background image
background_image = pygame.image.load('background_test_1.webp')

# Create a resizable button instance with correct fractions
fraction_of_x = 0.75
fraction_of_y = 0.1
fraction_of_width = 0.15
fraction_of_height = 0.2
fancy_button = Fancy_buttons(screen, fraction_of_x,  fraction_of_y, fraction_of_width, fraction_of_height)
fancy_button_2 = Fancy_buttons(screen, fraction_of_x,  6 * fraction_of_y, fraction_of_width, fraction_of_height)

# Demo loop
running = True
time_left = 30.0
captured_pieces_white = ['♞', '♟', '♝']  # Example captured pieces for display

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update screen size and button size dynamically based on new window size
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            background_image = pygame.transform.scale(background_image, (event.w, event.h))
            fancy_button.recalculate_dimensions()
            fancy_button_2.recalculate_dimensions()

    # Fill the screen with the background image
    screen.blit(background_image, (0, 0))

    # Simulate timer countdown
    time_left -= clock.get_time() / 1000
    if time_left < 0:
        time_left = 30  # Reset for demonstration

    # Draw the timer for "White" and captured pieces
    fancy_button.draw_timer(time_left, 'black', captured_pieces_white)
    fancy_button_2.draw_timer(time_left, 'white', captured_pieces_white)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

        