from engine import Minsikfish, START_FEN
import threading
import time


class Uci:

    def __init__(self, minsik: Minsikfish):
        self.minsik = minsik
        self.wait()

    def wait(self):
        # print("uci.wait")
        should = True
        while should:
            should = self.parse(input())

    def parse(self, read: str):
        commands = read.rstrip().split()
        command = commands.pop(0)
        intents = {
            "uci": self.uci,
            "isready": self.ready,
            "position": self.set_position,
            "ucinewgame": self.new_game,
            "print": self.d,
            "go": self.search_start,
            "quit": self.quit,
        }
        try:
            intents[command](commands)
        except KeyError:
            # print(f"uci.parse: unsupported command {command}")
            pass
        return command != "quit"

    def uci(self, commands):
        print("id name Minsikfish 0.2-take8")
        print("id author Nullsp4ce")
        # further options go here
        print("uciok")

    def ready(self, commands):
        print("readyok")

    def new_game(self, commands):
        self.minsik.board.set_fen(START_FEN)

    def set_position(self, commands):
        # print("uci.set_position")
        consumed = 0
        mode = commands[0]
        if mode == "startpos":
            self.minsik.board.set_fen(START_FEN)
            consumed = 1
        elif mode == "fen":
            # fully qualified FEN has 6 segments, but... oh no
            fen = " ".join(commands[1:7])
            self.minsik.board.set_fen(fen)
            consumed = 7  # ?

        if len(commands) > consumed:
            for move_uci in commands[consumed + 1 :]:
                self.minsik.board.push_uci(move_uci)

    def d(self, commands):
        print(self.minsik.board)

    def search(self):
        best_move = self.minsik.struggle()
        if best_move is None:
            print("info string ahnsik")
            return

        print(f"info depth 1 pv {best_move.uci()}")
        print(f"bestmove {best_move}")

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
