import os
from collections import deque
from game.board import Board
from game.controllers import PlayerController, AiController
from game.settings import *

__author__ = 'bengt'


class Game(object):
    """Game ties everything together. It has a board,
    two controllers, and can draw to the screen."""

    def __init__(self, timeout=1000,
                 display_moves=True,
                 players=['ai', 'ai'],
                 colour=False):
        self.board = Board(colour)
        self.timeout = timeout
        self.ai_counter = 0

        self.list_of_colours = [BLACK, WHITE]
        self.players = players
        self.display_moves = display_moves

        self.controllers = deque([self._make_controller(c, p) for c, p in zip(self.list_of_colours, self.players)])
        self.player = self.controllers[0].get_colour()

        self.board.set_black(4, 3)
        self.board.set_black(3, 4)
        self.board.set_white(4, 4)
        self.board.set_white(3, 3)

        self.board.mark_moves(self.player)

        self.previous_move = None

    def _make_controller(self, colour, controller_type):
        if controller_type == 'player':
            return PlayerController(colour)
        else:
            self.ai_counter += 1
            return AiController(self.ai_counter, colour, self.timeout)

    def show_info(self):
        print("Playing as:       " + self.player)
        print("Displaying moves: " + str(self.display_moves))
        print("Current turn:     " + str(self.controllers[0]))
        print("Number of Black:  " + str(
            len([p for p in self.board.pieces if p.get_state() == BLACK])))
        print("Number of White:  " + str(
            len([p for p in self.board.pieces if p.get_state() == WHITE])))

    def show_board(self):
        self.player = self.controllers[0].get_colour()
        self.board.mark_moves(self.player)
        print(self.board.draw())

    def show_commands(self):
        moves = [self.to_board_coordinates(piece.get_position()) for piece in self.board.get_move_pieces(self.player)]

        if not moves:
            raise NoMovesError

        print("Possible moves are: ", moves)
        self.board.clear_moves()

    def run(self):
        while True:
            os.system('clear')
            self.show_info()

            self.show_board()

            try:
                self.show_commands()

                next_move = self.controllers[0].next_move(self.board)
                self.board.make_move(next_move, self.controllers[0].get_colour())
            except NoMovesError:
                print("Game Over")
                blacks = len([p for p in self.board.pieces if p.get_state() == BLACK])
                whites = len([p for p in self.board.pieces if p.get_state() == WHITE])
                if blacks > whites:
                    print("Black won this game.")
                    exit()
                elif blacks == whites:
                    print("This game was a tie.")
                    exit()
                else:
                    print("White won this game.")
                    exit()

            self.controllers.rotate()

            print("Current move is: ", self.to_board_coordinates(next_move))

            self.previous_move = next_move

    def to_board_coordinates(self, coordinate):
        x, y = coordinate
        return '{0}{1}'.format(chr(ord('a') + x), y + 1)