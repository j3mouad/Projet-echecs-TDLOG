import pygame

def perfect_font(button_width, button_height):
    """
    Adjusts and returns a Pygame font based on the button dimensions.

    Parameters:
        button_width (int): The width of the button.
        button_height (int): The height of the button.

    Returns:
        pygame.font.Font: A dynamically adjusted Pygame font object.
    """
    # Calculate font size as a fraction of button dimensions
    # Experimentally, we use 50% of the button height or adjust as needed
    font_size = int(min(button_width, button_height) * 0.5)

    # Set minimum and maximum font sizes for stability
    font_size = max(10, min(font_size, 60))  # Ensure font size is between 10 and 60

    # Return a dynamically created font
    return pygame.font.SysFont("Comic Sans MS", font_size)


# Initialize Pygame
pygame.init()
background_image = pygame.image.load("background_image.png")
fontComic20  = pygame.font.SysFont("Comic Sans MS", 20)
fontComic32 = pygame.font.SysFont("Comic Sans MS", 32)

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

# ChessUI class for drawing
class ChessUI:
    def __init__(self, screen, light_color, dark_color, info_panel_color):
        self.screen = screen
        self.light_color = light_color
        self.dark_color = dark_color
        self.info_panel_color = info_panel_color
        self.board_width_ratio = 5 / 8  # Fraction of the screen width for the chessboard
        self.update_dimensions()
        self.rectangle_width = None
        self.rectangle_height = None
        self.big_screen = False
    def update_dimensions(self):
        # Calculate dimensions dynamically based on screen size
        screen_width, screen_height = self.screen.get_size()
        self.board_width = screen_width * self.board_width_ratio
        self.rectangle_width = self.board_width / 8
        self.rectangle_height = screen_height / 8

    def draw_board(self):
        # Draw the chessboard
        self.update_dimensions()
        for row in range(8):
            for col in range(8):
                color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        col * self.rectangle_width,
                        row * self.rectangle_height,
                        self.rectangle_width,
                        self.rectangle_height
                    )
                )

    def draw_pieces(self, chess_board):
        # Draw the pieces
        self.update_dimensions()
        for row in range(8):
            for col in range(8):
                piece = chess_board[row][col]
                if piece != '--':
                    resized_piece = pygame.transform.scale(
                        pieces_images[piece],
                        (int(self.rectangle_width), int(self.rectangle_height))
                    )
                    self.screen.blit(
                        resized_piece,
                        (col * self.rectangle_width, row * self.rectangle_height)
                    )

    def draw_info_panel(self):
        screen_width, screen_height = self.screen.get_size()
        info_panel_x = self.board_width  
        pygame.draw.rect(
            self.screen,
            self.info_panel_color,
            pygame.Rect(info_panel_x, 0, screen_width - info_panel_x, screen_height)
        )
    def game_mode_select_page(self):
        width,height = self.screen.get_size()
        scaled_image = pygame.transform.scale(background_image,(width,height))
        self.screen.blit(scaled_image,(0,0))
        button_width = 0.25*width
        button_height = 0.1*height

        #initializing text in buttons depending on the size of the screen(small screen - big screen)
        fontComic  = perfect_font(button_width,button_height)

        text_play_game = fontComic.render("play game",True,(0,0,0))
        text_multiplayer = fontComic.render("Multiplayer",True,(0,0,0))
        text_settings = fontComic.render(" settings  ",True,(0,0,0))
        
        #initializing buttons
        button_play_game = pygame.Surface((button_width,button_height))
        button_multiplayer = pygame.Surface((button_width,button_height))
        button_settings = pygame.Surface((button_width,button_height))

        #coloring buttons
        color = (145,53,47)
        button_play_game.fill(color)
        button_multiplayer.fill(color)
        button_settings.fill(color)

        #rendering text on buttons
        button_play_game.blit(text_play_game,(button_width/4,button_height/7))
        button_multiplayer.blit(text_multiplayer,(button_width/4,button_height/7))
        button_settings.blit(text_settings,(button_width/4,button_height/7))

        #rendering the buttons on the screen
        self.screen.blit(button_play_game,((width - button_width) /2,(0.2 * height)))
        self.screen.blit(button_multiplayer,((width - button_width) /2,(0.4 * height)))
        self.screen.blit(button_settings,((width - button_width) /2,(0.6 * height)))
    def settings(self, play_with_white: bool, chess_game_mode: str):
            # Get current screen size
            width, height = self.screen.get_size()

            # Scale and blit the background image
            scaled_image = pygame.transform.scale(background_image, (width, height))
            self.screen.blit(scaled_image, (0, 0))

            # Fonts and Colors
            font = pygame.font.Font(None, int(height * 0.05))  # Font size scales with screen height
            text_color = (0,0,0)  # White text color
            button_color = (145,53,47)  # Light gray button color
            button_hover_color = (72, 41, 38)  # Slightly lighter button color

            # Title Text
            title_text = font.render("Settings", True, text_color)
            title_text_x = (width - title_text.get_width()) // 2
            title_text_y = int(0.05 * height)
            self.screen.blit(title_text, (title_text_x, title_text_y))

            # Draw "Select Color" Section
            color_text = font.render("Select Color:", True, text_color)
            color_text_x = int(0.1 * width)
            color_text_y = title_text_y + int(1.5 * font.get_height())
            self.screen.blit(color_text, (color_text_x, color_text_y))

            # Draw Color Buttons (White and Black)
            button_width = int(0.25*width)
            button_height = int(0.1*height)
            spacing = int(0.05 * height)  # Space between buttons

            # White Button
            white_button_x = color_text_x
            white_button_y = color_text_y + font.get_height() + spacing
            white_button_rect = pygame.Rect(white_button_x, white_button_y, button_width, button_height)
            pygame.draw.rect(self.screen, button_color if not play_with_white else button_hover_color, white_button_rect)
            white_text = font.render("White", True, text_color)
            self.screen.blit(white_text, (white_button_x + (button_width - white_text.get_width()) // 2,
                                  white_button_y + (button_height - white_text.get_height()) // 2))

            # Black Button
            black_button_x = white_button_x + button_width + spacing
            black_button_y = white_button_y
            black_button_rect = pygame.Rect(black_button_x, black_button_y, button_width, button_height)
            pygame.draw.rect(self.screen, button_color if play_with_white else button_hover_color, black_button_rect)
            black_text = font.render("Black", True, text_color)
            self.screen.blit(black_text, (black_button_x + (button_width - black_text.get_width()) // 2,
                                  black_button_y + (button_height - black_text.get_height()) // 2))

            # Draw "Select Game Mode" Section
            mode_text = font.render("Select Game Mode:", True, text_color)
            mode_text_x = color_text_x
            mode_text_y = white_button_y + button_height + (2 * spacing)
            self.screen.blit(mode_text, (mode_text_x, mode_text_y))

            # Draw Game Mode Buttons (Classic, Blitz, Rapid)
            mode_button_width = button_width
            mode_button_spacing = int(0.03 * width)

            # Classic Button
            classic_button_x = color_text_x
            classic_button_y = mode_text_y + font.get_height() + spacing
            classic_button_rect = pygame.Rect(classic_button_x, classic_button_y, mode_button_width, button_height)
            pygame.draw.rect(self.screen, button_hover_color if chess_game_mode == "Classic" else button_color, classic_button_rect)
            classic_text = font.render("Classic", True, text_color)
            self.screen.blit(classic_text, (classic_button_x + (mode_button_width - classic_text.get_width()) // 2,
                                    classic_button_y + (button_height - classic_text.get_height()) // 2))

            # Blitz Button
            blitz_button_x = classic_button_x + mode_button_width + mode_button_spacing
            blitz_button_y = classic_button_y
            blitz_button_rect = pygame.Rect(blitz_button_x, blitz_button_y, mode_button_width, button_height)
            pygame.draw.rect(self.screen, button_hover_color if chess_game_mode == "Blitz" else button_color, blitz_button_rect)
            blitz_text = font.render("Blitz", True, text_color)
            self.screen.blit(blitz_text, (blitz_button_x + (mode_button_width - blitz_text.get_width()) // 2,
                                  blitz_button_y + (button_height - blitz_text.get_height()) // 2))

            # Rapid Button
            rapid_button_x = blitz_button_x + mode_button_width + mode_button_spacing
            rapid_button_y = blitz_button_y
            rapid_button_rect = pygame.Rect(rapid_button_x, rapid_button_y, mode_button_width, button_height)
            pygame.draw.rect(self.screen, button_hover_color if chess_game_mode == "Rapid" else button_color, rapid_button_rect)
            rapid_text = font.render("Rapid", True, text_color)
            self.screen.blit(rapid_text, (rapid_button_x + (mode_button_width - rapid_text.get_width()) // 2,
                                  rapid_button_y + (button_height - rapid_text.get_height()) // 2))

    def draw_timer():
        pass



        






