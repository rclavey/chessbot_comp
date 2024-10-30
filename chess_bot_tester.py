import random
from chess_rules import Board, ROWS, COLS, Pawn, King, Knight, Rook, Bishop, Queen

USE_PYGAME_UI = False

class RandomAgent:
    def __init__(self, color):
        self.color = color

    def choose_move(self, board):
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece != 0 and piece.color == self.color:
                    valid_moves = piece.get_valid_moves(board)
                    if valid_moves:
                        pieces.append((piece, valid_moves))

        if not pieces:
            return None, None

        piece, moves = random.choice(pieces)
        move = random.choice(moves)
        return piece, move

def play_game(agent1, agent2):
    board = Board(use_pygame_ui=False)
    agents = {'white': agent1, 'black': agent2}
    move_log = []

    while True:
        current_agent = agents[board.turn]
        piece, move = current_agent.choose_move(board)

        # Re-check that the piece is still valid
        if piece is None or board.board[piece.row][piece.col] != piece:
            continue  # Skip to the next iteration if piece is no longer valid

        # Log the move in algebraic notation
        notation = get_algebraic_notation(board, piece, move)
        move_log.append(notation)

        # Execute the move, using promotion if the piece is a pawn reaching the last rank
        board.select_piece(piece.row, piece.col)
        if isinstance(piece, Pawn) and (move[0] == 0 or move[0] == ROWS - 1):
            board.promote_pawn(piece, move[0], move[1], promotion_choice='queen')  # Default promotion to Queen
        else:
            board.move_piece(move[0], move[1])

        # Check game end conditions immediately after the move
        if board.is_checkmate():
            result = 'black' if board.turn == 'white' else 'white'
            break
        elif board.is_stalemate() or board.is_threefold_repetition() or board.is_fifty_move_rule():
            result = 'draw'
            break

    # Format move_log as a single space-separated string for game_analyzer
    return result, len(move_log), " ".join(move_log)

def get_algebraic_notation(board, piece, move):
    """Convert a move to algebraic notation format."""
    if isinstance(piece, Pawn):
        piece_symbol = ''
    elif isinstance(piece, Knight):
        piece_symbol = 'N'
    elif isinstance(piece, Bishop):
        piece_symbol = 'B'
    elif isinstance(piece, Rook):
        piece_symbol = 'R'
    elif isinstance(piece, Queen):
        piece_symbol = 'Q'
    elif isinstance(piece, King):
        piece_symbol = 'K'
    else:
        piece_symbol = ''

    capture = 'x' if board.board[move[0]][move[1]] != 0 else ''
    origin_col = chr(piece.col + ord('a'))
    origin_row = str(ROWS - piece.row)
    dest_col = chr(move[1] + ord('a'))
    dest_row = str(ROWS - move[0])
    
    if isinstance(piece, King) and abs(move[1] - piece.col) == 2:
        return 'O-O' if move[1] > piece.col else 'O-O-O'

    promotion = ''
    if isinstance(piece, Pawn) and (move[0] == 0 or move[0] == ROWS - 1):
        promotion = '=Q'

    if piece_symbol == '':
        if capture:
            notation = f"{origin_col}{capture}{dest_col}{dest_row}{promotion}"
        else:
            notation = f"{dest_col}{dest_row}{promotion}"
    else:
        notation = f"{piece_symbol}{origin_col}{origin_row}{capture}{dest_col}{dest_row}{promotion}"
    
    return notation

Board.get_algebraic_notation = get_algebraic_notation

def main():
    num_games = 10
    agent1 = RandomAgent('white')
    agent2 = RandomAgent('black')

    results = {'white': 0, 'black': 0, 'draw': 0}
    game_details = []

    for i in range(num_games):
        result, move_count, move_log = play_game(agent1, agent2)
        results[result] += 1
        game_details.append({
            'game': i + 1,
            'winner': result,
            'move_count': move_count,
            'notation': move_log
        })

    # Print game details in algebraic notation
    for game in game_details:
        print(f"\nGame {game['game']} - Winner: {game['winner']}")
        print(f"Total Moves: {game['move_count']}")
        print("Game Notation (Algebraic):")
        print(game['notation'])

    # Summary of results
    print("\nSummary of results:")
    print(f"White wins: {results['white']}")
    print(f"Black wins: {results['black']}")
    print(f"Draws: {results['draw']}")

if __name__ == "__main__":
    main()