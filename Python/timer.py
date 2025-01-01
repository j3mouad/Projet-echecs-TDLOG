import pygame
from typing import Literal

# Load chess piece images
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

# Load clock images
white_clock = pygame.image.load('white_clock.png')
black_clock = pygame.image.load('black_clock.png')


class Fancy_buttons:
    def __init__(self, screen, fraction_of_x, fraction_of_y, fraction_of_width, fraction_of_height):
        assert fraction_of_x + fraction_of_width <= 1, "fraction_of_x + fraction_of_width > 1"
        assert fraction_of_y + fraction_of_height <= 1, "fraction_of_y + fraction_of_height > 1"
        
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

    def recalculate_dimensions(self):
        width, height = self.screen.get_size()
        self.x = self.fraction_of_x * width
        self.y = self.fraction_of_y * height
        self.width = self.fraction_of_width * width
        self.height = self.fraction_of_height * height
        
        
    def left_arrow(self):

        arrow_left_points = [
        (self.x, self.y + self.height / 2),  # Tip of the arrow
        (self.x  + self.width / 2, self.y),  # Top-left
        (self.x  + self.width / 2, self.y + self.height / 2.25),  # Mid-left
        (self.x  + self.width, self.y + self.height / 2.25),  # Right-most point
        (self.x  + self.width, self.y +  self.height / 1.75),
        (self.x  + self.width / 2, self.y + self.height / 1.75),  # Mid-right
        (self.x  + self.width / 2, self.y + self.height),  # Bottom-left
        (self.x , self.y + self.height / 2)  # Back to tip to close
    ]
        pygame.draw.polygon(self.screen, (255, 255, 255), arrow_left_points)
    
    def pause(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.width / 4, self.height))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x + 0.75 * self.width, self.y ,self.width / 4, self.height))
        
    def pause_button(self):
        pass
    def draw_timer_options(self, width, height):
        # Divide the width into three equal sections
        section_width = width // 3
        icon_height = height  # Icons will have the same height as the provided height

        # Create the surface for the timer options
        options_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        options_surface.fill((0, 0, 0, 0))  # Transparent background

        # Arrow pointing left
        arrow_left_points = [
        (section_width * 0.2, icon_height // 2),  # Tip of the arrow
        (section_width * 0.5, icon_height * 0.2),  # Top corner
        (section_width * 0.5, icon_height * 0.8)   # Bottom corner
        ]
        pygame.draw.polygon(options_surface, (255, 255, 255), arrow_left_points)

        # Pause button
        pause_rect_width = section_width * 0.1
        gap_between_rects = pause_rect_width * 0.5
        rect1_x = section_width + section_width * 0.5 - gap_between_rects
        rect2_x = rect1_x + gap_between_rects + pause_rect_width

        rect1 = (rect1_x, icon_height * 0.2, pause_rect_width, icon_height * 0.6)
        rect2 = (rect2_x, icon_height * 0.2, pause_rect_width, icon_height * 0.6)

        pygame.draw.rect(options_surface, (255, 255, 255), rect1)
        pygame.draw.rect(options_surface, (255, 255, 255), rect2)

        # Arrow pointing right
        arrow_right_points = [
        (section_width * 2.5, icon_height // 2),  # Tip of the arrow
        (section_width * 2.2, icon_height * 0.2),  # Top corner
        (section_width * 2.2, icon_height * 0.8)   # Bottom corner
        ]
        pygame.draw.polygon(options_surface, (255, 255, 255), arrow_right_points)

        # Blit the options surface onto the main screen
        self.screen.blit(options_surface, (self.x, self.y + self.height + 10))

    def draw_timer(self, time: float, player: Literal['white', 'black'], captured_pieces: list[str],opacity1,opacity2):
        """
        Draw the timer in MM:SS format and captured pieces for a player.
        """
        int_width = int(self.width)
        int_height = int(self.height)

        # Validate dimensions
        if int_width <= 0 or int_height <= 0:
            raise ValueError(f"Invalid Surface dimensions: width={int_width}, height={int_height}")
        if int_width > 2000 or int_height > 2000:
            raise ValueError(f"Surface too large: width={int_width}, height={int_height}")

        # Draw background rectangles
        overlay1 = pygame.Surface((int_width, int_height // 2), pygame.SRCALPHA)
        pygame.draw.rect(overlay1, (0, 0, 0, opacity1), (0, 0, int_width, int_height // 3.5), border_top_left_radius=20, border_top_right_radius=20)

        overlay2 = pygame.Surface((int_width, int_height // 2), pygame.SRCALPHA)
        pygame.draw.rect(overlay2, (0, 0, 0, opacity2), (0, 0, int_width, int_height // 2), border_bottom_left_radius=20, border_bottom_right_radius=20)

        self.screen.blit(overlay1, (self.x, self.y))
        self.screen.blit(overlay2, (self.x, self.y + int_height // 3.5))

        # Display player clock icon
        if player == "white":
            scaled_white_clock = pygame.transform.scale(white_clock, (int(0.5 * self.width), int(0.3 * self.height)))
            self.screen.blit(scaled_white_clock, (self.x - 0.1 * self.width, self.y))
        else:
            scaled_black_clock = pygame.transform.scale(black_clock, (int(0.5 * self.width), int(0.3 * self.height)))
            self.screen.blit(scaled_black_clock, (self.x - 0.1 * self.width, self.y))

        # Convert time to MM:SS format
        minutes = int(time) // 60
        seconds = int(time) % 60
        timer_text = f"{minutes:02}:{seconds:02}"

        # Timer font and position
        timer_font_size = max(20, int(self.height * 0.2))
        timer_font = pygame.font.SysFont('Arial', timer_font_size, bold=True)
        timer_surface = timer_font.render(timer_text, True, (255, 255, 255) if time < 10 else (255, 255, 255))
        self.screen.blit(timer_surface, (self.x + self.width * 0.35, self.y + int(self.height * 0.05)))

        # Draw captured pieces
        piece_size = max(20, int(self.height * 0.1))
        row_capacity = int(self.width // (piece_size))
        rows = (len(captured_pieces) + row_capacity - 1) // row_capacity

        for row in range(rows):
            for col in range(row_capacity):
                idx = row * row_capacity + col
                if idx >= len(captured_pieces):
                    break
                piece = captured_pieces[idx]
                if piece in pieces_images:
                    piece_image = pygame.transform.scale(pieces_images[piece], (piece_size, piece_size))
                    piece_x = self.x + col * (piece_size)
                    piece_y = self.y + self.height // 3.5 + row * (piece_size)
                    self.screen.blit(piece_image, (piece_x, piece_y))


