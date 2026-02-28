# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from enum import Enum

# 24 +2 which is for the buffer below
moves_to_go_default = 26
buffer_millis = 200
buffer_moves = 2


class State(Enum):
    IDLE = 1
    SEARCH = 2
    # PONDER = 3


state: State = State.IDLE


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


lim: SearchLimiter


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


def lim_from_tc_from_str(is_stm_white, commands):
    wtime = 0
    btime = 0
    winc = 0
    binc = 0
    movestogo = 0
    pairs = [commands[i * 2 : (i + 1) * 2] for i in range(int(len(commands) / 2))]

    for [key, value] in pairs:
        match key:
            case "wtime":
                wtime = int(value)
            case "btime":
                btime = int(value)
            case "winc":
                winc = int(value)
            case "binc":
                binc = int(value)
            case "movestogo":
                movestogo = int(value)
    return lim_from_tc(is_stm_white, wtime, btime, winc, binc, movestogo)


def from_cmd(is_stm_white, commands):
    mode = ""
    if len(commands) > 0:
        mode = commands.pop(0)
    match mode:
        case "depth":
            value = int(commands.pop(0))
            return SearchLimiter(TimingMode.DEPTH, depth=value)
        case "nodes":
            value = int(commands.pop(0))
            return SearchLimiter(TimingMode.NODES, nodes=value)
        case "movetime":
            value = int(commands.pop(0))
            return lim_from_fixed(value)
        case item if item in ["wtime", "btime", "winc", "binc", "movestogo"]:
            return lim_from_tc_from_str(is_stm_white, [mode, *commands])
        case _:
            return SearchLimiter(TimingMode.INFINITE)
