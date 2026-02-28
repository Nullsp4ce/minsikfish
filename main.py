# pylint: disable=missing-module-docstring, missing-function-docstring

import threading
import sys
from engine import (
    START_FEN,
    awake,
    g,
    is_stm_white,
)
import clock


def wait():
    # print("uci.wait")
    should = True
    while should:
        should = parse(input())


def parse(read: str):
    commands = read.rstrip().split()
    command = commands.pop(0)
    intents = {
        "uci": uci,
        "isready": ready,
        "position": set_position,
        "ucinewgame": new_game,
        "print": d,
        "go": search_start,
        "stop": stop,
        "quit": quit_minsik,
    }
    try:
        intents[command](commands)
    except KeyError:
        # print(f"uci.parse: unsupported command {command}")
        pass
    return command != "quit"


def uci(commands):
    del commands
    print("id name Minsikfish 0.5")
    print("id author Nullsp4ce")
    # further options go here
    print("uciok")


def ready(commands):
    del commands
    print("readyok")


def new_game(commands):
    del commands
    g.board.set_fen(START_FEN)


def set_position(commands):
    # print("uci.set_position")
    consumed = 0
    mode = ""
    if len(commands) > 0:
        mode = commands[0]
    if mode == "startpos":
        g.board.set_fen(START_FEN)
        consumed = 1
    elif mode == "fen":
        # fully qualified FEN has 6 segments, but... oh no
        fen = " ".join(commands[1:7])
        g.board.set_fen(fen)
        consumed = 7  # ?

    if len(commands) > consumed:
        for move_uci in commands[consumed + 1 :]:
            g.board.push_uci(move_uci)


def d(commands):
    del commands
    print(g.board)


def search():
    bm = awake()

    # print when search is completed/stopped
    print(f"bestmove {bm}")
    print("info string ahnsik")
    sys.stdout.flush()


def search_start(commands):
    clock.lim = clock.from_cmd(is_stm_white(), commands)
    clock.state = clock.State.SEARCH
    pain = threading.Thread(target=search, args=())
    pain.start()


def stop(commands):
    del commands
    clock.state = clock.State.IDLE


def quit_minsik(commands):
    # print("uci.quit")
    stop(commands)


wait()
