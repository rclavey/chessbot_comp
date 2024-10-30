import pygame
import sys
from chess_rules import Board  # Import Board class from chess_rules

# Constants for display
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE = (245, 245, 220)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)

def draw_squares(win):
    """Draw the chessboard squares."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    # Initialize the board
    board = Board(use_pygame_ui=True)

    run = True
    while run:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                board.select_piece(row, col)

        # Check for game end conditions
        if board.is_checkmate():
            winner = "White" if board.turn == 'black' else "Black"
            board.display_game_over(win, f"{winner} is checkmated! {'Black' if board.turn == 'white' else 'White'} wins!")
        elif board.is_stalemate():
            board.display_game_over(win, "Stalemate! It's a draw!")

        # Draw board and pieces
        draw_squares(win)
        board.draw(win)  # Pass the window to the draw function
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()