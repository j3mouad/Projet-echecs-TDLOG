import pygame

def perfect_font(button_width, button_height):
    font_size = int(min(button_width, button_height) * 0.5)
    font_size = max(10, min(font_size, 60))
    return pygame.font.SysFont("Comic Sans MS", font_size)

pygame.init()
background_image = pygame.image.load("background_image.png")
fontComic20 = pygame.font.SysFont("Comic Sans MS", 20)
fontComic32 = pygame.font.SysFont("Comic Sans MS", 32)

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

class ChessUI:
    def __init__(self, screen, info_panel_color, button_color = (211, 144, 99), button_hover_color = None, button_selected_color = (72, 41, 38), text_color = (255,255,255)):
        self.screen = screen
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.button_selected_color = button_selected_color
        self.text_color = text_color
        self.info_panel_color = info_panel_color
        self.board_width_ratio = 5 / 8
        self.update_dimensions()
        self.big_screen = False
        self.which_screen = "main screen"
        self.buttons_settings = []
        self.buttons_main = []
        self.play_white = True
        self.play_against_human = True
        self.chess_game_mode = "Classic"
        self.click_play_game = False
        self.click_multiplayer = False
    def update_dimensions(self):
        self.buttons_main = []
        self.buttons_settings = []
        screen_width, screen_height = self.screen.get_size()
        self.board_width = screen_width * self.board_width_ratio
        self.rectangle_width = self.board_width / 8
        self.rectangle_height = screen_height / 8

    def draw_board(self):
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
        width, height = self.screen.get_size()
        scaled_image = pygame.transform.scale(background_image, (width, height))
        self.screen.blit(scaled_image, (0, 0))
        button_width = 0.25 * width
        button_height = 0.1 * height

        fontComic = perfect_font(button_width, button_height)
        text_play_game = fontComic.render("play game", True, self.text_color)
        text_multiplayer = fontComic.render("Multiplayer", True, self.text_color)
        text_settings = fontComic.render(" settings  ", True,  self.text_color)
        
        button_play_game = pygame.Surface((button_width, button_height))
        button_multiplayer = pygame.Surface((button_width, button_height))
        button_settings = pygame.Surface((button_width, button_height))

        button_play_game.fill(self.button_color)
        button_multiplayer.fill(self.button_color)
        button_settings.fill(self.button_color)

        button_play_game.blit(text_play_game, (button_width / 4, button_height / 7))
        button_multiplayer.blit(text_multiplayer, (button_width / 4, button_height / 7))
        button_settings.blit(text_settings, (button_width / 4, button_height / 7))

        self.screen.blit(button_play_game, ((width - button_width) / 2, (0.2 * height)))
        self.screen.blit(button_multiplayer, ((width - button_width) / 2, (0.4 * height)))
        self.screen.blit(button_settings, ((width - button_width) / 2, (0.6 * height)))

        if self.buttons_main == []:
            self.buttons_main.append({
                        "x": (width - button_width) / 2,
                        "y": 0.2 * height,
                        "width": button_width,
                        "height": button_height,
                        "functionnality": "play_game",
                        })
            self.buttons_main.append({
                        "x": (width - button_width) / 2,
                        "y": 0.4 * height,
                        "width": button_width,
                        "height": button_height,
                        "functionnality": "multiplayer",
                        })
            self.buttons_main.append({
                        "x": (width - button_width) / 2,
                        "y": 0.6 * height,
                        "width": button_width,
                        "height": button_height,
                        "functionnality": "settings",
                        })

                
