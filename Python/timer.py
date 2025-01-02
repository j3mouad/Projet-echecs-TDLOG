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
        
        
    def left_arrow(self,color, opacity):
        
        arrow_layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        arrow_left_points = [
        (0, self.height / 2),  # Tip of the arrow
        (self.width / 2, 0),  # Top-left
        (self.width / 2, self.height / 2.25),  # Mid-left
        (self.width, self.height / 2.25),  # Right-most point
        (self.width, self.height / 1.75),
        (self.width / 2, self.height / 1.75),  # Mid-right
        (self.width / 2, self.height),  # Bottom-left
        (0, self.height / 2)  # Back to tip to close
    ]
        x, y, z = color
        pygame.draw.polygon(arrow_layer, (x, y, z, opacity), arrow_left_points)
        self.screen.blit(arrow_layer, (self.x, self.y))
        
    def right_arrow(self, color, opacity):
        
        arrow_layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        arrow_right_points = [
        (0, self.height / 2.25),
        (self.width / 2, self.height / 2.25),
        (self.width / 2, 0),
        (self.width, self.height / 2),
        (self.width / 2, self.height),
        (self.width / 2, self.height / 1.75),
        (0, self.height / 1.75),
        (0, self.height / 2.25),
    ]
        x, y, z = color
        # Draw the arrow on the transparent Surface
        pygame.draw.polygon(arrow_layer, (x, y, z, opacity), arrow_right_points)

        # Blit the transparent Surface onto the main screen at the desired position
        self.screen.blit(arrow_layer, (self.x, self.y))
        
    def pause(self,color, opacity):
        # Create a transparent Surface
        pause_layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Define the dimensions of the pause bars relative to the layer
        bar_width = self.width / 3
        bar_height = self.height

        x, y, z = color
        # Draw the left pause bar on the transparent Surface
        pygame.draw.rect(pause_layer, (x, y, z, opacity), (0, 0, bar_width, bar_height))

        # Draw the right pause bar on the transparent Surface
        pygame.draw.rect(pause_layer, (x, y, z, opacity), ((2 / 3) * self.width, 0, bar_width, bar_height))

        # Blit the transparent Surface onto the main screen at the desired position
        self.screen.blit(pause_layer, (self.x, self.y))

        
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
    
    def draw_control_pannel(self, color, opacity):
        width, height = self.screen.get_size()
        
        width_for_each_icon = self.width // 3
        height_for_each_icon = self.height
        
        padding_x = 0.25 * width_for_each_icon
        padding_y = 0.25 * height_for_each_icon
        
        x1, y1 = self.x + padding_x, self.y + padding_y
        x2, y2 = x1 + width_for_each_icon + 2 * padding_x, self.y + padding_y
        x3, y3 = x2 + width_for_each_icon + 2 * padding_x, self.y + padding_y
          
        left_arrow = Fancy_buttons(self.screen, x1 / width, y1 / height, width_for_each_icon / width, height_for_each_icon / height)
        pause_button = Fancy_buttons(self.screen, x2 / width, y2 / height, width_for_each_icon / width, height_for_each_icon / height)
        right_arrow = Fancy_buttons(self.screen, x3 / width, y3 / height, width_for_each_icon / width, height_for_each_icon / height)
        
        left_arrow.left_arrow(color, opacity)
        pause_button.pause(color, opacity)
        right_arrow.right_arrow(color, opacity)
#(33, 52, 81), (0, 0, 0)
    def draw_main_timer_menu(self, color, opacity):


    # --------------------------------------------------
    # 1) Calculate Button Sizes and Gaps
    # --------------------------------------------------
    # Define a small horizontal gap for spacing between buttons
       button_gap = int(self.width * 0.02)  # 2% of total width as spacing

    # We have 3 buttons and 2 gaps:
    # total_width = 3 * button_width + 2 * button_gap
       button_width = (self.width - 2 * button_gap) // 3
       button_height = self.height // 10

    # Overlay for the remaining window space
       overlay_window_height = self.height - button_height

    # Unpack the color (RGB)
       x, y, z = color

    # --------------------------------------------------
    # 2) Create Button Surfaces
    # --------------------------------------------------
    # Gameplay Button
       overlay_gameplay = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    # Fill
       pygame.draw.rect(
        overlay_gameplay,
        (x, y, z, opacity),
        (0, 0, button_width, button_height),
        border_top_left_radius=20
    )
    # Black Border (width=2)
       pygame.draw.rect(
        overlay_gameplay,
        (0, 0, 0),
        (0, 0, button_width, button_height),
        2,  # border thickness
        border_top_left_radius=20
    )

    # Moves Button
       overlay_moves = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    # Fill
       pygame.draw.rect(
        overlay_moves,
        (x, y, z, opacity),
        (0, 0, button_width, button_height)
    )
    # Black Border
       pygame.draw.rect(
        overlay_moves,
        (0, 0, 0),
        (0, 0, button_width, button_height),
        2  # border thickness
    )

    # Settings Button
       overlay_settings = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    # Fill
       pygame.draw.rect(
        overlay_settings,
        (x, y, z, opacity),
        (0, 0, button_width, button_height),
        border_top_right_radius=20
    )
    # Black Border
       pygame.draw.rect(
        overlay_settings,
        (0, 0, 0),
        (0, 0, button_width, button_height),
        2,  # border thickness
        border_top_right_radius=20
    )

    # --------------------------------------------------
    # 3) Create a Large Overlay for Remaining Window
    # --------------------------------------------------
       overlay_window = pygame.Surface((self.width, overlay_window_height), pygame.SRCALPHA)
    # Fill
       pygame.draw.rect(
        overlay_window,
        (x, y, z, opacity),
        (0, 0, self.width, overlay_window_height)
    )
    # Black Border (optional)
       pygame.draw.rect(
        overlay_window,
        (0, 0, 0),
        (0, 0, self.width, overlay_window_height),
        2  # border thickness
    )

    # --------------------------------------------------
    # 4) Dynamic Text for Buttons
    # --------------------------------------------------
    # Scale font based on button height, clamped between 12 and 40
       text_size = max(12, min(40, int(button_height * 0.5)))
       font = pygame.font.SysFont(None, text_size)

    # Gameplay text
       gameplay_text = font.render("Gameplay", True, (255, 255, 255))
       gameplay_rect = gameplay_text.get_rect(center=(button_width // 2, button_height // 2))
       overlay_gameplay.blit(gameplay_text, gameplay_rect)

    # Moves text
       moves_text = font.render("Moves", True, (255, 255, 255))
       moves_rect = moves_text.get_rect(center=(button_width // 2, button_height // 2))
       overlay_moves.blit(moves_text, moves_rect)

    # Settings text
       settings_text = font.render("Settings", True, (255, 255, 255))
       settings_rect = settings_text.get_rect(center=(button_width // 2, button_height // 2))
       overlay_settings.blit(settings_text, settings_rect)

    # --------------------------------------------------
    # 5) Blit Surfaces onto the Main Screen
    # --------------------------------------------------
    # Button Y-position is self.y
    # Gameplay
       self.screen.blit(overlay_gameplay, (self.x, self.y))
    # Moves => offset by one button + gap
       self.screen.blit(overlay_moves, (self.x + button_width + button_gap, self.y))
    # Settings => offset by two buttons + two gaps
       self.screen.blit(
        overlay_settings,
        (self.x + 2 * (button_width + button_gap), self.y)
    )

    # Large overlay below the buttons
       self.screen.blit(overlay_window, (self.x, self.y + button_height))

        
        
        
        
        
        
        
        
        

