import pygame

# Initialize Pygame
pygame.init()


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



# Test chessboard setup
chess_board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

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