#this function is very important as it renders
    def settings(self):
        width, height = self.screen.get_size()
        scaled_image = pygame.transform.scale(background_image, (width, height))
        self.screen.blit(scaled_image, (0, 0))

        font = pygame.font.Font(None, int(height * 0.05))

        title_text = font.render("Settings", True, self.text_color)
        title_text_x = (width - title_text.get_width()) // 2
        title_text_y = int(0.05 * height)
        self.screen.blit(title_text, (title_text_x, title_text_y))
        epsilon = width // 100

        button_width = int(0.25 * width)
        button_height = int(0.1 * height)
        spacing = int(0.05 * height)


        color_text = font.render("Select Color:", True, self.text_color)
        color_text_x = int(0.1 * width)
        color_text_y = title_text_y + int(1.5 * font.get_height())
        self.screen.blit(color_text, (color_text_x, color_text_y))

        pygame.draw.polygon(self.screen,
                    self.button_selected_color,
                    [
                        (color_text_x, title_text_y),
                        (color_text_x + 2 * epsilon, title_text_y + 2 * epsilon),
                        (color_text_x + 2 * epsilon, title_text_y + epsilon ),
                        (color_text_x + 4 * epsilon, title_text_y + epsilon ),
                        (color_text_x + 4 * epsilon, title_text_y - epsilon ),
                        (color_text_x + 2 * epsilon, title_text_y -  epsilon ),
                        (color_text_x + 2 * epsilon, title_text_y - 2 * epsilon ),
                        (color_text_x, title_text_y)  # Last point closes the polygon
                    ])
        
        
        #play with white button
        white_button_x = color_text_x
        white_button_y = color_text_y + font.get_height() + spacing
        white_button_rect = pygame.Rect(white_button_x, white_button_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.button_color if not self.play_white else self.button_selected_color, white_button_rect)
        white_text = font.render("White", True, self.text_color)
        self.screen.blit(white_text, (white_button_x + (button_width - white_text.get_width()) // 2,
                                      white_button_y + (button_height - white_text.get_height()) // 2))

        #play with black button
        black_button_x = white_button_x + button_width + spacing
        black_button_y = white_button_y
        black_button_rect = pygame.Rect(black_button_x, black_button_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.button_color if self.play_white else self.button_selected_color, black_button_rect)
        black_text = font.render("Black", True, self.text_color)
        self.screen.blit(black_text, (black_button_x + (button_width - black_text.get_width()) // 2,
                                      black_button_y + (button_height - black_text.get_height()) // 2))

        mode_text = font.render("Select Game Mode:", True, self.text_color)
        mode_text_x = color_text_x
        mode_text_y = white_button_y + button_height + (2 * spacing)
        self.screen.blit(mode_text, (mode_text_x, mode_text_y))

       
        mode_button_width = button_width
        mode_button_spacing = int(0.03 * width)
        #classic buttons
        classic_button_x = color_text_x
        classic_button_y = mode_text_y + font.get_height() + spacing
        classic_button_rect = pygame.Rect(classic_button_x, classic_button_y, mode_button_width, button_height)
        pygame.draw.rect(self.screen, self.button_selected_color if self.chess_game_mode == "Classic" else self.button_color, classic_button_rect)
        classic_text = font.render("Classic", True, self.text_color)
        self.screen.blit(classic_text, (classic_button_x + (mode_button_width - classic_text.get_width()) // 2,
                                        classic_button_y + (button_height - classic_text.get_height()) // 2))
        
        #blitz button
        blitz_button_x = classic_button_x + mode_button_width + mode_button_spacing
        blitz_button_y = classic_button_y
        blitz_button_rect = pygame.Rect(blitz_button_x, blitz_button_y, mode_button_width, button_height)
        pygame.draw.rect(self.screen, self.button_selected_color if self.chess_game_mode == "Blitz" else self.button_color, blitz_button_rect)
        blitz_text = font.render("Blitz", True, self.text_color)
        self.screen.blit(blitz_text, (blitz_button_x + (mode_button_width - blitz_text.get_width()) // 2,
                                      blitz_button_y + (button_height - blitz_text.get_height()) // 2))
        
        #rapid button
        rapid_button_x = blitz_button_x + mode_button_width + mode_button_spacing
        rapid_button_y = blitz_button_y
        rapid_button_rect = pygame.Rect(rapid_button_x, rapid_button_y, mode_button_width, button_height)
        pygame.draw.rect(self.screen, self.button_selected_color if self.chess_game_mode == "Rapid" else self.button_color, rapid_button_rect)
        rapid_text = font.render("Rapid", True, self.text_color)
        self.screen.blit(rapid_text, (rapid_button_x + (mode_button_width - rapid_text.get_width()) // 2,
                                      rapid_button_y + (button_height - rapid_text.get_height()) // 2))

        play_mode_text = font.render("Player:", True, self.text_color)
        play_mode_text_x = int(0.1 * width)
        play_mode_text_y = rapid_button_y + button_height + (2 * spacing)
        self.screen.blit(play_mode_text, (play_mode_text_x, play_mode_text_y))

        #human button
        human_button_x = play_mode_text_x
        human_button_y = play_mode_text_y + font.get_height() + spacing
        human_button_rect = pygame.Rect(human_button_x, human_button_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.button_selected_color if self.play_against_human else self.button_color, human_button_rect)
        human_text = font.render("Play Against Human", True, self.text_color)
        self.screen.blit(human_text, (human_button_x + (button_width - human_text.get_width()) // 2,
                                      human_button_y + (button_height - human_text.get_height()) // 2))
        #AI button
        ai_button_x = human_button_x + button_width + spacing
        ai_button_y = human_button_y
        ai_button_rect = pygame.Rect(ai_button_x, ai_button_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.button_color if self.play_against_human else self.button_selected_color, ai_button_rect)
        ai_text = font.render("Play Against AI", True, self.text_color)
        self.screen.blit(ai_text, (ai_button_x + (button_width - ai_text.get_width()) // 2,
                                   ai_button_y + (button_height - ai_text.get_height()) // 2))
        """
here if the buttons attribute is an empty list we will append in it the buttons, it is helpful 
to check after if the user clicked or hovered over some buttons as we need the rectangles position
        """ 
        if self.buttons_settings == []:
            self.buttons_settings.append({
                                "x": color_text_x,
                                "y" : title_text_y - epsilon,
                                "width" : 4*epsilon,
                                "height" : 4*epsilon,
                                "functionnality" : "return",
                                })
            self.buttons_settings.append({
                                "x": white_button_x,
                                "y": white_button_y,
                                "width" : button_width,
                                "height" : button_height,
                                "functionnality" : "white_button",  
                                })
            self.buttons_settings.append({
                                "x": black_button_x,
                                "y": black_button_y,
                                "width" : button_width,
                                "height" : button_height,
                                "functionnality" : "black_button",  
                                })
            self.buttons_settings.append({
                                "x": classic_button_x,
                                "y": classic_button_y,
                                "width" : mode_button_width,
                                "height" : button_height,
                                "functionnality" : "Classic",  
                                })
            self.buttons_settings.append({
                                "x": blitz_button_x,
                                "y": blitz_button_y,
                                "width" : mode_button_width,
                                "height" : button_height,
                                "functionnality" : "Blitz",  
                                })
            self.buttons_settings.append({
                                "x": rapid_button_x,
                                "y": rapid_button_y,
                                "width" : mode_button_width,
                                "height" : button_height,
                                "functionnality" : "Rapid",  
                                })
            self.buttons_settings.append({
                                "x": human_button_x,
                                "y": human_button_y,
                                "width" :button_width,
                                "height" : button_height,
                                "functionnality" : "human",  
                                })
            self.buttons_settings.append({
                                "x": ai_button_x,
                                "y": ai_button_y,
                                "width" : button_width,
                                "height" : button_height,
                                "functionnality" : "AI",  
                                })
    def which_screen_to_render(self):
        if self.which_screen == "settings":
            self.settings()
        elif self.which_screen == "main screen":
            self.game_mode_select_page()
        else:
            raise ValueError(f"Invalid screen state: {self.which_screen}")

    def handling_events_logic(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Mouse clicked at:", mouse_pos)
            if self.which_screen == "settings":
                for button in self.buttons_settings:
                    mouse_pos = pygame.mouse.get_pos()
                    if (button["x"] <= mouse_pos[0] <= button["x"] + button["width"] and
                        button["y"] <= mouse_pos[1] <= button["y"] + button["height"]):
                        if button["functionnality"] == "return":
                            self.which_screen = "main screen"                 
                        elif button["functionnality"] == "white_button":
                            self.play_white = True
                        elif button["functionnality"] == "black_button":
                            self.play_white = False
                        elif button["functionnality"] == "Classic":
                            self.chess_game_mode = "Classic"
                        elif button["functionnality"] == "Blitz":
                            self.chess_game_mode = "Blitz"
                        elif button["functionnality"] == "Rapid":
                            self.chess_game_mode = "Rapid"
                        elif button["functionnality"] == "human":
                            self.play_against_human = True
                            print("Human button clicked. play_against_human =", self.play_against_human)
                        elif button["functionnality"] == "AI":
                            self.play_against_human = False
            else:
                for button in self.buttons_main:
                    mouse_pos = pygame.mouse.get_pos()
                    if (button["x"] <= mouse_pos[0] <= button["x"] + button["width"] and
                        button["y"] <= mouse_pos[1] <= button["y"] + button["height"]):
                        if button["functionnality"] == "play_game":
                            self.click_play_game = True
                        elif button["functionnality"] == "multiplayer":
                            self.click_multiplayer = True
                        elif button["functionnality"] == "settings":
                            self.which_screen = "settings"
        self.which_screen_to_render()



