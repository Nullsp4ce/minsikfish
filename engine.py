import chess
from time import perf_counter
from math import trunc
import sys

INFINITY = 32768
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

MATE_LIMIT = 1000


def mate_distancing(num):
    if num >= INFINITY - MATE_LIMIT:
        return num - 1
    if num <= -(INFINITY - MATE_LIMIT):
        return num + 1
    return num


class Minsikfish:

    value = {"P": 100, "N": 300, "B": 300, "R": 500, "Q": 900, "K": INFINITY}

    def __init__(self, fen=START_FEN):
        self.board = chess.Board(fen)

    def push(self, move: chess.Move):
        self.board.push(move)

    def hit_blunt(self):
        # actually evaluation function
        score = 0
        for _, piece in self.board.piece_map().items():
            if piece is None:
                continue
            elif piece.color is self.board.turn:
                score += self.value[piece.symbol().upper()]
            else:
                score -= self.value[piece.symbol().upper()]
        return score

    def should_runsik(self):
        force_depth = 3  # depth-limiting option for example
        # TODO: change into while-true + stop + time management
        return self.depth > force_depth

    def awake(self):
        # IDDFS function
        self.nodes = 0
        self.start_millis = perf_counter() * 1000
        self.depth = 1
        while True:
            (pv, score) = self.struggle(self.depth)
            end_millis = perf_counter() * 1000
            millis_time = trunc(end_millis - self.start_millis)
            nps = trunc(self.nodes * 1000 / (end_millis - self.start_millis))
            pv_uci = list(map(lambda move: move.uci(), pv))
            print(
                f"info depth {self.depth} score cp {score} time {millis_time} nodes {self.nodes} nps {nps} pv {' '.join(pv_uci)}"
            )
            sys.stdout.flush()
            self.depth += 1
            if self.should_runsik():
                break
        return pv_uci[0]

    def struggle(self, depth=1) -> tuple[list[chess.Move], int]:
        # actually search function
        # TODO: support partial search

        self.nodes += 1

        if self.board.is_checkmate():
            return ([], -INFINITY)
        if self.board.is_stalemate():
            return ([], 0)

        if depth == 0:
            return ([], self.hit_blunt())

        moves = self.board.generate_legal_moves()
        pv: list[chess.Move] = []
        best_score = -INFINITY

        for move in moves:
            self.board.push(move)
            (following, score) = self.struggle(depth - 1)
            score *= -1
            score = mate_distancing(score)
            self.board.pop()

            if score > best_score:
                pv = [move, *following]
                best_score = score

        return (pv, best_score)
