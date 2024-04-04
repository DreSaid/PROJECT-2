import pygame
import serial
import sys
import math
import time

#15cm/s

# Initialize Pygame
pygame.init()


# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Etch-a-Sketch")


# Function to draw grid lines
def draw_grid():
    # Calculate grid spacing based on the desired range of the grid and screen dimensions
    grid_range = 75  # Range of the grid (from -150 to 150)
    grid_spacing = min(width, height) // (2 * grid_range)  # Spacing between grid lines
    
    # Define scale parameters
    grid_color = (0, 0, 0)  # Color for grid lines (black)
    origin_x, origin_y = width // 2, height // 2  # Define the origin at the middle of the screen

    # Draw vertical grid lines and label increments
    for i in range(-grid_range, grid_range + 1, 10):
        pygame.draw.line(screen, grid_color, (origin_x + i * grid_spacing, 0), (origin_x + i * grid_spacing, height))

        # Labeling
        font = pygame.font.Font(None, 24)
        if i < 0:
            text = font.render(str(-abs(i)), True, (0, 0, 0))  # Show negative value below 0
        else:
            text = font.render("+" + str(i), True, (0, 0, 0))  # Show positive value above 0 with "+"

        text_rect = text.get_rect(center=(origin_x + i * grid_spacing, origin_y + 270))  # Center vertically
        screen.blit(text, text_rect)

    # Draw horizontal grid lines and labels
    for i in range(-grid_range, grid_range + 1, 10):
        pygame.draw.line(screen, grid_color, (0, origin_y + i * grid_spacing), (width, origin_y + i * grid_spacing))

        # Labeling
        font = pygame.font.Font(None, 24)
        if i < 0:
            text = font.render("+" + str(abs(i)), True, (0, 0, 0))  # Show positive value with "+"
        else:
            text = font.render("-" + str(abs(i)), True, (0, 0, 0))  # Show negative value

        text_rect = text.get_rect(center=(origin_x - 370, origin_y + i * grid_spacing))
        screen.blit(text, text_rect)


# Function to clear the screen except for the grid lines
def clear_screen():
    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Redraw grid lines
    draw_grid()

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

# Clear the screen to remove all blue drawn lines
clear_screen()

origin_x, origin_y = width // 2, height // 2  # Define the origin at the middle of the screen
prev_x=origin_x
prev_y=origin_y
speed = 0

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
        x_volts, y_volts, metal = map(float, data.split(','))
        # Calculate speed and direction based on joystick inputs
        if y_volts > 3:
            if x_volts < 0.3:
                angle += 2
                speed = 0.15
                 #angle left + fast forward
            elif x_volts > 3:
                angle -= 1.3
                speed = +0.15
                 #angle right and fast forward
            else:
                 speed = 0.323
        elif y_volts < 0.3:
            if x_volts < 0.3:
                angle -= 1.3
                speed = -0.10
                #angle right ? + slow back
            elif x_volts > 3:
                angle += 1.3
                speed = -0.10
                #angle left ? + slow back
            else:
                speed = -0.304
        else: 
            if x_volts < 0.3:
                angle += 2
                #speed?
            elif x_volts > 3:
                angle -= 2
            else:
                speed = 0
        
        

        # Update cursor position based on speed and direction
        x += (speed * math.cos(angle * math.pi / 180))
        y += (speed * math.sin(angle * math.pi / 180))

        # Ensure the cursor stays within the screen bounds
        x = max(-75, min(x, 75))  # Limit x-coordinate to -75 to 75
        y = max(-75, min(y, 75))  # Limit y-coordinate to -75 to 75

        # Map cursor position to screen coordinates with scale and origin adjustment
        origin_x, origin_y = width // 2, height // 2  # Define the origin at the middle of the screen
        cursor_x = int(x * 5) + origin_x
        cursor_y = origin_y - int(y * 5)
        

        # Draw a line from the previous position to the current position
        pygame.draw.line(screen, (0, 0, 255), (prev_x, prev_y), (cursor_x, cursor_y))

        if metal:
            #pygame.draw.circle(screen, (255,0,0), (cursor_x, cursor_y),2)
            # Draw an "X" at the cursor position
            pygame.draw.line(screen, (255, 0, 0), (cursor_x - 10, cursor_y - 10), (cursor_x + 10, cursor_y + 10), 2)  # Diagonal line 1
            pygame.draw.line(screen, (255, 0, 0), (cursor_x + 10, cursor_y - 10), (cursor_x - 10, cursor_y + 10), 2)  # Diagonal line 2



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
