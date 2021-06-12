# coding: utf-8
from game import *


def app():
    """アプリケーション"""

    tetris = Tetris(None)
    gui = GUI(tetris)

    tetris.gui = gui

    gui.mainloop()


if __name__=="__main__":
    app()
