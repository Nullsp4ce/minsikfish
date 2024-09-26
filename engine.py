import chess

INFINITY = 32768
START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class Minsikfish:
    
    value = {
        'P': 100,
        'N': 300,
        'B': 300,
        'R': 500,
        'Q': 900,
        'K': INFINITY
    }

    def __init__(self, fen = START_FEN):
        self.board = chess.Board(fen)

    def push(self, move: chess.Move):
        self.board.push(move)

    def hit_blunt(self):
        # actually evaluation function
        score = 0
        for _, piece in self.board.piece_map().items():
            if piece is None:
                continue
            elif piece.color is chess.WHITE:
                score += self.value[piece.symbol()]
            else:
                score -= self.value[piece.symbol().upper()]
        return score

    def struggle(self):
        # actually search function
        moves = self.board.generate_pseudo_legal_moves()
        best_move = None
        best_score = -INFINITY

        for move in moves:
            self.board.push(move)
            
            score = self.hit_blunt()
            
            self.board.pop()
            
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
