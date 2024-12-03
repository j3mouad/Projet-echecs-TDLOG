import pygame
import sys
from copy import deepcopy
import time
from random import shuffle
from utils import has_non_empty_list
import math
# Initialisation de Pygame
pygame.init()
click_sound_add_time_button = pygame.mixer.Sound("chess_add_time_sound.wav")  # Ensure you have a click.wav file in the same directory
click_sound_chess=pygame.mixer.Sound("chess_move_soundf.mp3")
screen_width = 500
screen_height = 500
added_screen_width = 400
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
pygame.display.set_caption("Chess")
# Colors
# Define colors
white, grey, red, orange = (255, 255, 255), (128, 128, 128), (255, 0, 0), (255,165,0)
brown, light_brown, highlight_color = (118, 150, 86), (238, 238, 210), (200, 200, 0)
square_size = screen_width // 8
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
button_color = (100, 200, 100)  #green
button_hover_color = (150, 250, 150)  



# Taille de la case
square_size = screen_width // 8
class coords:
    def __init__(self,x,y):
        self.x=x
        self.y=y
# Charger les images des pièces
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

class ChessGame:
    def __init__(self):
        self.screen = screen
        self.chess_board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.chess_board_squares = [
    ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
    ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
    ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
    ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
    ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
    ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
    ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
    ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]
    ]
        
        self.list_of_boards=[self.chess_board for _ in range(10000)]
        self.len_list_of_boards=0 
        self.list_of_times=[[0,0] for _ in range(10000)]
        self.turn = 'white'
        self.player='white'
        self.last_move=[]
        self.possible_moves=[]
        self.winner = None
        self.cooldown=0.5
        self.white_time = -1  # 10 minutes en secondes
        self.black_time = -1
        self.white_king_moved=False
        self.black_king_moved=False
        self.initial_white_time = self.white_time
        self.initial_black_time = self.black_time
        self.last_time_update = pygame.time.get_ticks()
        self.running = True
        self.x_square_clicked=None
        self.y_square_clicked=None

        self.number_of_time_same_piece_clicked= 0
        self.last_click_time=0
        self.is_back_button_pressed=0
        self.white_king_check=False
        self.black_king_check=False
        self.classic=True
        self.selected_piece=[]
        self.pion_passant=False
        self.last_time_back_clicked=0
        self.x_king, self.y_king = -1, -1
        self.white_moves={(-1,-1):[-1]}
        self.black_moves={(-1,-1):[-1]}
        self.rook_moved=[0,0,0,0]
        self.castle=[0,0,0,0]
        self.big_screen = False
    def manage_size(self):
        if self.big_screen:
            width, height = pygame.display.get_window_size()
            screen_width = (5/9)*width
            added_screen_width = (4/9)*width
            screen_height = height
        else:
            screen_width = 500
            screen_height = 500
            added_screen_width = 400

    def time_reg(self,white_time,black_time):
        self.white_time=white_time
        self.black_time=black_time
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = light_brown if (row + col) % 2 == 0 else brown
                pygame.draw.rect(self.screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
    
    def draw_pieces(self):
        font = pygame.font.Font(None, 12)
        for row in range(8):
            for col in range(8):
                text = font.render(self.chess_board_squares[col][row], True, (0, 0, 255)) 
                screen.blit(text, (row*square_size, col*square_size))
                piece = self.chess_board[row][col]
                if piece != '--':
                    resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                    self.screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
                    

    def draw_add_time_button(self):
        self.button_rect = pygame.Rect(screen_width + 20, 200, 250, 80)
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.button_rect)
        else:
            pygame.draw.rect(self.screen, black, self.button_rect)

        font = pygame.font.Font(None, 36)
        button_text = font.render('+ 5 seconds', True, white)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, text_rect)
   
    def handle_add_time_button(self):
        current_time = time.time()  # Get the current time
        
        if pygame.mouse.get_pressed()[0]: 
            # Check if the left mouse button is pressed
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                if (self.number_of_time_same_piece_clicked==0) :
                    self.number_of_time_same_piece_clicked=1
                    return 
                # Check if enough time has passed since the last click
                if current_time - self.last_click_time >= self.cooldown:
                    # Play click sound
                    click_sound_add_time_button.play()

                    if  self.turn== 'white':
                        self.black_time += 5  # Add 5 seconds to black's time
                    else:
                        self.white_time += 5  # Add 5 seconds to white's time

                    self.last_click_time = current_time  # Update the last click time fix this code so it gets to add time in the left mouse click

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, black)
        if (self.white_time<=5):
            white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, red)
        if (self.black_time<=5):
            black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, red)

        if (self.player=='white') :
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(white_timer_surface, (screen_width + 20, 450))
            self.screen.blit(black_timer_surface, (screen_width + 20, 50))
        if (self.player=='black'):
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(black_timer_surface, (screen_width + 20, 450))
            self.screen.blit(white_timer_surface, (screen_width + 20, 50))
    def game_ends(self):
        if (self.white_time<=0 ):
            self.winner = 'black'
            self.running = False
            return True
        if (self.black_time<=0):
            self.winner = 'white'
            self.running = False
            return True
        if (not has_non_empty_list(self.white_moves) and self.turn=='white') :
           if (self.white_king_check):
               self.winner = 'black'
               self.running=False
               return True
           else :
               self.winner = 'Stalemate'
               self.running=False
               return False
        if (not has_non_empty_list(self.black_moves) and self.turn=='black'):
            if (self.black_king_check):
                self.winner = 'white'
                self.running=False
                return True
            else :
                self.winner = 'Stalemate'
                self.running=False
                return False
        
        
    def flip_board(self):
        L= [[self.chess_board[i][j] for j in range(8)] for i in range(7,-1,-1)]
        self.chess_board=deepcopy(L)
    def show_winner(self):
        # Reinitialize Pygame in case it was previously quit
        pygame.init()
        # Set up the new screen
        screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
        pygame.display.set_caption("Winner Announcement")
        screen.fill(white)

        # Render the winner text
        font = pygame.font.Font(None, 72)  # Larger font for visibility
        winner = "No one" if self.winner is None else self.winner
        winner_text = font.render(f'{winner} won!', True, black)
        text_rect = winner_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(winner_text, text_rect)
        # Update the display
        pygame.display.flip()
        # Event loop to keep the window open
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Exit the program gracefully
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False  # Close the winner screen on any key or mouse press

        pygame.quit()


   
    def draw_move_back_button(self):
        # Define button properties
        button_width = 60
        button_height = 50
        button_x = screen_width + 150
        button_y = 300
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Draw button with hover effect
        pygame.draw.rect(self.screen, black if not button_rect.collidepoint(mouse_pos) else button_hover_color, button_rect)

        # Render text on button
        font = pygame.font.Font(None, 24)  # Choose font size and style
        text = font.render("Back", True, white)  # Render text with white color
        text_rect = text.get_rect(center=button_rect.center)  # Center text on button
        self.screen.blit(text, text_rect)

        # Handle click on button
        if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            # Prevent multiple triggers with cooldown and only trigger on mouse button down
            self.handle_back_button_click()

    def handle_back_button_click(self):
        # Logic for what happens when the button is clicked
        time = pygame.time.get_ticks()
        if ((time - self.last_time_back_clicked) <= self.cooldown):
            return
        if (self.len_list_of_boards == 0):
            return
        self.last_time_back_clicked = time
        self.len_list_of_boards-=1
        l=self.len_list_of_boards
        self.white_time, self.black_time = self.list_of_times[l - 1]
        self.chess_board = deepcopy(self.list_of_boards[l - 1])
        self.selected_piece=[]
        self.draw_board()
        self.draw_pieces()
        self.last_move=[]
        self.turn = 'black' if self.turn == 'white' else 'white'
        pygame.display.flip()
        pygame.time.delay(100)
    
    def choose_game(self,width,height):
        # initializing the window
        window = pygame.display.set_mode((screen_width + added_screen_width, screen_height),pygame.RESIZABLE)
        #writing text above
        pygame.display.set_caption("Let's play Chess!")
        
        # Load the background image
        background_image = pygame.image.load("background_image.jpg")
        #adjusting the image to the width and height
        background_image = pygame.transform.scale(background_image, (screen_width + added_screen_width, screen_height))
        #initializing a font variable that will be used to render text
        font = pygame.font.Font(None, 28)
        text = font.render("Choose color and time ", True, black)
        width, height = pygame.display.get_window_size()

        button_width = 0.3*width
        button_height = 0.10*height
        button_margin = 20
        button_x = 0.35*width
        button_y = 0.2*height
        #drawing buttons at the first page
        button_black = pygame.Rect(button_x, button_y, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)
        button_2v2 = pygame.Rect(button_x+button_width+20, button_y +  (button_height + button_margin), button_width, button_height)
        button_random=pygame.Rect(button_x, button_y+4*button_height, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)
        button_rapid = pygame.Rect(button_x, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_classic = pygame.Rect(button_x + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_blitz = pygame.Rect(button_x + button_width+40 , button_y + 2 * (button_height + button_margin), button_width/2, button_height)
        first_choosing=True
        second_choosing = True
        white_time=0
        black_time=0
        
        while first_choosing or second_choosing:
            mouse_pos = pygame.mouse.get_pos()
            # Draw the background image
            window.blit(background_image, (0, 0))
            window.blit(text, (50, 50))
            pygame.draw.rect(window, white if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, white if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)
            black_text = font.render("Black pieces", True, black)
            white_text = font.render("White pieces", True, black)
            window.blit(black_text, (button_x + 10, button_y + 10))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + 10))
            pygame.draw.rect(window, orange if not button_2v2.collidepoint(mouse_pos) else button_hover_color, button_2v2)
            pygame.draw.rect(window, orange if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, orange if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)
            pygame.draw.rect(window, orange if not button_rapid.collidepoint(mouse_pos) else button_hover_color, button_rapid)
            pygame.draw.rect(window, orange if not button_classic.collidepoint(mouse_pos) else button_hover_color, button_classic)
            pygame.draw.rect(window, orange if not button_blitz.collidepoint(mouse_pos) else button_hover_color, button_blitz) 
            pygame.draw.rect(window, orange if not button_random.collidepoint(mouse_pos) else button_hover_color, button_random)
            black_text = font.render("Jouer avec Noirs", True, black)
            white_text = font.render("Jouer avec Blancs", True, black)
            classic_text = font.render("Jeu classique",True, black) 
            blitz_text = font.render("Jeu blitz",True,black)
            rapid_text= font.render("Jeu rapide",True,black)
            twovtwo_text = font.render("Jeu 1 VS 1",True,black)
            random_text=font.render("Jeu de Fisher",True,black)
            window.blit(black_text, (button_x + 10, button_y + (button_height - black_text.get_height()) // 2))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + (button_height - white_text.get_height()) // 2))
            window.blit(classic_text, (button_x + button_width / 2 + button_margin + 10, button_y + 2 * (button_height + button_margin) + (button_height - classic_text.get_height()) // 2))
            window.blit(rapid_text, (button_x +10 , button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(blitz_text, (button_x + 50+button_width, button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(random_text, (button_x +50, button_y + 4 * (button_height) + (button_height - random_text.get_height()) // 2))
            window.blit(twovtwo_text, (button_x+button_width+30, button_y +  (button_height + button_margin) + (button_height - random_text.get_height()) // 2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_black.collidepoint(event.pos):
                        first_choosing = False
                        self.turn = 'black'
                        self.flip_board()
                    
                    elif button_white.collidepoint(event.pos):
                        first_choosing = False
                        self.player = 'white'
                    elif button_classic.collidepoint(event.pos) :
                        second_choosing=False
                        self.time_reg(3600,3600)
                        white_time=3600
                        black_time=3600
                    elif button_rapid.collidepoint(event.pos) : 
                        second_choosing=False
                        self.time_reg(600,600)
                        white_time=600
                        black_time=600
                        self.classic=False
                    elif button_blitz.collidepoint(event.pos) :
                        second_choosing = False
                        self.time_reg(60,60)
                        white_time=60
                        black_time=60
                    elif button_random.collidepoint(event.pos) :
                        shuffle(self.chess_board[0])
                        shuffle(self.chess_board[7])
                    elif  button_2v2.collidepoint(event.pos) : 
                        first_choosing = False
                        self.player = 'white'
        self.list_of_boards[0]=[self.chess_board]
        self.len_list_of_boards+=1
        return (white_time,black_time)    
    def change_player(self) :
        if (self.turn=='white') :
            self.turn='black'
        else :
            self.turn='white'
    def update_timers(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_time_update) // 1000

        if elapsed_time > 0:
            if self.turn == 'white':
                self.white_time -= elapsed_time
            else:
                self.black_time -= elapsed_time
            self.last_time_update = current_time

        if self.white_time <= 0 or self.black_time <= 0:
            self.winner = "black" if self.white_time <= 0 else "white"
    def castling(self) :
        if not (self.classic) : 
            return 
        if  not (self.white_king_check) and not self.white_king_moved :
            if (self.rook_moved[0]==0 and self.chess_board[7][5]=='--' and self.chess_board[7][6]=='--') :
                b = False
                for key in self.black_moves :
                    b= (6,7) in self.black_moves[key] or (5,7) in self.black_moves[key] or b 
                    if (b) :
                        break
                self.castle[0]=not b 
            if (self.rook_moved[1]==0 and self.chess_board[7][1]=='--' and self.chess_board[7][2]=='--' and self.chess_board[7][3]=='--') :
                b = False
                for key in self.black_moves :
                    
                    b= (3,7) in self.black_moves[key] or (2,7) in self.black_moves[key] or (1,7) in self.black_moves[key] 
                    if (b) :
                        break
                self.castle[1] = not b       
         
        if not (self.black_king_check) and not self.black_king_moved :
            if (self.rook_moved[2]== 0 and self.chess_board[0][1]=='--' and self.chess_board[0][2]=='--' and self.chess_board[0][3]=='--') :
                b = False
                for key in self.white_moves :
                    b= (1,0) in self.white_moves or (2,0) in self.white_moves or (3,0) in self.white_moves
                    if (b):
                        break
                self.castle[2] =not  b
            if (self.rook_moved[3]==0 and self.chess_board[0][6]=='--' and self.chess_board[0][5]=='--' ) :
                b = False
                for key in self.white_moves :
                    b= (5,0) in self.white_moves[key] or (6,0) in self.white_moves[key]
                    if (b):
                        break
                self.castle[3] = not b 
                        
    def is_valid_move(self, start: float, end : float):
        x, y = start
        mx, my = end
        start_piece = self.chess_board[y][x]
        end_piece = self.chess_board[my][mx]
        opponent_color = 'b' if self.turn=='w' else 'w' 
        # Ensure the piece belongs to the current player and the destination is valid
        if start_piece == '--' or end_piece[0] == start_piece[0]:
            return False

        piece_type = start_piece[1]
        
        # Pawn moves
        if piece_type == 'P':
            direction = -1 if start_piece[0] == 'w' else 1  # White moves up, black moves down
            if mx == x:  # Moving straight
                if my == y + direction and end_piece == '--':  # Single step
                    return True
                if (y == 1 or y == 6) and my == y + 2 * direction and end_piece == '--' and \
                        self.chess_board[y + direction][x] == '--':  # Double step
                    return True
            elif abs(mx - x) == 1 and my == y + direction:
                # Capture move
                if end_piece != '--':
                    return True
                # En passant capture
                last_move = self.last_move
                print (last_move)# Store last move as (start, end)
                if last_move and self.chess_board[last_move[1][1]][last_move[1][0]][1] == 'P' and abs(last_move[1][1]-last_move[0][1])==2:
                    print(last_move[1])
                    if last_move[1][0] == mx and last_move[1][1]+direction == my : 
                        self.pion_passant = True
                        return True

        # Rook moves
        elif piece_type == 'R':
            if x == mx or y == my:  # Horizontal or vertical move
                step_x = 1 if mx > x else -1 if mx < x else 0
                step_y = 1 if my > y else -1 if my < y else 0
                for i in range(1, max(abs(mx - x), abs(my - y))):
                    if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                        return False
                return True

        # Knight moves
        elif piece_type == 'N':
            if (abs(mx - x) == 2 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 2):
                return True


        # Bishop moves
        elif piece_type == 'B':
            if abs(mx - x) == abs(my - y):  # Diagonal move
                step_x = 1 if mx > x else -1
                step_y = 1 if my > y else -1
                for i in range(1, abs(mx - x)):
                    if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                        return False
                return True


        # King moves
        elif piece_type == 'K':
            if max(abs(mx - x), abs(my - y)) == 1:  # One square in any direction
                return True
            if (start_piece[0]=='w' and not self.white_king_moved ) :
                if (mx==6 and my == 7  and self.castle[0]) :
                    return True
                if (mx==2 and my == 7  and self.castle[1]) :
                    return True
            if (start_piece[0]=='b' and not self.black_king_moved) :
                if (mx==2 and my == 0  and self.castle[2]) :
                    print('ezrfzefze')
                    return True
                if (mx==6 and my == 0  and self.castle[3]) :
                    print('fzefezeedf')
                    return True
        # Queen moves
        elif piece_type == 'Q':
            if abs(mx - x) == abs(my - y) or x == mx or y == my:  # Diagonal, horizontal, or vertical
                step_x = 1 if mx > x else -1 if mx < x else 0
                step_y = 1 if my > y else -1 if my < y else 0
                for i in range(1, max(abs(mx - x), abs(my - y))):
                    if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                        return False
                return True

        return False

    def get_possible_moves(self, x:float, y:float):
        """Returns moves for the piece at (x, y) that don't put its king in check."""
        moves = []
        # Check all potential moves
        for my in range(8):
            for mx in range(8):
                if self.is_valid_move((x, y), (mx, my)):
                    
                    moves.append((mx, my))
        return moves


    def move_piece(self, start: float, x: float, y:float): 
        """Moves the piece from start to (x, y). Handles en passant captures."""
        mx, my = start
        moving_piece = self.chess_board[my][mx]
        direction = -1 if self.turn == 'black' else 1
        if (moving_piece[1]=='K' and abs(mx-x)==2 and self.classic and my==y):
            if (my  == 7 and not self.white_king_moved and not self.white_king_check and self.turn=='white') :
                self.chess_board[y][x]=moving_piece
                self.chess_board[my][mx]='--'
                direction = int((mx-x)/2)
                if(x==6) :
                    self.chess_board[my][7]='--'
                else :
                    self.chess_board[my][0]='--'
                rook = moving_piece[0] + 'R'
                self.chess_board[y][mx-direction]=rook
                self.white_king_moved=True

                return
            if (my==0 and not self.black_king_check and not self.black_king_moved and self.black=='black' ) :
                self.chess_board[y][x]=moving_piece
                self.chess_board[my][mx]='--'
                direction = int((mx-x)/2)
                if(x==6) :
                    self.chess_board[my][7]='--'
                else :
                    self.chess_board[my][0]='--'
                rook = moving_piece[0] + 'R'
                self.chess_board[y][mx-direction]=rook
                self.black_king_moved=True

                return
        if (self.chess_board[my][mx][1]=='K') :
            color = self.chess_board[my][mx][0] 
            if (color=='w') :
                self.white_king_moved=True
            else :
                self.black_king_moved=True
        # Move the piece from start to (x, y)
        
            
        self.chess_board[y][x], self.chess_board[my][mx] = moving_piece, '--'
        if ((y==0 or y==7) and  self.chess_board[y][x][1]=='P') :
            self.chess_board[y][x] = self.chess_board[y][x][0] + 'Q'
            
                    
            
        # Handle en passant capture
        if (self.pion_passant) :
            # Clear the square of the pawn captured via en passant
            print(x,' ',y+direction)
            self.chess_board[y+direction][x] = '--'
            
        
            # Reset en passant if no double-step pawn move occurred
        self.pion_passant = False

    def back_move_piece(self, start, x:float, y:float, piece): 
        """Reverts a move to restore board state."""
        print("this is", piece)
        mx, my = start
        self.chess_board[y][x], self.chess_board[my][mx] = self.chess_board[my][mx], piece

    def is_king_in_check(self):
        """Checks if the player's king is in check."""
        color=self.turn[0]
        king_position = self.get_king_position()
        if not king_position:
            # King not found, possibly captured
            self.running=False
            self.winner = 'black' if color=='w' else 'white'
            
            return True

        x_king, y_king = king_position
        opponent_color = 'b' if color == 'w' else 'w'
        # Check if any opponent piece can capture the king's position
        for y in range(8):
            for x in range(8):
                piece = self.chess_board[y][x]
                if piece[0] == opponent_color :
                    
                    if self.is_valid_move((x, y), (x_king, y_king)):
                        
                        return True

        return False

    def simulate_move_and_check(self, start:list, end:list):
        """Simulates a move and checks if it puts the player's king in check."""
        piece = self.chess_board[start[1]][start[0]]
        target_piece = self.chess_board[end[1]][end[0]]
        
        # Make the move temporarily
        self.chess_board[end[1]][end[0]] = piece
        self.chess_board[start[1]][start[0]] = "--"
        # Check if the king is in check after the move
        in_check = self.is_king_in_check()

        # Undo the move
        self.chess_board[start[1]][start[0]] = piece
        self.chess_board[end[1]][end[0]] = target_piece

        return  not in_check

    def get_valid_moves(self, x_square, y_square):
        """Returns a list of valid moves that do not put the player's own king in check."""
        self.possible_moves = self.get_possible_moves(x_square, y_square)
        valid_moves = [move for move in self.possible_moves if self.simulate_move_and_check((x_square, y_square), move)]
        return valid_moves

    
    def get_king_position(self):
        """Finds and returns the position of the king of the given color."""
        color = self.turn[0]
        king = color + 'K'
        for y in range(8):
            for x in range(8):
                if self.chess_board[y][x] == king:
                    return (x, y)
        return None
    
    def check(self, x_square, y_square):
        """Checks if the move puts the opponent's king in check."""
        if (self.chess_board[y_square][x_square]=='--') :
            return (-1,-1)
        moves = self.get_valid_moves(x_square, y_square)
        color = 'b' if self.turn[0] == 'w' else 'w'
        king = color + 'K'

        for move in moves:
            if self.chess_board[move[1]][move[0]] == king:
                

                return move  # Returns the position of the king in check

        return (-1, -1)
    
    def all_moves(self) :
        if (self.turn=='white') :
            self.white_moves.clear() 
            for y in range(8):
                for x in range(8):
                    if self.chess_board[y][x][0]=='w' :
                        self.white_moves[(x,y)]=self.get_valid_moves(x,y)
        if (self.turn=='black') :
            self.black_moves.clear()
            for y in range(8) :
                for x in range(8) :
                    if self.chess_board[y][x][0]=='b' :
                        self.black_moves[(x,y)]=self.get_valid_moves(x,y)
        
        
    def update_list_of_boards(self) : 
        l = self.len_list_of_boards
        # Ensure the list_of_boards contains independent deep copies of the board (3D list)
        if self.list_of_boards[l-1] != self.chess_board:
            self.list_of_boards[l] = deepcopy(self.chess_board)
            self.list_of_times[l] = [self.white_time, self.black_time]
            self.len_list_of_boards += 1
            
    def draw_king_in_check(self) :
        x_king,y_king=self.x_king,self.y_king
        if x_king==-1 and y_king==-1 : 
            if (self.turn=='white') : 
                self.white_king_check=False
            else :
                self.black_king_check=False
            return
        if (x_king, y_king) != (-1, -1):
            if (self.turn=='white') : 
                self.white_king_check=True
            else :
                self.black_king_check=True
            pygame.draw.rect(screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))
    def draw_selected_piece(self) : 
        if self.selected_piece:
            x, y = self.selected_piece
            if self.turn[0] == self.chess_board[y][x][0]:  # Ensure selected piece belongs to current player
                pygame.draw.rect(screen, grey, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
                for mx, my in self.possible_moves:
                    pygame.draw.rect(screen, grey, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def draw_last_move(self) :
        if len(self.last_move) > 1:
            x, y = self.last_move[0]
            mx, my = self.last_move[1]
            pygame.draw.rect(screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def run(self) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Check if left click
                    x, y = event.pos
                    x_square, y_square = x // square_size, y // square_size
                    # Ensure within board bounds
                    if 0 <= x_square < 8 and 0 <= y_square < 8:
                        if self.selected_piece and (x_square, y_square) in self.possible_moves:
                            self.is_king_in_check()
                            self.move_piece(self.selected_piece, x_square, y_square)
                            click_sound_chess.play()
                            self.last_move = [[self.selected_piece[0], self.selected_piece[1]], [x_square, y_square]]
                            # Check if the move results in a check
                            self.x_king, self.y_king = -1, -1  # Reset king position
                            for i in range(8):
                                for j in range(8):
                                    check_pos = self.check(i, j)
                                   #"" if check_pos != [-1, -1]:  # Update if a check is found
                                    self.x_king, self.y_king = check_pos
                                    if (self.x_king !=-1) : 
                                        break 
                                if self.x_king != -1:
                                    break
                            self.change_player()
                            self.selected_piece, self.possible_moves = None, []
                        elif self.chess_board[y_square][x_square][0]==self.turn[0]:
                            self.selected_piece = (x_square, y_square)
                            self.all_moves()
                            if (self.turn=='white') : 
                                self.possible_moves = deepcopy(self.white_moves[(x_square, y_square)])  # Only get valid moves
                            else :
                                self.possible_moves = deepcopy(self.black_moves[(x_square, y_square)])  # Only get valid moves
        pygame.display.flip()
    def from_float_to_int_coordinates(self, float_coords:coords ):
        x_square = math.floor(float_coords.x / square_size) 
        y_square = 7-math.floor(float_coords.y / square_size) 
        return coords(x_square,y_square)
    def get_point_in_topleft_square(self, int_coords:coords):
        x_coordinates = int_coords.x*square_size
        y_coordinates = (7-int_coords.y)*square_size
        return coords(x_coordinates,y_coordinates)
    def translation1(self ,initial_coords: coords, final_coords:coords, steps:int):
        initial_square = self.get_point_in_topleft_square(initial_coords)
        final_square = self.get_point_in_topleft_square(final_coords)
        piece = self.chess_board[7-initial_coords.y][initial_coords.x]
        self.chess_board[7-initial_coords.y][initial_coords.x] = '--'
        delta_x = (final_square.x-initial_square.x)/steps
        delta_y = (final_square.y-initial_square.y)/steps
        resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
        for i in range(steps):
            initial_square.x+=delta_x
            initial_square.y+=delta_y
            current_square = self.get_point_in_topleft_square(initial_square)
            self.draw_board()
            self.draw_pieces()
            for i in range(-1,2):
                for j in range(-1,2):
                    color = light_brown if (i + j + current_square.x + current_square.y) % 2 == 1 else brown
                    pygame.draw.rect(screen, color, (current_square.x+i, current_square.y+i, square_size, square_size))        
                    self.screen.blit(resized_piece, pygame.Rect(initial_square.x, initial_square.y,square_size,square_size))
                    pygame.display.flip()
                    pygame.time.delay(1)
        self.chess_board[7-final_coords.y][final_coords.x] = piece
        pygame.display.flip()
