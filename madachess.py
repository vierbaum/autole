import pygame
import sys
import chess
import chess.engine
import socket

# Define some constants for the color values
bgColor = "#1B1D1E"
fgColor = "#F8F8F2"
CR = "#CC241D"


# Define some constants for the chess piece names and their corresponding images
PIECES = {
    "P": "P.png",
    "N": "N.png",
    "B": "B.png",
    "R": "R.png",
    "Q": "Q.png",
    "K": "K.png",
    "p": "p.png",
    "n": "n.png",
    "b": "b.png",
    "r": "r.png",
    "q": "q.png",
    "k": "k.png"
}

# Create a dictionary to store the images of the pieces
piecesImg = {piece: pygame.image.load("pieces/" + filename) for piece, filename in PIECES.items()}

# Initialize the Pygame font module
pygame.font.init()

# Create a font object
FONT = pygame.font.SysFont("jetbrainsmonomediumnerdfontmono", 20)

def drawBoard(screen, board, squareSize, clicked):
    """Draws the chess board and pieces on the screen.

    Args:
        screen: the Pygame surface to draw the board on
        board: the chess.Board object representing the current game state
        squareSize: the size of each square on the board
    """
    for x in range(8):
        for y in range(8):
            # Create a rectangle for the current square
            rect = pygame.Rect(x * squareSize, (7 - y) * squareSize, squareSize, squareSize)
            # Fill the rectangle with the appropriate color
            color = fgColor if (x + y) % 2 == 0 else bgColor
            pygame.draw.rect(screen, color, rect)
            # Get the chess piece at the current square, if any
            piece = board.piece_at(8 * y + x)
            if piece and clicked != x + y * 8:
                # Get the corresponding image for the piece
                img = piecesImg[piece.symbol()]
                # Scale the image to the appropriate size
                img = pygame.transform.scale(img, (squareSize, squareSize))
                # Draw the image on the square
                screen.blit(img, (x * squareSize, (7 - y) * squareSize))

def drawHoveringPiece(screen, squareSize, pos, hoveringPiece):
    img = piecesImg[hoveringPiece.symbol()]
    img = pygame.transform.scale(img, (squareSize, squareSize))
    # Draw the image on the square
    rect = pygame.Rect(0, 0, squareSize, squareSize)
    rect.center = pos
    screen.blit(img, rect)



def main(screen, host_ip, server_port):
    board = chess.Board()
    #sf = chess.engine.SimpleEngine.popen_uci(r"/usr/bin/Stockfish20220622")
    clicked = None
    hoveringPiece = None
    while True:
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sizeX, sizeY = screen.get_size()
        squareSize = sizeX // 8 if sizeX < sizeY else sizeY // 8
        boardRect = pygame.Rect(0, 0, squareSize * 8, squareSize * 8)
        if not board.turn:

            try:
                data = "C"
                data += board.move_stack[-1].uci()
                print(data)
                tcp_client.connect((host_ip, server_port))
                tcp_client.sendall(data.encode())

                # Read data from the TCP server and close the connection
                received = tcp_client.recv(1024)
            finally:
                pass
                tcp_client.close()

            board.push(chess.Move.from_uci(received.decode()))
            if board.is_checkmate():
                print("MATED!")
                drawBoard(screen, board, squareSize, clicked)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                    text_surface = FONT.render("MADA LOST", True, CR)  
                    screen.blit(text_surface, (sizeX / 3, sizeY / 2))
                    pygame.display.update()
                
        
        screen.fill(bgColor)
        drawBoard(screen, board, squareSize, clicked)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                x, y = pygame.mouse.get_pos()
                if boardRect.collidepoint((x, y)):
                    clicked = x // squareSize + (7 - y // squareSize) * 8
                    hoveringPiece = board.piece_at(clicked)
            if event.type == pygame.MOUSEBUTTONUP and clicked:
                x, y = pygame.mouse.get_pos()
                newSquare = x // squareSize + (7 - y // squareSize) * 8
                move = chess.Move(clicked, newSquare)
                print(move)
                if move in board.legal_moves:
                    #board.set_piece_at(newSquare, board.piece_at(clicked))
                    #board.remove_piece_at(clicked)
                    if board.turn:
                        board.push(move)
                        drawBoard(screen, board, squareSize, clicked)
                    else:
                        print("NOT YOUR TURN, MADA")
                else:
                    print("NOT A VALID MOVE, MADA")
                hoveringPiece = None
                clicked = None
        if clicked and hoveringPiece:
            drawHoveringPiece(screen, squareSize, pygame.mouse.get_pos(), hoveringPiece)
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((100, 100), pygame.RESIZABLE)
    screen.fill(bgColor)
    main(screen)
    pygame.quit()
    sys.exit()