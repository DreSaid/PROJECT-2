import pygame
import serial
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Etch-a-Sketch")
screen.fill((255, 255, 255))  # Fill the screen with white

# Cursor position
x, y = width // 2, height // 2
speed = 5  # Cursor speed

# Initialize the serial port
ser = serial.Serial('COM1', 9600)  # Update with the correct COM port and baud rate

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick values from the serial port
    data = ser.readline().decode().strip()
    if data:
        x_axis, y_axis = map(float, data.split(','))

        # Update cursor position based on joystick inputs
        x += int(x_axis * speed)
        y += int(y_axis * speed)

        # Ensure the cursor stays within the screen bounds
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))

        # Draw a line from the previous position to the current position
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y))

        # Update the display
        pygame.display.flip()

# Close the serial port
ser.close()

# Quit Pygame
pygame.quit()
sys.exit()
