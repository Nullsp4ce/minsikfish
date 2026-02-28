# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from enum import Enum
import threading
from time import perf_counter_ns
from math import trunc
import sys
import chess
import clock

INFINITY = 32768
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
MATE_LIMIT = 1000
VALUE = {"P": 100, "N": 300, "B": 300, "R": 500, "Q": 900, "K": INFINITY}


class State(Enum):
    IDLE = 1
    SEARCH = 2
    # PONDER = 3


class Searcher:
    def __init__(self):
        self.nodes = 0
        self.start_nanos = 0
        self.depth = 0
        self.state = State.IDLE


sea = Searcher()
board = chess.Board(START_FEN)


def mate_distancing(num):
    if num >= INFINITY - MATE_LIMIT:
        return num - 1
    if num <= -(INFINITY - MATE_LIMIT):
        return num + 1
    return num


def is_stm_white():
    return board.turn == chess.WHITE


def hit_blunt():
    # actually evaluation function
    score = 0
    for _, piece in board.piece_map().items():
        if piece is None:
            continue
        if piece.color is board.turn:
            score += VALUE[piece.symbol().upper()]
        else:
            score -= VALUE[piece.symbol().upper()]
    return score


def should_runsik():
    # called in IDDFS root
    if sea.state == State.IDLE:
        return True
    match clock.lim.mode:
        case clock.TimingMode.DEPTH:
            return sea.depth > clock.lim.depth
        case clock.TimingMode.NODES:
            return sea.nodes > clock.lim.nodes
        case mode if mode in [clock.TimingMode.MOVETIME, clock.TimingMode.TC]:
            # branching factor: dictates whether next ply's search can fully pass
            # if BF = 3, 3 / 1/(1-1/3) = x2 of used time is needed again
            bf = 20
            cur_nanos = perf_counter_ns()
            return (cur_nanos - sea.start_nanos) * (bf - 1) > clock.lim.movetime_nano()
        case _:
            return False


def should_runsik_nodes():
    # 'run every few thousand nodes or so': called at depth 3 left
    # (affected by general nodes per depth)
    if sea.state == State.IDLE:
        return True
    match clock.lim.mode:
        case clock.TimingMode.DEPTH:
            return sea.depth > clock.lim.depth
        case clock.TimingMode.NODES:
            return sea.nodes > clock.lim.nodes
        case mode if mode in [clock.TimingMode.MOVETIME, clock.TimingMode.TC]:
            # quit only if movetime is passed (different from root fx)
            cur_nanos = perf_counter_ns()
            return (cur_nanos - sea.start_nanos) > clock.lim.movetime_nano()
        case _:
            return False


def awake():
    # IDDFS function
    sea.nodes = 0
    sea.start_nanos = perf_counter_ns()
    sea.depth = 1
    while True:
        next_info = struggle(depth_remaining=sea.depth)
        if next_info is None:
            break
        (pv, score) = next_info
        end_nanos = perf_counter_ns()
        nanos_time = end_nanos - sea.start_nanos
        millis_time = trunc(nanos_time / 1_000_000)
        nps = trunc(sea.nodes * 1_000_000_000 / (nanos_time))
        pv_uci = list(map(lambda move: move.uci(), pv))
        print(
            f"info depth {sea.depth} score cp {score} "
            f"time {millis_time} nodes {sea.nodes} nps {nps} "
            f"pv {' '.join(pv_uci)}"
        )
        sys.stdout.flush()
        sea.depth += 1
        if should_runsik():
            break
    return pv_uci[0]


def struggle(
    alpha=-INFINITY, beta=INFINITY, depth_remaining=1
) -> tuple[list[chess.Move], int] | None:
    # actually search function

    if depth_remaining == 3 and should_runsik_nodes():
        return

    sea.nodes += 1

    if board.is_checkmate():
        return ([], -INFINITY)
    if board.is_stalemate():
        return ([], 0)

    if depth_remaining == 0:
        return ([], hit_blunt())

    moves = board.generate_legal_moves()
    pv: list[chess.Move] = []
    best_score = -INFINITY

    for move in moves:
        board.push(move)
        next_info = struggle(-beta, -alpha, depth_remaining - 1)
        if next_info is None:
            return None
        (following, score) = next_info
        score *= -1
        score = mate_distancing(score)
        board.pop()

        # fail-soft alpha-beta
        if score > best_score:
            best_score = score
            if score > alpha:
                pv = [move, *following]
                alpha = score
        if score >= beta:
            return ([], best_score)  # can also exceed beta

    return (pv, best_score)


def start():
    sea.state = State.SEARCH
    pain = threading.Thread(target=search, args=())
    pain.start()


def search():
    bm = awake()

    print(f"bestmove {bm}")
    print("info string ahnsik")
    sys.stdout.flush()


def stop():
    sea.state = State.IDLE
