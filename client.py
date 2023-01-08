import pygame
import socket
import sys
import math

pygame.init()
SCREEN = pygame.display.set_mode((100, 100), pygame.RESIZABLE)
SCREEN.fill("#1B1D1E")

server_port = 9999

try:
    host_ip = socket.gethostbyname("autole")
    print("Found server on", host_ip)
except Exception:
    host_ip = input("Unable to locate server!\nPlease input ip manually:\n")

# Initialize a TCP client socket using SOCK_STREAM
direction = None
while True:
    data = None
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 1
            if event.key == pygame.K_DOWN:
                direction = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                direction = None

    SCREEN.fill("#1B1D1E")
    sizeX, sizeY = SCREEN.get_size()

    #p = pygame.Surface([100, 100])
    #p.set_colorkey("#1B1D1E")
    #p.fill("#F8F8F2")


    dx = pygame.mouse.get_pos()[0] - sizeX // 2
    dy = pygame.mouse.get_pos()[1] - sizeY // 2
    if dy != 0: 
        rads = math.atan(dx/dy) 
    else: 
        rads = 0
    a = math.degrees(rads)

    if dy > 0:
        a += 180
    if dy == 0 and dx > 0:
        a = -35
    if dy == 0 and dx < 0:
        a = 35



    if a > 35 and a < 135:
        a = 35
    if a >= 135:
        a = 180 - a
    if a < 0 and a < -35:
        a = -35

    if direction != None:
        p = pygame.image.load("Arrow_g.png")
    else:
        p = pygame.image.load("Arrow.png")

    p = pygame.transform.rotate(p, a)
    rect = p.get_rect(center = (sizeX // 2, sizeY // 2))
    SCREEN.blit(p, rect)


    pygame.display.update()

    try:
        if direction == None:
            data = "s"
        if direction == 1:
            data = "f"
        if direction == 2:
            data = "b"

        data += " " + str(int(a))
        tcp_client.connect((host_ip, server_port))
        # Establish connection to TCP server and exchange data
        tcp_client.sendall(data.encode())

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()

    print ("Bytes Received: {}".format(received.decode()))

