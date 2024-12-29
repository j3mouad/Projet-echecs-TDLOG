import pygame
import sys

pygame.init()

FPS = 60

# ----- COLORS -----
BROWN_LIGHT = (196, 164, 132)   # Lighter brown
BROWN_DARK = (140, 110, 80)     # Darker brown
CREAM = (240, 234, 214)         # Cream for White area
YELLOW_BASE = (225, 200, 50)    # Button base color
YELLOW_HOVER = (255, 255, 100)  # Button hover color
BLACK = (0, 0, 0)
WHITE = (238, 238, 210)

# ----- FONTS -----
TITLE_FONT = pygame.font.SysFont("Arial", 24, bold=True)
BODY_FONT = pygame.font.SysFont("Arial", 20)

def draw_vertical_gradient(surface, rect, top_color, bottom_color):
    """
    Draw a vertical gradient from 'top_color' to 'bottom_color'
    inside the given 'rect' on 'surface'.
    """
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        color = (
            int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio),
            int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio),
            int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio),
        )
        pygame.draw.line(surface, color, (x, y + i), (x + w, y + i))

class FancyButton:
    """
    A simple button class with hover effect.
    """
    def __init__(self, text, rect, font, base_color, hover_color, text_color=BLACK):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, BLACK, self.rect, width=2, border_radius=6)
        surface.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class TimerUI:
    """
    Manages the Timer area on the right 2/5 of the screen:
      - Top (Black) area with a scrollable move list
      - Middle bar with 3 fancy buttons
      - Bottom (White) area with a scrollable move list
    """
    def __init__(self):
        self.black_scroll_offset = 0
        self.white_scroll_offset = 0
        self.black_moves = [f"B{i}" for i in range(1, 21)]
        self.white_moves = [f"W{i}" for i in range(1, 21)]

        self.prev_button = None
        self.pause_button = None
        self.next_button = None
        self.buttons = []

    def draw(self, screen, timer_rect):
        """
        Draw the Timer UI in the given 'timer_rect'.
        """
        draw_vertical_gradient(screen, timer_rect, WHITE, (220, 220, 200))
        pygame.draw.rect(screen, BLACK, timer_rect, width=4, border_radius=15)

        x, y, w, h = timer_rect
        black_height = int(h * 0.45)
        middle_height = int(h * 0.10)
        white_height = h - black_height - middle_height

        black_rect = (x, y, w, black_height)
        middle_rect = (x, y + black_height, w, middle_height)
        white_rect = (x, y + black_height + middle_height, w, white_height)

        self.draw_black_area(screen, black_rect)
        self.draw_middle_buttons(screen, middle_rect)
        self.draw_white_area(screen, white_rect)

    def draw_black_area(self, screen, rect):
        x, y, w, h = rect
        pygame.draw.rect(screen, (250, 250, 250), rect, border_radius=15)

        title_surf = TITLE_FONT.render("Black's Time: 00:00", True, BLACK)
        screen.blit(title_surf, (x + 10, y + 5))

        epsilon_x = 0.15 * w
        epsilon_y = 0.15 * h
        scroll_rect = pygame.Rect(x + epsilon_x, y + epsilon_y, w * 0.7, h * 0.7)

        draw_vertical_gradient(screen, scroll_rect, (250, 250, 250), (210, 210, 210))  # Gray gradient
        pygame.draw.rect(screen, BLACK, scroll_rect, width=2, border_radius=10)

        sub = screen.subsurface(scroll_rect)
        offset = self.black_scroll_offset
        current_y = offset
        for move in self.black_moves:
            move_surf = BODY_FONT.render(move, True, BLACK)
            sub.blit(move_surf, (10, current_y))
            current_y += 30

    def draw_white_area(self, screen, rect):
        x, y, w, h = rect
        pygame.draw.rect(screen, (250, 250, 250), rect, border_radius=15)

        epsilon_x = 0.15 * w
        epsilon_y = 0.15 * h
        scroll_rect = pygame.Rect(x + epsilon_x, y + epsilon_y, w * 0.7, h * 0.7)

        draw_vertical_gradient(screen, scroll_rect, (200, 200, 200), (180, 180, 180))  # Gray gradient
        pygame.draw.rect(screen, BLACK, scroll_rect, width=2, border_radius=10)

        sub = screen.subsurface(scroll_rect)
        offset = self.white_scroll_offset
        current_y = offset
        for move in self.white_moves:
            move_surf = BODY_FONT.render(move, True, BLACK)
            sub.blit(move_surf, (10, current_y))
            current_y += 30

        title_surf = TITLE_FONT.render("White's Time: 00:00", True, BLACK)
        screen.blit(title_surf, (x + 10, y + h - 35))

    def draw_middle_buttons(self, screen, rect):
        self.update_buttons(rect)
        for btn in self.buttons:
            btn.draw(screen)

    def update_buttons(self, rect):
        x, y, w, h = rect
        btn_width = w // 3

        rect_prev = pygame.Rect(x, y, btn_width, h)
        rect_pause = pygame.Rect(x + btn_width, y, btn_width, h)
        rect_next = pygame.Rect(x + 2 * btn_width, y, btn_width, h)

        self.prev_button = FancyButton("<<", rect_prev, TITLE_FONT, (210, 210, 210), YELLOW_HOVER, BLACK)
        self.pause_button = FancyButton("||", rect_pause, TITLE_FONT, (210, 210, 210), YELLOW_HOVER, BLACK)
        self.next_button = FancyButton(">>", rect_next, TITLE_FONT, (210, 210, 210), YELLOW_HOVER, BLACK)

        self.buttons = [self.prev_button, self.pause_button, self.next_button]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.prev_button and self.prev_button.check_click(mouse_pos):
                    print("<< Previous Move clicked!")
                if self.pause_button and self.pause_button.check_click(mouse_pos):
                    print("|| Pause clicked!")
                if self.next_button and self.next_button.check_click(mouse_pos):
                    print(">> Next Move clicked!")

            if event.button == 4:
                self.black_scroll_offset += 15
                self.white_scroll_offset += 15
            if event.button == 5:
                self.black_scroll_offset -= 15
                self.white_scroll_offset -= 15

            self.black_scroll_offset = min(self.black_scroll_offset, 0)
            self.white_scroll_offset = min(self.white_scroll_offset, 0)

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                btn.check_hover(mouse_pos)

def main():
    screen_width = 960
    screen_height = 640
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Timer (Enhanced UI)")

    clock = pygame.time.Clock()
    timer_ui = TimerUI()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            else:
                timer_ui.handle_event(event)

        screen.fill((238, 238, 210))

        board_width = int((3 / 5) * screen_width)
        left_rect = (0, 0, board_width, screen_height)
        pygame.draw.rect(screen, (50, 50, 50), left_rect)

        timer_rect = (board_width, 0, screen_width - board_width, screen_height)
        timer_ui.draw(screen, timer_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
