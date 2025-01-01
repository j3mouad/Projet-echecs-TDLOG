from timer import Fancy_buttons
import pygame
def draw_timer_test():
   pygame.init()
   screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
   pygame.display.set_caption("Responsive Chess Timer Example")
   clock = pygame.time.Clock()

   # Load and scale the background image
   background_image = pygame.image.load('background_test_1.webp')

   # Create a resizable button instance with correct fractions
   fraction_of_x = 0.75
   fraction_of_y = 0.1
   fraction_of_width = 0.2
   fraction_of_height = 0.3 
   fancy_button = Fancy_buttons(screen, fraction_of_x, fraction_of_y, fraction_of_width, fraction_of_height)
   fancy_button_2 = Fancy_buttons(screen, fraction_of_x, 6 * fraction_of_y, fraction_of_width, fraction_of_height)

   # Demo loop
   running = True
   time_left = 90.0
   captured_pieces_white = ['wR', 'wP', 'wN', 'wB'] * 4  # Example captured pieces for display
   captured_pieces_black = ['bR', 'bP', 'bN', 'bB'] * 4

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
          time_left = 90  # Reset for demonstration

        # Draw the timer for "Black" and "White" players
       fancy_button.draw_timer(time_left, 'black', captured_pieces_black,50,80)
       fancy_button_2.draw_timer(time_left, 'white', captured_pieces_white,170,200)
       pygame.display.flip()
       clock.tick(30)

   pygame.quit()
   


def draw_timer_options_test():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Test Timer Options")
    clock = pygame.time.Clock()

    # Load and scale the background image
    background_image = pygame.image.load('background_test_1.webp')

    # Create a Fancy_buttons instance to call the method
    fraction_of_x = 0.3
    fraction_of_y = 0.3
    fraction_of_width = 0.6
    fraction_of_height = 0.5
    fancy_button = Fancy_buttons(screen, fraction_of_x, fraction_of_y, fraction_of_width, fraction_of_height)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update screen size dynamically based on window resize
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                background_image = pygame.transform.scale(background_image, (event.w, event.h))
                fancy_button.recalculate_dimensions()

        # Fill the screen with the background image
        screen.blit(background_image, (0, 0))

        # Test the draw_timer_options_1 method
        fancy_button.left_arrow()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def test_pause():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Test Pause Button")
    clock = pygame.time.Clock()

    # Create a Fancy_buttons instance
    fraction_of_x = 0.4
    fraction_of_y = 0.3
    fraction_of_width = 0.2
    fraction_of_height = 0.4
    fancy_button = Fancy_buttons(screen, fraction_of_x, fraction_of_y, fraction_of_width, fraction_of_height)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle resizing
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                fancy_button.recalculate_dimensions()

        # Fill the screen with a background color
        screen.fill((30, 30, 30))

        # Test the pause method
        fancy_button.pause()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Run the test
draw_timer_options_test()

