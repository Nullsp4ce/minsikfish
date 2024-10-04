from enum import Enum

# 24 +2 which is for the buffer below
moves_to_go_default = 26
buffer_millis = 200
buffer_moves = 2


class TimingMode(Enum):
    DEPTH = 1
    NODES = 2
    MOVETIME = 3
    TC = 4
    INFINITE = 5


class SearchLimiter:
    def __init__(self, mode: TimingMode, depth=0, nodes=0, movetime=0):
        self.mode = mode
        self.depth = depth
        self.nodes = nodes
        self.movetime = movetime


def from_fixed(movetime: int):
    if movetime > buffer_millis:
        return movetime - buffer_millis
    else:
        return 0


def lim_from_fixed(movetime: int):
    return SearchLimiter(TimingMode.MOVETIME, movetime=from_fixed(movetime))


def from_tc(is_white: bool, wtime, btime, winc, binc, movestogo):
    if movestogo > 0:
        moves_to_go_actual = movestogo + buffer_moves
    else:
        moves_to_go_actual = moves_to_go_default
    if is_white:
        movetime = winc + wtime / moves_to_go_actual
    else:
        movetime = binc + btime / moves_to_go_actual
    return from_fixed(movetime)


def lim_from_tc(is_white: bool, wtime, btime, winc, binc, movestogo):
    movetime = from_tc(is_white, wtime, btime, winc, binc, movestogo)
    return SearchLimiter(TimingMode.TC, movetime=movetime)
