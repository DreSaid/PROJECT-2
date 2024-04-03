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
speed = 2  # Cursor speed

# Previous cursor position
prev_x, prev_y = x, y

# Initialize the serial port
ser = serial.Serial('COM7', 115200)  # Update with the correct COM port and baud rate

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick values from the serial port
    data = ser.readline().decode().strip()
    if data:
        x_volts, y_volts = map(float, data.split(','))

        # Map joystick voltages to cursor movement
        x_axis = (x_volts - 1.615) * speed * -1  # Adjusted for neutral position
        y_axis = (y_volts - 1.615) * speed  # Adjusted for neutral position

        # Update cursor position based on joystick inputs
        x -= int(x_axis)
        y -= int(y_axis)

        # Ensure the cursor stays within the screen bounds
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))

        # Draw a line from the previous position to the current position
        pygame.draw.line(screen, (0, 0, 0), (prev_x, prev_y), (x, y))

        # Update the display
        pygame.display.flip()

        # Update the previous position
        prev_x, prev_y = x, y

# Close the serial port
ser.close()

# Quit Pygame
pygame.quit()
sys.exit()
