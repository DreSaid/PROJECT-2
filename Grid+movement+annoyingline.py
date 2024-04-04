import pygame
import serial
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Etch-a-Sketch")
screen.fill((255, 255, 255))  # Fill the screen with white

# Calculate grid spacing based on the desired range of the grid and screen dimensions
grid_range = 75  # Range of the grid (from -150 to 150)
grid_spacing = min(width, height) // (2 * grid_range)  # Spacing between grid lines

# Define scale parameters
grid_color = (200, 200, 200)  # Color for grid lines
origin_x, origin_y = width // 2, height // 2  # Define the origin at the middle of the screen

# Draw grid lines and label increments
for i in range(-grid_range, grid_range + 1, 10):
    # Vertical grid lines
    pygame.draw.line(screen, grid_color, (origin_x + i * grid_spacing, 0), (origin_x + i * grid_spacing, height))
    
    # Labeling
    font = pygame.font.Font(None, 24)
    if i < 0:
        text = font.render(str(-abs(i)), True, (0, 0, 0))  # Show negative value below 0
    else:
        text = font.render("+" + str(i), True, (0, 0, 0))  # Show positive value above 0 with "+"
    
    text_rect = text.get_rect(center=(origin_x + i * grid_spacing, origin_y + 270))  # Center vertically
    screen.blit(text, text_rect)



# Horizontal grid lines and labels
for i in range(-grid_range, grid_range + 1, 10):
    # Horizontal grid lines
    pygame.draw.line(screen, grid_color, (0, origin_y + i * grid_spacing), (width, origin_y + i * grid_spacing))
    
    # Labeling
    font = pygame.font.Font(None, 24)
    if i < 0:
        text = font.render("+" + str(abs(i)), True, (0, 0, 0))  # Show positive value with "+"
    else:
        text = font.render("-" + str(abs(i)), True, (0, 0, 0))  # Show negative value
    
    text_rect = text.get_rect(center=(origin_x - 370 , origin_y + i * grid_spacing))
    screen.blit(text, text_rect)



# Cursor position
x, y = 0, 0  # Initialize cursor position at the origin

# Previous cursor position
prev_x, prev_y = x, y

# Initialize the serial port
ser = serial.Serial('COM4', 115200)  # Update with the correct COM port and baud rate

# Angle and turning speed
angle = 90
turn_speed = 75  # Degrees per second

# Game loop
running = True
last_time = time.time()  # Record the initial time
while running:
    current_time = time.time()  # Record the current time
    elapsed_time = current_time - last_time  # Calculate the elapsed time since the last iteration
    last_time = current_time  # Update the last time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick values from the serial port
    data = ser.readline().decode().strip()
    if data:
        x_volts, y_volts = map(float, data.split(','))

        # Calculate speed and direction based on joystick inputs
        if y_volts < 1.6:
            speed = -(y_volts - 1.6) * 1  # Reverse speed
        elif y_volts > 1.65:
            speed = -(y_volts - 1.65) * 1  # Forward speed
        else:
            speed = 0  # Neutral

        # Calculate the angle of the robot's movement
        if x_volts >= 1.60 and x_volts <= 1.62:  # Neutral, hold direction
            pass
        elif x_volts < 0.3:
            angle += turn_speed * elapsed_time  # Spin left
            speed = 0
        elif x_volts >= 0.3 and x_volts < 1.62:
            angle += turn_speed * (1.62 - x_volts) / 1.6 * elapsed_time  # Slightly turn left
        elif x_volts > 1.62 and x_volts <= 3.0:
            angle -= turn_speed * (x_volts - 1.62) / 1.58 * elapsed_time  # Slightly turn right
        elif x_volts >= 3.0:
            angle -= turn_speed * elapsed_time  # Spin right
            speed = 0

        # Update cursor position based on speed and direction
        x += (speed * math.cos(angle * math.pi / 180))
        y += (speed * math.sin(angle * math.pi / 180))

        # Ensure the cursor stays within the screen bounds
        x = max(-grid_range, min(x, grid_range))  # Limit x-coordinate to -grid_range to grid_range
        y = max(-grid_range, min(y, grid_range))  # Limit y-coordinate to -grid_range to grid_range

        # Map cursor position to screen coordinates with scale and origin adjustment
        cursor_x = int(x * grid_spacing) + origin_x
        cursor_y = origin_y - int(y * grid_spacing)

        # Draw a line from the previous position to the current position
        pygame.draw.line(screen, (0, 0, 0), (prev_x, prev_y), (cursor_x, cursor_y))

        # Update the display
        pygame.display.flip()

        # Update the previous position
        prev_x, prev_y = cursor_x, cursor_y

    # Print current speed and angle
    print("Current speed:", speed)
    print("Current angle:", angle)

# Close the serial port
ser.close()

# Quit Pygame
pygame.quit()
