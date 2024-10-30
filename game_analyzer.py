import pygame
from chess_rules import Board, ROWS, COLS, Pawn, King, Bishop, Rook, Knight, Queen 

 
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game Analyzer")

# Chessboard dimensions and colors
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
WHITE = (245, 245, 220)
BROWN = (139, 69, 19)

# Sidebar and arrow dimensions
SIDEBAR_WIDTH = SCREEN_WIDTH - BOARD_SIZE
ARROW_SIZE = 40
BAR_WIDTH = 50
MAX_BAR_HEIGHT = BOARD_SIZE - ARROW_SIZE - 60

# Text box dimensions
TEXT_BOX_HEIGHT = SCREEN_HEIGHT - BOARD_SIZE
TEXT_BOX_WIDTH = SCREEN_WIDTH
SCROLL_STEP = 10  # Pixels to move on each scroll event
scroll_offset = 0 

# Load piece images
piece_images = {}
piece_names = [
    'white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
    'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king'
]
for name in piece_names:
    piece_images[name] = pygame.transform.scale(
        pygame.image.load(f'images/{name}.png'), (SQUARE_SIZE, SQUARE_SIZE)
    )

# Font for the text box
font = pygame.font.SysFont(None, 24)

# Moves and state initialization
game_to_analyze = "Ng1h3 f6 c4 a6 a3 c6 g3 e5 d3 Ra8a7 Bf1g2 c5 Bg2d5 Ke8e7 d4 Qd8a5 Ke1f1 h5 Rh1g1 cxd4 a4 Nb8c6 Rg1h1 Ra7a8 Nb1c3 Ke7d6 Ra1b1 dxc3 Rb1a1 Rh8h7 f4 Rh7h6 c5 Qa5xc5 b3 Rh6g6 Nh3g1 Rg6g5 h4 c2 Kf1g2 b6 Bc1b2 Bf8e7 fxe5 Rg5xe5 Ra1b1 b5 Qd1xc2 g6 Bd5e4 Ra8a7 b4 Ng8h6 Ng1f3 Bc8b7 Be4f5 Ra7a8 Bb2c3 Nh6g4 axb5 gxf5 Rh1h2 f4 bxc5 Re5xc5 e4 Nc6a5 Nf3d4 Bb7xe4 Kg2g1 Na5b3 Qc2d1 Rc5d5 gxf4 Be7f8 b6 Nb3c5 Kg1f1 f5 Bc3e1 Nc5a4 Rb1c1 Na4c5 Qd1b3 a5 Qb3b2 Kd6e7 Nd4b3 Be4c2 Be1xa5 Ke7e6 Qb2g7 Rd5d6 Ba5e1 Ke6d5 Nb3d2 Bc2e4 Be1f2 Nc5a6 Nd2c4 Kd5c6 Kf1e2 Na6b8 Rc1c2 Be4g2 Ke2e1 Ng4e5 Rh2h3 Bf8xg7 Ke1e2 Kc6b7 Rc2c1 Bg2xh3 fxe5 Ra8a6 exd6 Bh3g2 Bf2e3 f4 Ke2d3 f3 Kd3c2 f2 Nc4d2 Kb7c8 b7 Bg2xb7 Nd2b3 Kc8d8 Kc2d2 Bb7h1 Rc1c2 Bg7a1 Rc2c7 Ra6a5 Nb3c5 Ra5xc5 Kd2e2 Bh1f3 Ke2xf2 Nb8c6 Rc7c8 Kd8xc8 Kf2g1 Ba1h8 Be3f4 Kc8b7 Bf4g5 Nc6d8 Bg5f6 Bf3c6 Kg1h2 Rc5e5 Bf6xh8 Re5b5 Kh2g3 Kb7c8 Kg3f2 Nd8b7 Bh8a1 Kc8d8 Ba1f6 Kd8e8 Kf2e1 Ke8f7 Bf6d8 Rb5g5 Ke1e2 Kf7g6 Bd8a5 Nb7d8 hxg5 Kg6h7 g6 Kh7g8 Ke2e1 h4 g7 h3 Ke1e2 Kg8h7 g8=Q Kh7h6 Qg8xd8 Bc6a8 Ke2e3 h2 Ba5b4 Kh6g7 Ke3d2 Kg7h7 Kd2d1 Kh7h6 Kd1d2 h1=Q Bb4a5 Qh1g2 Kd2d1 Ba8d5 Kd1e1 Kh6g6 Qd8g8 Bd5xg8 Ba5b6 Qg2h1 Ke1e2 Kg6f7 Ke2e3 Kf7g7 Bb6a5 Kg7h8 Ba5d8 Bg8h7 Ke3d2 Bh7c2 Kd2c3 Qh1c6 Kc3b4 Kh8g7 Bd8c7 Qc6a4 Kb4c5 Qa4e4 Kc5b6 Kg7h8 Kb6b5 Bc2d1 Kb5a5 Bd1g4 Bc7b8 Kh8g8 Bb8a7 Qe4g6 Ba7f2 Kg8h7 Ka5b4 Kh7h6 Bf2c5 Bg4h3 Kb4b5 Qg6b1 Bc5b4 Kh6g5 Kb5a5 Qb1d1 Bb4e1 Bh3g4 Be1g3 Qd1b3 Bg3e5 Bg4h5 Be5a1 Kg5g6"
moves = game_to_analyze.split()
current_move_index = 0

