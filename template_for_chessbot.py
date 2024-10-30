import random
from chess_rules import Board, Pawn, King, Knight, Rook, Bishop, Queen, ROWS, COLS
from chess_bot_tester import RandomAgent, play_game  

class TemplateAI:
    def __init__(self, color):
        self.color = color

    def choose_move(self, board):
        """
        Placeholder for AI logic to choose a move.
        
        Args:
            board (Board): The current board state.
        
        Returns:
            tuple: Selected piece and its target move (both None for now).
        """
        # Placeholder logic - random move generator to show how format necessary
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

def main():
    # Play a game where TemplateAI is White
    template_ai_white = TemplateAI('white')
    random_agent_black = RandomAgent('black')
    print("\nGame 1: TemplateAI (White) vs RandomAgent (Black)")
    result, move_count, move_log = play_game(template_ai_white, random_agent_black)
    print(f"Result: {result}")
    print(f"Move Count: {move_count}")
    print("Move Log:", move_log)

    # Play a game where TemplateAI is Black
    random_agent_white = RandomAgent('white')
    template_ai_black = TemplateAI('black')
    print("\nGame 2: RandomAgent (White) vs TemplateAI (Black)")
    result, move_count, move_log = play_game(random_agent_white, template_ai_black)
    print(f"Result: {result}")
    print(f"Move Count: {move_count}")
    print("Move Log:", move_log)

    """
    After getting the results from the terminal, you can use game_analyzer.py to 
    copy and paste the move log from the game into game_analyzer.py to watch the 
    game play out. 

    You can also use two_player_chess.py for pass'n'play style chess where you can 
    visualize things/strategy and run your own tests to ensure I coded the rules 
    correctly.

    The chess_rules.py file is where all rules pertaining to how the pieces move,
    win conditions, tie conditions, etc. can be found.

    The chess_bot_tester is where you can test ai's against one another, I imported 
    the feature and implemented it in the main function above for your convenience.

    That's about all you'll need to know (aside from how to code and how to play
    chess), so good luck to you all, I know you're going to need it!

    Have fun playing for second!!!

    P.S. you may need to change the path to the images to match your environment if 
    you want to use two_player_chess or game_analyzer.

    """

if __name__ == "__main__":
    main()
