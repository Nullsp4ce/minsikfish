# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from time import perf_counter_ns
from math import trunc
import sys
import chess
import clock

INFINITY = 32768
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
MATE_LIMIT = 1000
VALUE = {"P": 100, "N": 300, "B": 300, "R": 500, "Q": 900, "K": INFINITY}


class Globals:
    def __init__(self):
        self.board = chess.Board(START_FEN)
        self.nodes = 0
        self.start_nanos = 0
        self.depth = 0


g = Globals()


def mate_distancing(num):
    if num >= INFINITY - MATE_LIMIT:
        return num - 1
    if num <= -(INFINITY - MATE_LIMIT):
        return num + 1
    return num


def push(move: chess.Move):
    g.board.push(move)


def is_stm_white():
    return g.board.turn == chess.WHITE


def hit_blunt():
    # actually evaluation function
    score = 0
    for _, piece in g.board.piece_map().items():
        if piece is None:
            continue
        if piece.color is g.board.turn:
            score += VALUE[piece.symbol().upper()]
        else:
            score -= VALUE[piece.symbol().upper()]
    return score


def should_runsik():
    # called in IDDFS root
    if clock.state == clock.State.IDLE:
        return True
    match clock.lim.mode:
        case clock.TimingMode.DEPTH:
            return g.depth > clock.lim.depth
        case clock.TimingMode.NODES:
            return g.nodes > clock.lim.nodes
        case mode if mode in [clock.TimingMode.MOVETIME, clock.TimingMode.TC]:
            # branching factor: dictates whether next ply's search can fully pass
            # if BF = 3, 3 / 1/(1-1/3) = x2 of used time is needed again
            bf = 20
            cur_nanos = perf_counter_ns()
            return (cur_nanos - g.start_nanos) * (
                bf - 1
            ) > clock.lim.movetime * 1_000_000
        case _:
            return False


def should_runsik_nodes():
    # 'run every few thousand nodes or so': called at depth 3 left
    # (affected by general nodes per depth)
    if clock.state == clock.State.IDLE:
        return True
    match clock.lim.mode:
        case clock.TimingMode.DEPTH:
            return g.depth > clock.lim.depth
        case clock.TimingMode.NODES:
            return g.nodes > clock.lim.nodes
        case mode if mode in [clock.TimingMode.MOVETIME, clock.TimingMode.TC]:
            # quit only if movetime is passed (different from root fx)
            cur_nanos = perf_counter_ns()
            return (cur_nanos - g.start_nanos) > clock.lim.movetime * 1_000_000
        case _:
            return False


def awake():
    # IDDFS function
    g.nodes = 0
    g.start_nanos = perf_counter_ns()
    g.depth = 1
    while True:
        next_info = struggle(depth=g.depth)
        if next_info is None:
            break
        (pv, score) = next_info
        end_nanos = perf_counter_ns()
        nanos_time = end_nanos - g.start_nanos
        millis_time = trunc(nanos_time / 1_000_000)
        nps = trunc(g.nodes * 1_000_000_000 / (nanos_time))
        pv_uci = list(map(lambda move: move.uci(), pv))
        print(
            f"info depth {g.depth} score cp {score} "
            f"time {millis_time} nodes {g.nodes} nps {nps} "
            f"pv {' '.join(pv_uci)}"
        )
        sys.stdout.flush()
        g.depth += 1
        if should_runsik():
            break
    return pv_uci[0]


def struggle(
    alpha=-INFINITY, beta=INFINITY, depth=1
) -> tuple[list[chess.Move], int] | None:
    # actually search function

    if depth == 3 and should_runsik_nodes():
        return

    g.nodes += 1

    if g.board.is_checkmate():
        return ([], -INFINITY)
    if g.board.is_stalemate():
        return ([], 0)

    if depth == 0:
        return ([], hit_blunt())

    moves = g.board.generate_legal_moves()
    pv: list[chess.Move] = []
    best_score = -INFINITY

    for move in moves:
        g.board.push(move)
        next_info = struggle(-beta, -alpha, depth - 1)
        if next_info is None:
            return None
        (following, score) = next_info
        score *= -1
        score = mate_distancing(score)
        g.board.pop()

        # fail-soft alpha-beta
        if score > best_score:
            best_score = score
            if score > alpha:
                pv = [move, *following]
                alpha = score
        if score >= beta:
            return ([], best_score)  # can also exceed beta

    return (pv, best_score)
