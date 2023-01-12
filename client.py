import pygame
import socket
import sys
import math
import madachess

# Initialize the pygame library
pygame.init()

# Create a 100x100 window that is resizable
SCREEN = pygame.display.set_mode((100, 100), pygame.RESIZABLE)
# Fill the window with the color "#1B1D1E"
SCREEN.fill("#1B1D1E")

# Set the server port to 9999
server_port = 9999

try:
    # Attempt to get the host IP of the server named "autole"
    host_ip = socket.gethostbyname("autole")
    print("Found server on", host_ip)
except Exception:
    # If the server cannot be found, prompt the user to input the IP manually
    host_ip = input("Unable to locate server!\nPlease input ip manually:\n")

# Initialize a variable to store the direction of movement (None, "up", or "down")
direction = None

# Create a rectangle for the chess button
chessRect = pygame.Rect(0, 0, 20, 20)

while True:
    data = None
    # Initialize a TCP client socket
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Update the direction variable when the up or down arrow key is pressed
            if event.key == pygame.K_UP:
                direction = 1
            if event.key == pygame.K_DOWN:
                direction = 2
        if event.type == pygame.KEYUP:
            # Clear the direction variable when the up or down arrow key is released
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                direction = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)
            if chessRect.collidepoint((x, y)):
                madachess.main(SCREEN, host_ip, server_port)

    # Fill the screen with the color "#1B1D1E"
    SCREEN.fill("#1B1D1E")
    sizeX, sizeY = SCREEN.get_size()

    dx = pygame.mouse.get_pos()[0] - sizeX // 2
    dy = pygame.mouse.get_pos()[1] - sizeY // 2
    if dy != 0: 
        rads = math.atan(dx/dy) 
    else: 
        rads = 0
    a = math.degrees(rads)

    # Check the quadrant of the angle
    if dy > 0:
        a += 180
    if dy == 0 and dx > 0:
        a = -35
    if dy == 0 and dx < 0:
        a = 35

    # Check if the angle is within a certain range
    if a > 35 and a < 135:
    a = 35
    if a >= 135:
        a = 180 - a
    if a < 0 and a < -35:
        a = -35
   
    # Load different arrow images depending on the direction variable
    if direction != None:
        p = pygame.image.load("Arrow_g.png")
    else:
        p = pygame.image.load("Arrow.png")

    # Rotate the arrow image by the calculated angle
    p = pygame.transform.rotate(p, a)
    rect = p.get_rect(center = (sizeX // 2, sizeY // 2))
    # Draw the arrow image on the screen
    SCREEN.blit(p, rect)

    # Update the display
    pygame.display.update()

    try:
        # Set the data to be sent to the server
        if direction == None:
            data = "s"
        if direction == 1:
            data = "f"
        if direction == 2:
            data = "b"

        data += " " + str(int(a))
        # Connect to the server
        tcp_client.connect((host_ip, server_port))
        # Send the data to the server
        tcp_client.sendall(data.encode())

        # Receive data from the server and close the connection
        received = tcp_client.recv(1024)
    finally:
        # Close the TCP connection
        tcp_client.close()

    # Print the received data
    print ("Bytes Received: {}".format(received.decode()))
