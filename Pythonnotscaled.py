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

# Cursor position
x, y = width // 2, height // 2
speed = 1  # Cursor speed

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
            angle -= turn_speed * elapsed_time  # Spin left
            speed = 0
        elif x_volts >= 0.3 and x_volts < 1.62:
            angle -= turn_speed * (1.62 - x_volts) / 1.6 * elapsed_time  # Slightly turn left
        elif x_volts > 1.62 and x_volts <= 3.0:
            angle += turn_speed * (x_volts - 1.62) / 1.58 * elapsed_time  # Slightly turn right
        elif x_volts >= 3.0:
            angle += turn_speed * elapsed_time  # Spin right
            speed = 0

        # Update cursor position based on speed and direction
        x += (speed * math.cos(angle * math.pi / 180))
        y += (speed * math.sin(angle * math.pi / 180))

        # Ensure the cursor stays within the screen bounds
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))

        # Draw a line from the previous position to the current position
        pygame.draw.line(screen, (0, 0, 0), (prev_x, prev_y), (x, y))

        # Update the display
        pygame.display.flip()

        # Update the previous position
        prev_x, prev_y = x, y

    # Print current speed and angle
    print("Current speed:", speed)
    print("Current angle:", angle)

# Close the serial port
ser.close()

# Quit Pygame
pygame.quit()
sys.exit()
