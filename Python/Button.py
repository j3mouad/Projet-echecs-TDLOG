import pygame
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color, shadow_color=(0, 0, 0), shadow_offset=(5, 5), shadow_opacity=100, shadow_blur=10, callback=None):
        """
        Button with an improved shadow effect.

        Parameters:
            x, y (int): Top-left position of the button.
            width, height (int): Dimensions of the button.
            text (str): Text displayed on the button.
            font (pygame.font.Font): Font used for the text.
            color (tuple): Button color.
            hover_color (tuple): Color when hovered.
            text_color (tuple): Text color.
            shadow_color (tuple): Shadow color.
            shadow_offset (tuple): Offset of the shadow (x, y).
            shadow_opacity (int): Transparency of the shadow (0-255).
            shadow_blur (int): Blur radius for the shadow.
            callback (callable): Function to execute on click.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.shadow_opacity = shadow_opacity
        self.shadow_blur = shadow_blur
        self.hovered = False
        self.callback = callback

    def draw_shadow(self, screen):
        """
        Draws a soft shadow for the button.
        """
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset[0]
        shadow_rect.y += self.shadow_offset[1]

        for i in range(self.shadow_blur, 0, -1):
            alpha = self.shadow_opacity * (i / self.shadow_blur)
            shadow_surface = pygame.Surface((shadow_rect.width + i * 2, shadow_rect.height + i * 2), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, (*self.shadow_color, int(alpha)), pygame.Rect(i, i, shadow_rect.width, shadow_rect.height), border_radius=10)
            screen.blit(shadow_surface, (shadow_rect.x - i, shadow_rect.y - i))

    def draw(self, screen):
        """
        Draws the button with shadow and hover effects.
        """
        # Draw shadow first
        self.draw_shadow(screen)

        # Determine current color
        current_color = self.hover_color if self.hovered else self.color

        # Draw button with rounded corners
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Render and center the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def handle_event(self, event):
        """
        Handles hover and click events.
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if self.callback:
                self.callback()
            return True
        return False
def on_button_click():
    print("Button clicked!")

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    # Create a button with enhanced shadow
    button = Button(
        x=300, y=250, width=200, height=60,
        text="Click Me",
        font=font,
        color=(145, 53, 47),
        hover_color=(72, 41, 38),
        text_color=(255, 255, 255),
        shadow_color=(0, 0, 0),
        shadow_offset=(8, 8),
        shadow_opacity=120,
        shadow_blur=15,
        callback=on_button_click
    )

    running = True
    while running:
        screen.fill((30, 30, 30))  # Background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button event
            button.handle_event(event)

        # Draw button
        button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()