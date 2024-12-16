import pygame
import time
class Board:
    def __init__(self, screen, rectangle_width, rectangle_height, white_rectangle_color, black_rectangle_color):
        self.screen = screen
        self.rectangle_width = rectangle_width
        self.rectangle_height = rectangle_height
        self.white_rectangle_color = white_rectangle_color
        self.black_rectangle_color = black_rectangle_color
        self.update_dimension()
        self.piece =  {
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
        self.board_state = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.last_selected_rectangle = None 
        self.valid_moves = []
        self.hover_color = (180,180,160)  # Example: Yellow for highlights
        self.select_color = (255, 215, 0)
        self.hovered_rectangle = (0,0) # tuple indicating the position of the last rectangle hovered
        self.selected_rectangle = None # tuple indicating the position of the last rectangle selected
        self.valid_moves = [(0,7),(0,6),(0,5),(0,4),(0,3)] # a list indicating valid moves the piece in the selected_rectangle can do 
    def update_dimension(self):
        width,height = self.screen.get_size()
        self.rectangle_width = width // 8
        self.rectangle_height = height //8

    def draw_rectangle(self, x :int,y :int, color):
        pygame.draw.rect(self.screen, color, (x * self.rectangle_width, y * self.rectangle_height, self.rectangle_width, self.rectangle_height))  

    def draw_little_circle(self, x :int,y :int, color):
        pass
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if (row, col) == self.selected_rectangle:
                    self.draw_rectangle(row, col, self.select_color)
                    for x,y in self.valid_moves:
                        pygame.draw.circle(self.screen, (100,100,80),  
                                   (x * self.rectangle_width + self.rectangle_width // 2,
                                    y * self.rectangle_height + self.rectangle_height // 2), 
                                   min(self.rectangle_width, self.rectangle_height) // 5)
                else:
                    color = self.white_rectangle_color if (row + col) % 2 == 0 else self.black_rectangle_color
                    self.draw_rectangle(row , col, color)
    def draw_pieces(self):
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        for row in range(rows):
            for col in range(cols):
                if self.board_state[row][col] != '--':
                    position = (col*self.rectangle_width, row*self.rectangle_height)
                    piece = self.piece[self.board_state[row][col]]
                    scaled_image = pygame.transform.scale(piece, (self.rectangle_width, self.rectangle_height))
                    self.screen.blit(scaled_image,position)
    def smooth_transition(self, coords_start:tuple, coords_end:tuple, steps:int):
        x_start = coords_start[0] * self.rectangle_width
        y_start = coords_start[1] * self.rectangle_height
        piece_that_will_transition = self.board_state[coords_start[1]][coords_start[0]]
        self.board_state[coords_start[1]][coords_start[0]] = '--'

        assert isinstance(coords_start, tuple) and len(coords_start) == 2, "coords_start must be a tuple of (row,col)"
        assert isinstance(coords_end, tuple) and len(coords_end) == 2, "coords_end must be a tuple of (row,col)"
        assert isinstance(steps,int) and steps > 0, "steps must be a positive integer"
        assert piece_that_will_transition != '--', 'there is no piece here to be able to transition'

        image = self.piece[piece_that_will_transition]
        
        x_end = coords_end[0] * self.rectangle_width
        y_end = coords_end[1] * self.rectangle_height

        step_x = (x_end - x_start)/steps
        step_y = (y_end - y_start)/steps

        clock = pygame.time.Clock()
        while abs(x_start - x_end) > 0.1 or abs(y_start - y_end) > 0.1:
            x_start += step_x
            y_start += step_y
            self.draw_board()
            self.draw_pieces()
            scaled_image = pygame.transform.scale(image, (self.rectangle_width, self.rectangle_height))
            self.screen.blit(scaled_image, (int(x_start), int(y_start)))
            pygame.display.flip()
            clock.tick(60)
        
        scaled_image = pygame.transform.scale(image,(self.rectangle_width,self.rectangle_height))
        self.screen.blit(scaled_image, (int(x_end), int(y_end)))
        pygame.display.flip()
        self.board_state[coords_end[1]][coords_end[0]] = piece_that_will_transition

    def get_the_position_of_the_rectangle_hovered(self, position:tuple):
        x_hovered = position[0]
        y_hovered = position[1]

        int_x_coordinates = x_hovered // self.rectangle_width
        int_y_coordinates = y_hovered // self.rectangle_height


        return int_x_coordinates, int_y_coordinates

    def hover_rectangle(self):
        # get the current rectangle where the mouse is hovering
        mouse_x, mouse_y = pygame.mouse.get_pos()

        int_x_coordinates, int_y_coordinates = self.get_the_position_of_the_rectangle_hovered((mouse_x, mouse_y))
        x_last_hovered, y_last_hovered = self.hovered_rectangle

        if not (0 <= int_x_coordinates < 8 and 0 <= int_y_coordinates < 8):
            return
        
        if not (0 <= x_last_hovered < 8 and 0 <= y_last_hovered < 8):
            return

        image_last_hovered = self.board_state[y_last_hovered][x_last_hovered]
        image_hovered = self.board_state[int_y_coordinates][int_x_coordinates]

        if (int_x_coordinates,int_y_coordinates) != self.selected_rectangle:
            if int_x_coordinates != x_last_hovered or int_y_coordinates != y_last_hovered:
                color = self.white_rectangle_color if (x_last_hovered + y_last_hovered) % 2 == 0 else self.black_rectangle_color

                pygame.draw.rect(self.screen, color, (x_last_hovered*self.rectangle_width , y_last_hovered*self.rectangle_height, self.rectangle_width, self.rectangle_height))
                pygame.draw.rect(self.screen, self.hover_color , (int_x_coordinates*self.rectangle_width, int_y_coordinates*self.rectangle_height, self.rectangle_width, self.rectangle_height))

                if (int_x_coordinates, int_y_coordinates) in self.valid_moves:
                    pygame.draw.circle(self.screen, (100,100,80),  
                                   (int_x_coordinates * self.rectangle_width + self.rectangle_width // 2,
                                    int_y_coordinates * self.rectangle_height + self.rectangle_height // 2), 
                                   min(self.rectangle_width, self.rectangle_height) // 5)
                if image_last_hovered != '--':
                    scaled_image = pygame.transform.scale(self.piece[image_last_hovered],(self.rectangle_width,self.rectangle_height))
                    self.screen.blit(scaled_image, (x_last_hovered*self.rectangle_width,y_last_hovered*self.rectangle_height))

                if image_hovered != '--':
                    scaled_image = pygame.transform.scale(self.piece[image_hovered],(self.rectangle_width,self.rectangle_height))
                    self.screen.blit(scaled_image,(int_x_coordinates*self.rectangle_width,int_y_coordinates*self.rectangle_height))

            else:
                pygame.draw.rect(self.screen, self.hover_color , (int_x_coordinates*self.rectangle_width, int_y_coordinates*self.rectangle_height, self.rectangle_width, self.rectangle_height))
                if (int_x_coordinates, int_y_coordinates) in self.valid_moves:
                    pygame.draw.circle(self.screen, (100,100,80),  
                                   (int_x_coordinates * self.rectangle_width + self.rectangle_width // 2,
                                    int_y_coordinates * self.rectangle_height + self.rectangle_height // 2), 
                                   min(self.rectangle_width, self.rectangle_height) // 5)
                if image_hovered != '--':
                    scaled_image = pygame.transform.scale(self.piece[image_hovered],(self.rectangle_width,self.rectangle_height))
                    self.screen.blit(scaled_image,(int_x_coordinates*self.rectangle_width,int_y_coordinates*self.rectangle_height))
                    
                    
                
        self.hovered_rectangle = (int_x_coordinates, int_y_coordinates)
        pygame.display.update()
    def select_rectangle(self, event, valid_moves:list):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            int_x_coordinates, int_y_coordinates = self.get_the_position_of_the_rectangle_hovered((mouse_x, mouse_y))
            if not (0 <= int_x_coordinates < 8 and 0 <= int_y_coordinates < 8):
                return
            if self.selected_rectangle == None:
                self.selected_rectangle = (int_x_coordinates,int_y_coordinates)
            else:
                self.selected_rectangle = None
    
    

        
        




                
    


        