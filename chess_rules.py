import pygame
import random

# Constants for board size
ROWS, COLS = 8, 8
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // COLS
WHITE = (245, 245, 220)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)

# Piece Classes
class Piece:
    def __init__(self, row, col, color, name):
        self.row = row
        self.col = col
        self.color = color  
        self.name = name    
        self.has_moved = False
        self.captured = False

    def move(self, row, col):
        self.row = row
        self.col = col
        self.has_moved = True

    def get_valid_moves(self, board, avoid_check=True):
        return []

class Pawn(Piece):
    def get_valid_moves(self, board, en_passant_target=None, avoid_check=True):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Move forward
        if 0 <= self.row + direction < ROWS:
            if board.board[self.row + direction][self.col] == 0:
                moves.append((self.row + direction, self.col))
                # Double move from starting position
                if self.row == start_row and board.board[self.row + 2*direction][self.col] == 0:
                    moves.append((self.row + 2*direction, self.col))

        # Captures
        for dx in [-1, 1]:
            new_col = self.col + dx
            if 0 <= new_col < COLS and 0 <= self.row + direction < ROWS:
                target = board.board[self.row + direction][new_col]
                if target != 0 and target.color != self.color:
                    moves.append((self.row + direction, new_col))

        # En Passant
        if en_passant_target:
            if abs(en_passant_target[1] - self.col) == 1 and self.row + direction == en_passant_target[0]:
                moves.append(en_passant_target)

        if avoid_check:
            moves = [move for move in moves if not board.is_in_check_after_move(self, move)]
        return moves

class Rook(Piece):
    def get_valid_moves(self, board, avoid_check=True):
        moves = []
        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            for i in range(1, ROWS):
                r = self.row + d[0]*i
                c = self.col + d[1]*i
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board.board[r][c] == 0:
                        moves.append((r, c))
                    elif board.board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        if avoid_check:
            moves = [move for move in moves if not board.is_in_check_after_move(self, move)]
        return moves

class Knight(Piece):
    def get_valid_moves(self, board, avoid_check=True):
        moves = []
        # All possible L-shaped moves
        steps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]
        for s in steps:
            r = self.row + s[0]
            c = self.col + s[1]
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board.board[r][c] == 0 or board.board[r][c].color != self.color:
                    moves.append((r, c))
        if avoid_check:
            moves = [move for move in moves if not board.is_in_check_after_move(self, move)]
        return moves

class Bishop(Piece):
    def get_valid_moves(self, board, avoid_check=True):
        moves = []
        # Diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, ROWS):
                r = self.row + d[0]*i
                c = self.col + d[1]*i
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board.board[r][c] == 0:
                        moves.append((r, c))
                    elif board.board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        if avoid_check:
            moves = [move for move in moves if not board.is_in_check_after_move(self, move)]
        return moves

class Queen(Piece):
    def get_valid_moves(self, board, avoid_check=True):
        moves = []
        # Combine rook and bishop moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, ROWS):
                r = self.row + d[0]*i
                c = self.col + d[1]*i
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board.board[r][c] == 0:
                        moves.append((r, c))
                    elif board.board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        if avoid_check:
            moves = [move for move in moves if not board.is_in_check_after_move(self, move)]
        return moves

class King(Piece):
    def get_valid_moves(self, board, castle_rights=None, avoid_check=True):
        moves = []
        # One square in any direction
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            r = self.row + d[0]
            c = self.col + d[1]
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board.board[r][c] == 0 or board.board[r][c].color != self.color:
                    moves.append((r, c))

        # Castling
        if not self.has_moved and castle_rights:
            # Kingside castling
            if castle_rights[self.color]['kingside']:
                if board.board[self.row][self.col + 1] == 0 and board.board[self.row][self.col + 2] == 0:
                    moves.append((self.row, self.col + 2))
            # Queenside castling
            if castle_rights[self.color]['queenside']:
                if board.board[self.row][self.col - 1] == 0 and board.board[self.row][self.col - 2] == 0 and board.board[self.row][self.col - 3] == 0:
                    moves.append((self.row, self.col - 2))

        if avoid_check:
            moves = [move for move in moves if not board.is_in_check_after_move(self, move)]
        return moves



