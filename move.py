class Move:
  def __init__(self, start, end):
    self.start = start 
    self.end = end     

  def __repr__(self):
    return f"Move({self.start} -> {self.end})"

def generate_moves(board):
  # Generate all pseudo-legal moves (for simplicity, no actual chess logic here)
  moves = []
  for pos in range(64):
    piece = board.get_piece(pos)
    if piece == 1:
      if pos >= 8 and board.get_piece(pos - 8) == 0:
        moves.append(Move(pos, pos - 8))
    elif piece == -1:
      if pos < 56 and board.get_piece(pos + 8) == 0:
        moves.append(Move(pos, pos + 8))
  return moves
