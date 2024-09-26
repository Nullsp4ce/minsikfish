from engine import Minsikfish, START_FEN
import threading
import time


class Uci:

    def __init__(self, minsik: Minsikfish):
        self.minsik = minsik
        self.wait()

    def wait(self):
        # print("uci.wait")
        self.parse(input())

    def parse(self, read: str):
        commands = read.rstrip().split()
        command = commands.pop(0)
        intents = {
            "uci": self.uci,
            "isready": self.ready,
            "position": self.set_position,
            "ucinewgame": self.new_game,
            "go": self.search_start,
            "quit": self.quit,
        }
        try:
            intents[command]()
        except KeyError:
            # print(f"uci.parse: unsupported command {command}")
            pass
        if command != "quit":
            self.wait()

    def uci(self, *commands):
        print("id name Minsikfish 0.1")
        print("id author Nullsp4ce")
        # further options go here
        print("uciok")

    def ready(self, *commands):
        print("readyok")

    def new_game(self, *commands):
        self.minsik.board.set_fen(START_FEN)

    def set_position(self, mode, *commands):
        # print("uci.set_position")
        if mode == "startpos":
            self.minsik.board.set_fen(START_FEN)
        elif mode == "fen":
            fen = commands.pop(0)
            self.minsik.board.set_fen(fen)

    def search(self):
        best_move = self.minsik.struggle()
        if best_move is None:
            print("info string ahnsik")
            return

        print(f"info depth 1 pv {best_move.uci()}")
        print(f"bestmove ${best_move}")

    def search_start(self, *commands):
        pain = threading.Thread(target=self.search, args=())
        pain.start()

    def quit(self, *commands):
        # print("uci.quit")
        return


def main():
    Uci(Minsikfish())


if __name__ == "__main__":
    main()
