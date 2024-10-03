import chess
from time import perf_counter
from math import trunc

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

    def awake(self):
        # IDDFS function
        self.nodes = 0
        start_time = perf_counter()
        this_depth = 0
        force_depth = 1  # depth-limiting option for example
        # TODO: change into while-true + stop + time management
        while this_depth < force_depth:
            this_depth += 1
            (pv, score) = self.struggle(this_depth)
            end_time = perf_counter()
            millis_time = trunc((end_time - start_time) * 1000)
            nps = trunc(self.nodes / (end_time - start_time))
            pv_uci = list(map(lambda move: move.uci(), pv))
            print(
                f"info depth {this_depth} score cp {score} time {millis_time} nodes {self.nodes} nps {nps} pv {' '.join(pv_uci)}"
            )
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