class Board:
    def __init__(self, use_pygame_ui=False):
        self.use_pygame_ui = use_pygame_ui
        self.board = self.create_board()
        self.selected_piece = None
        self.valid_moves = []
        self.turn = 'white'
        self.en_passant_target = None
        self.castle_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.in_check = {'white': False, 'black': False}
        self.promotion_in_progress = False
        self.board_state_counts = {}
        self.halfmove_clock = 0

        if self.use_pygame_ui:
            pygame.init()
            self.win = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Chess')
            self.images = self.load_images()

    def load_images(self):
        """Load images for chess pieces if using Pygame."""
        pieces = [
            'white_pawn', 'white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king',
            'black_pawn', 'black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king'
        ]
        images = {}
        for piece in pieces:
            images[piece] = pygame.transform.scale(
                pygame.image.load(f'images/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)
            )
        return images

    def get_fen(self):
        """Generates the FEN representation of the board."""
        fen = ""
        for row in self.board:
            empty_count = 0
            for piece in row:
                if piece == 0:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    symbol = piece.name[0].upper() if piece.color == "white" else piece.name[0].lower()
                    fen += symbol
            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"
        fen = fen[:-1]  # Remove last slash
        fen += f" {'w' if self.turn == 'white' else 'b'} - - 0 1"  # Add turn, castling, and other FEN details
        return fen
        
    def draw(self, win):
        """Draw all pieces and highlight valid moves if using Pygame."""
        if self.use_pygame_ui:
            # Draw each piece at the correct location and scale it based on SQUARE_SIZE
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece != 0:
                        # Resize the piece image to fit SQUARE_SIZE
                        piece_image = pygame.transform.scale(self.images[piece.name], (SQUARE_SIZE, SQUARE_SIZE))
                        win.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            # Highlight selected piece and valid moves
            if self.selected_piece:
                # Draw a rectangle around the selected piece
                pygame.draw.rect(win, BLUE, 
                                (self.selected_piece.col * SQUARE_SIZE, 
                                self.selected_piece.row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE), 3)

                # Draw circles on valid move squares
                for move in self.valid_moves:
                    row, col = move
                    pygame.draw.circle(win, BLUE, 
                                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                        row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

    def is_king_in_check(self, color):
        king = None
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king = piece
                    break
            if king:
                break

        if not king:
            return False

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color != color:
                    if (king.row, king.col) in piece.get_valid_moves(self, avoid_check=False):
                        return True
        return False

    def is_in_check_after_move(self, piece, move):
        original_row, original_col = piece.row, piece.col
        target_piece = self.board[move[0]][move[1]]

        # Simulate the move
        self.board[original_row][original_col] = 0
        self.board[move[0]][move[1]] = piece
        piece.row, piece.col = move[0], move[1]

        in_check = self.is_king_in_check(piece.color)

        # Undo the move
        self.board[original_row][original_col] = piece
        self.board[move[0]][move[1]] = target_piece
        piece.row, piece.col = original_row, original_col

        return in_check

    def create_board(self):
        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        
        # Place pawns
        for col in range(COLS):
            board[1][col] = Pawn(1, col, 'black', 'black_pawn')
            board[6][col] = Pawn(6, col, 'white', 'white_pawn')
            
        # Place other pieces
        # Black pieces
        board[0][0] = Rook(0, 0, 'black', 'black_rook')
        board[0][1] = Knight(0, 1, 'black', 'black_knight')
        board[0][2] = Bishop(0, 2, 'black', 'black_bishop')
        board[0][3] = Queen(0, 3, 'black', 'black_queen')
        board[0][4] = King(0, 4, 'black', 'black_king')
        board[0][5] = Bishop(0, 5, 'black', 'black_bishop')
        board[0][6] = Knight(0, 6, 'black', 'black_knight')
        board[0][7] = Rook(0, 7, 'black', 'black_rook')

        # White pieces
        board[7][0] = Rook(7, 0, 'white', 'white_rook')
        board[7][1] = Knight(7, 1, 'white', 'white_knight')
        board[7][2] = Bishop(7, 2, 'white', 'white_bishop')
        board[7][3] = Queen(7, 3, 'white', 'white_queen')
        board[7][4] = King(7, 4, 'white', 'white_king')
        board[7][5] = Bishop(7, 5, 'white', 'white_bishop')
        board[7][6] = Knight(7, 6, 'white', 'white_knight')
        board[7][7] = Rook(7, 7, 'white', 'white_rook')
        
        return board

    def promote_pawn(self, pawn, row, col, promotion_choice=None):
        # If using Pygame and no choice is given, prompt the user for a choice
        if self.use_pygame_ui and promotion_choice is None:
            self.promotion_in_progress = True
            promotion_choice = self.choose_promotion_piece(pawn.color)

        # Default promotion for AI or when no UI is active
        if promotion_choice is None:
            promotion_choice = random.choice(['queen', 'rook', 'bishop', 'knight'])

        # Promote the pawn to the chosen piece
        if promotion_choice == 'queen':
            self.board[row][col] = Queen(row, col, pawn.color, f"{pawn.color}_queen")
        elif promotion_choice == 'rook':
            self.board[row][col] = Rook(row, col, pawn.color, f"{pawn.color}_rook")
        elif promotion_choice == 'bishop':
            self.board[row][col] = Bishop(row, col, pawn.color, f"{pawn.color}_bishop")
        elif promotion_choice == 'knight':
            self.board[row][col] = Knight(row, col, pawn.color, f"{pawn.color}_knight")

        # Remove the original pawn after promotion
        self.board[pawn.row][pawn.col] = 0
        self.promotion_in_progress = False
        self.change_turn()  # Change turn after promotion

    def choose_promotion_piece(self, color):
        piece_options = ['queen', 'rook', 'bishop', 'knight']
        piece_images = {
            'queen': self.images[f"{color}_queen"],
            'rook': self.images[f"{color}_rook"],
            'bishop': self.images[f"{color}_bishop"],
            'knight': self.images[f"{color}_knight"]
        }
        
        # Display options for promotion
        self.win.fill(WHITE)
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render("Choose a piece for promotion:", True, (0, 0, 0))
        self.win.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 4))

        # Calculate even spacing and place each piece centered
        option_width = SQUARE_SIZE
        total_width = len(piece_options) * option_width + (len(piece_options) - 1) * 10
        start_x = (WIDTH - total_width) // 2

        for i, piece in enumerate(piece_options):
            x = start_x + i * (option_width + 10)
            y = HEIGHT // 2
            self.win.blit(piece_images[piece], (x, y))
            pygame.draw.rect(self.win, (0, 0, 0), (x, y, option_width, option_width), 2)

        pygame.display.flip()

        # Wait for user to select a piece
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i, piece in enumerate(piece_options):
                        px = start_x + i * (option_width + 10)
                        if px <= x <= px + option_width and y >= HEIGHT // 2:
                            return piece

    def select_piece(self, row, col):
        if self.promotion_in_progress:
            return  # Prevent selecting pieces while promotion is in progress
        
        if self.selected_piece:
            result = self.move_piece(row, col)
            if not result:
                self.selected_piece = None
                self.select_piece(row, col)
        else:
            piece = self.board[row][col]
            if piece != 0 and piece.color == self.turn:
                self.selected_piece = piece
                # Get valid moves
                if isinstance(piece, King):
                    self.valid_moves = piece.get_valid_moves(self, castle_rights=self.castle_rights, avoid_check=True)
                elif isinstance(piece, Pawn):
                    self.valid_moves = piece.get_valid_moves(self, en_passant_target=self.en_passant_target, avoid_check=True)
                else:
                    self.valid_moves = piece.get_valid_moves(self, avoid_check=True)
                self.valid_moves = [move for move in self.valid_moves if not self.is_in_check_after_move(piece, move)]

    def move_piece(self, row, col):
        if (row, col) in self.valid_moves:
            captured_piece = None
            
            # Handle En Passant
            if isinstance(self.selected_piece, Pawn) and self.en_passant_target == (row, col):
                captured_piece = self.board[self.selected_piece.row][col]
                self.board[self.selected_piece.row][col] = 0

            # Track en passant target if a pawn moves two squares
            if isinstance(self.selected_piece, Pawn) and abs(row - self.selected_piece.row) == 2:
                self.en_passant_target = ((row + self.selected_piece.row) // 2, self.selected_piece.col)
            else:
                self.en_passant_target = None

            # Handle Castling
            if isinstance(self.selected_piece, King):
                if col - self.selected_piece.col == 2:  # Kingside castling
                    rook = self.board[row][col + 1]
                    self.board[row][col - 1] = rook
                    self.board[row][col + 1] = 0
                    rook.move(row, col - 1)
                elif col - self.selected_piece.col == -2:  # Queenside castling
                    rook = self.board[row][col - 2]
                    self.board[row][col + 1] = rook
                    self.board[row][col - 2] = 0
                    rook.move(row, col + 1)

            # Determine if a piece was captured (excluding en passant)
            target_piece = self.board[row][col]
            if target_piece != 0 and target_piece.color != self.selected_piece.color:
                captured_piece = target_piece

            # Handle Pawn Promotion
            if isinstance(self.selected_piece, Pawn) and (row == 0 or row == ROWS - 1):
                self.promote_pawn(self.selected_piece, row, col)
                self.selected_piece = None
                self.valid_moves = []
            else:
                # Move the piece
                self.board[self.selected_piece.row][self.selected_piece.col] = 0
                self.selected_piece.move(row, col)
                self.board[row][col] = self.selected_piece
                self.change_turn(captured_piece=captured_piece)
                self.selected_piece = None
                self.valid_moves = []

            # Check for game over conditions
            if self.is_checkmate():
                print(f"{self.turn.capitalize()} is checkmated! {'Black' if self.turn == 'white' else 'White'} wins!")
            elif self.is_stalemate():
                print("Stalemate! It's a draw!")
            elif self.is_threefold_repetition():
                print("Threefold Repetition! It's a draw!")
            elif self.is_fifty_move_rule():
                print("50-Move Rule! It's a draw!")
            return True
        return False

    def change_turn(self, captured_piece=None):
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.in_check[self.turn] = self.is_king_in_check(self.turn)

        # Update for threefold repetition
        board_state = self.get_board_state()
        self.board_state_counts[board_state] = self.board_state_counts.get(board_state, 0) + 1

        # Update halfmove clock for 50-move rule
        if isinstance(self.selected_piece, Pawn) or captured_piece is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

    def is_checkmate(self):
        if not self.in_check[self.turn]:
            return False
        # No legal moves for the king means checkmate
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color == self.turn:
                    if len(piece.get_valid_moves(self)) > 0:
                        return False
        return True

    def is_threefold_repetition(self):
        return self.board_state_counts.get(self.get_board_state(), 0) >= 3

    def is_fifty_move_rule(self):
        return self.halfmove_clock >= 50

    def is_stalemate(self):
        if self.in_check[self.turn]:
            return False
        # No legal moves means stalemate
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color == self.turn:
                    if len(piece.get_valid_moves(self)) > 0:
                        return False
        return True

    def get_board_state(self):
        state = ''
        for row in self.board:
            for piece in row:
                if piece == 0:
                    state += '0'
                else:
                    state += piece.color[0] + piece.__class__.__name__[0]
        return state
