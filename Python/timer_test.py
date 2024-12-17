import pygame
import time
from timer import Timer
# Import the Timer class
# from your_module import Timer

pygame.init()

# Test Timer Class
def test_timer():
    # Initialize pygame screen for drawing (not necessary for all tests, but useful for visual validation)
    screen_width = 500
    added_screen_width = 200
    screen_height = 500
    screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
    pygame.display.set_caption("Timer Test")

    # Initialize the timer
    timer = Timer(cooldown=0.5)
    timer.start_timer(10, 10)  # Start with 10 seconds for both players

    # Test 1: Check initial times
    assert timer.white_time == 10, "White timer did not initialize correctly!"
    assert timer.black_time == 10, "Black timer did not initialize correctly!"
    print("Test 1 Passed: Initialization")

    # Test 2: Simulate time update
    time.sleep(1)  # Wait 1 second to simulate elapsed time
    timer.update_timer()
    if timer.turn == "white":
        assert timer.white_time <= 9, "White timer did not update correctly!"
    print("Test 2 Passed: Timer Update")

    # Test 3: Add time
    timer.add_time(5)  # Add 5 seconds to the current player's time
    if timer.turn == "white":
        assert timer.white_time == 14, "White timer did not update correctly after adding time!"
    print("Test 3 Passed: Adding Time")

    # Test 4: Switch turn and update
    timer.turn = "black"  # Switch to black
    timer.update_timer()  # Simulate time update
    assert timer.black_time <= 9, "Black timer did not update correctly!"
    print("Test 4 Passed: Turn Switching and Update")

    # Test 5: Timer runs out
    timer.start_timer(1, 1)  # Set very low times for a quick test
    time.sleep(2)  # Wait longer than the timer duration
    timer.update_timer()
    winner = timer.is_time_up()
    assert winner == "black", f"Expected 'black' to win, but got {winner}!"
    print("Test 5 Passed: Timer Expiry and Winner Check")

    # Visual test for drawing (optional)
    running = True
    while running:
        screen.fill((255, 255, 255))  # Clear screen
        timer.draw_timer(screen, screen_width, screen_height, added_screen_width, "white")
        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        timer.update_timer()  # Continuously update timer
        time.sleep(1)

    print("All tests passed successfully!")

# Run the test
test_timer()
pygame.quit()
