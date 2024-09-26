import chess
from engine import Minsikfish

def main():
    ahnsik = Minsikfish()
    observer = chess.Board()

    for ply in range(5):
      best_move = ahnsik.struggle()

      if best_move is None:
          print('info string ahnsik')
          break
      
      print(f'info depth 1 pv {best_move.uci()}')
      observer.push(best_move)
      ahnsik.board.set_fen(observer.fen())

if __name__ == "__main__":
    main()
