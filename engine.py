import chess
from time import perf_counter
from math import trunc
import sys
import clock

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

    def is_stm_white(self):
        return self.board.turn == chess.WHITE

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
        lim = self.limiter
        match lim.mode:
            case clock.TimingMode.DEPTH:
                return self.depth > lim.depth
            case clock.TimingMode.NODES:
                return self.nodes > lim.nodes
            case mode if mode in [clock.TimingMode.MOVETIME, clock.TimingMode.TC]:
                # branching factor: dictates whether next ply's search can fully pass
                # if BF = 3, 3 / 1/(1-1/3) = x2 of used time is needed again
                bf = 20
                cur_millis = perf_counter() * 1000
                return (cur_millis - self.start_millis) * (bf - 1) > lim.movetime
            case _:
                return False

    def awake(self, limiter: clock.SearchLimiter):
        # IDDFS function
        self.nodes = 0
        self.start_millis = perf_counter() * 1000
        self.limiter = limiter
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
