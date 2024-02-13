try:
    import chess
    import chess.engine
    import random
    
    class ChessBot:
        def __init__(self):
            self.board = chess.Board()
            self.engine = chess.engine.SimpleEngine.popen_uci("C:/Users/unite/Downloads/stockfish-windows-x86-64-modern/stockfish")
    
        def play(self):
            legal_moves = list(self.board.legal_moves)
            move_values = {}
            
            for move in legal_moves:
                self.board.push(move)
                evaluation = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))['score'].relative.score()
                self.board.pop()
                move_values[move] = evaluation
    
            # Bias towards better moves
            move_values = {k: v + max(move_values.values()) for k, v in move_values.items()}
    
            best_move = max(move_values, key=move_values.get)
    
            # Update move values based on previous evaluations
            if hasattr(self, 'previous_evaluation'):
                if move_values[best_move] < self.previous_evaluation:
                    move_values[best_move] *= -1
    
            self.previous_evaluation = move_values[best_move]
    
            return best_move
    
        def play_game(self):
            while not self.board.is_game_over():
                move = self.play()
                self.board.push(move)
                print("Move:", move, "Evaluation:", self.previous_evaluation)
                print(self.board)
    
    if __name__ == "__main__":
        try:
            bot = ChessBot()
            bot.play_game()
        except Exception as e:
            print(e)
            input("")
except Exception as e:
    print (e)
    input("")