# Arrow positions
arrow_y_position = BOARD_SIZE - ARROW_SIZE - 20
left_arrow_x = BOARD_SIZE + (SIDEBAR_WIDTH // 2) - ARROW_SIZE - 5
right_arrow_x = BOARD_SIZE + (SIDEBAR_WIDTH // 2) + 5



def draw_chessboard():
    """Draws a 640x640 chessboard in the top-left corner of the window."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    """Draws pieces on the chessboard based on the board state."""
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece != 0:
                piece_image = piece_images[piece.name]
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_eval_bar(eval_score):
    """Draws an evaluation bar on the right side of the board."""
    bar_x_position = BOARD_SIZE + (SIDEBAR_WIDTH - BAR_WIDTH) // 2
    bar_y_position = 20

    pygame.draw.rect(screen, (0, 0, 0), (bar_x_position, bar_y_position, BAR_WIDTH, MAX_BAR_HEIGHT), 1)

    white_height = MAX_BAR_HEIGHT // 2 + int((eval_score / 20) * (MAX_BAR_HEIGHT // 2))
    pygame.draw.rect(screen, (0, 0, 0), (bar_x_position + 1, bar_y_position + 1, BAR_WIDTH - 2, MAX_BAR_HEIGHT - white_height - 1))
    white_y_position = bar_y_position + (MAX_BAR_HEIGHT - white_height)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x_position + 1, white_y_position, BAR_WIDTH - 2, white_height - 1))

def draw_arrows():
    """Draws navigation arrows side by side at the bottom of the evaluation bar."""
    # Left arrow (backward)
    pygame.draw.polygon(screen, (0, 0, 0), [
        (left_arrow_x + ARROW_SIZE, arrow_y_position),
        (left_arrow_x, arrow_y_position + ARROW_SIZE // 2),
        (left_arrow_x + ARROW_SIZE, arrow_y_position + ARROW_SIZE)
    ])
    
    # Right arrow (forward)
    pygame.draw.polygon(screen, (0, 0, 0), [
        (right_arrow_x, arrow_y_position),
        (right_arrow_x + ARROW_SIZE, arrow_y_position + ARROW_SIZE // 2),
        (right_arrow_x, arrow_y_position + ARROW_SIZE)
    ])

def draw_text_box():
    global scroll_offset
    text_box_y_position = BOARD_SIZE
    text_box_rect = pygame.Rect(0, text_box_y_position, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT)
    pygame.draw.rect(screen, (220, 220, 220), text_box_rect)
    
    # Prepare lines for text wrapping
    lines = []
    current_line = ""
    for i, word in enumerate(moves):
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] < TEXT_BOX_WIDTH - 20:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Calculate max scroll based on content height
    max_scroll = max(0, len(lines) * 25 - TEXT_BOX_HEIGHT)
    scroll_offset = max(0, min(scroll_offset, max_scroll))

    # Track the index of moves displayed so we only highlight the correct occurrence
    move_count = 0
    y_offset = text_box_y_position + 10 - scroll_offset
    for i, line in enumerate(lines):
        words = line.split()
        x_offset = 10
        for word in words:
            if y_offset + i * 25 >= text_box_y_position:  # Only draw if within text box boundaries
                if word == moves[current_move_index] and move_count == current_move_index:
                    move_surface = font.render(word, True, (0, 0, 0))
                    move_rect = move_surface.get_rect(topleft=(x_offset, y_offset + i * 25))
                    pygame.draw.rect(screen, (255, 255, 0), move_rect)  # Highlight current move
                    screen.blit(move_surface, move_rect.topleft)
                else:
                    word_surface = font.render(word, True, (0, 0, 0))
                    screen.blit(word_surface, (x_offset, y_offset + i * 25))

            if word in moves:
                move_count += 1
            x_offset += font.size(word + " ")[0]

def apply_move(board, move):
    """Directly apply a move to the board using only chess_rules logic."""
    try:
        # Handle castling moves directly
        if move == "O-O":
            return board.castle_kingside()
        elif move == "O-O-O":
            return board.castle_queenside()

        # Identify if the move involves a promotion
        promotion = None
        if "=" in move:
            move, promotion = move.split("=")
            promotion = {
                'q': 'queen',
                'r': 'rook',
                'b': 'bishop',
                'n': 'knight'
            }.get(promotion.lower(), 'queen')  # Defaults to queen

        # Determine the destination
        dest_col = ord(move[-2]) - ord('a')
        dest_row = 8 - int(move[-1])

        # Determine the piece type and optional start coordinates
        piece_symbol = "" if move[0].islower() else move[0]
        start_col = start_row = None
        if len(move) > 2 and piece_symbol == "":
            if move[0].islower():
                start_col = ord(move[0]) - ord('a')
            elif move[0].isdigit():
                start_row = 8 - int(move[0])

        # Use chess_rules find_pieces to locate and select the piece
        possible_pieces = find_pieces(board, piece_symbol, board.turn, start_row, start_col, dest_row, dest_col)
        if not possible_pieces:
            print(f"Error parsing move: {move}")
            return False

        piece = possible_pieces[0]
        board.select_piece(piece.row, piece.col)  # Use chess_rules selection

        # Execute the move using chess_rules
        if promotion and isinstance(piece, Pawn) and (dest_row == 0 or dest_row == 7):
            board.promote_pawn(piece, dest_row, dest_col, promotion_choice=promotion)
        else:
            if not board.move_piece(dest_row, dest_col):
                print(f"Invalid move: {move}")
                return False

        return True

    except Exception as e:
        print(f"Error parsing move: {move}, {e}")
        return False

def find_pieces(board, piece_symbol, color, start_row, start_col, dest_row, dest_col):
    """Helper function to locate pieces on the board based on move criteria."""
    pieces = []
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece != 0 and piece.color == color:
                # Match piece type (Pawn, Rook, etc.) if specified
                if (piece_symbol == "" and isinstance(piece, Pawn)) or \
                   (piece_symbol == "N" and isinstance(piece, Knight)) or \
                   (piece_symbol == "B" and isinstance(piece, Bishop)) or \
                   (piece_symbol == "R" and isinstance(piece, Rook)) or \
                   (piece_symbol == "Q" and isinstance(piece, Queen)) or \
                   (piece_symbol == "K" and isinstance(piece, King)):
                    # Ensure piece can move to destination and match row/col restrictions
                    if (start_row is None or piece.row == start_row) and \
                       (start_col is None or piece.col == start_col) and \
                       (dest_row, dest_col) in piece.get_valid_moves(board):
                        pieces.append(piece)
    return pieces

# Initialize the chess board and set eval score
board = Board(use_pygame_ui=False)
eval_score = 0

PIECE_VALUES = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0  
}

def calculate_material_score(board):
    score = 0
    for row in board.board:
        for piece in row:
            if piece != 0:  # If there's a piece in the square
                value = PIECE_VALUES.get(piece.name.split("_")[1], 0)  # Get piece type and value
                score += value if piece.color == 'white' else -value
    return score

def reset_board_to_position(index):
    global eval_score
    board.__init__(use_pygame_ui=False)  # Reset the board to starting position
    for move in moves[:index + 1]:
        if not apply_move(board, move):
            print("Invalid move:", move)
            break
    # Calculate the evaluation score based on material balance
    eval_score = calculate_material_score(board)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if left_arrow_x <= x <= left_arrow_x + ARROW_SIZE and arrow_y_position <= y <= arrow_y_position + ARROW_SIZE:
                if current_move_index > 0:
                    current_move_index -= 1
                    reset_board_to_position(current_move_index)
            elif right_arrow_x <= x <= right_arrow_x + ARROW_SIZE and arrow_y_position <= y <= arrow_y_position + ARROW_SIZE:
                if current_move_index < len(moves) - 1:
                    current_move_index += 1
                    reset_board_to_position(current_move_index)
        
        # Handle scroll wheel events for scrolling the text box
        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset -= event.y * SCROLL_STEP  # Update scroll position based on wheel direction

    screen.fill((255, 255, 255))
    draw_chessboard()
    draw_pieces(board)
    draw_eval_bar(eval_score)
    draw_arrows()
    draw_text_box()
    pygame.display.flip()

pygame.quit()