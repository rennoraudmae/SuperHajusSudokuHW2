import re
import random
from common.custom_exceptions import LogicException
from server.player import Player


class SudokuGame():
    def __init__(self, game_name, max_players=2):
        self.game_name = game_name
        self.max_players = int(max_players)
        self.__id = re.sub('[^A-Za-z0-9]+', '', self.game_name)
        self.players = {}
        self.game_field, self.solution = self.__generate_puzzle()
        self.field_change_func = self.do_nothing

    def do_nothing(self, arg):
        pass

    def set_field_change_func(self, func):
        self.field_change_func = func

    def get_id(self):
        return self.__id

    def __generate_puzzle(self):
        sudoku = [['-', 1, '-', '-', 2, '-', '-', 3, '-'],
                  ['-', 9, '-', '-', '-', 4, '-', '-', '-'],
                  ['-', 7, '-', '-', 5, '-', 1, '-', '-'],
                  [2, '-', 1, '-', '-', '-', '-', '-', 9],
                  ['-', '-', '-', '-', 8, 1, '-', 5, '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-', 4],
                  [9, '-', '-', 5, '-', '-', '-', '-', 2],
                  ['-', '-', '-', 6, '-', '-', '-', '-', 3],
                  [3, '-', '-', '-', '-', '-', 7, '-', '-']]
        solution = [[5, 1, 4, 8, 2, 6, 9, 3, 7],
                    [8, 9, 3, 1, 7, 4, 6, 2, 5],
                    [6, 7, 2, 3, 5, 9, 1, 4, 8],
                    [2, 8, 1, 4, 6, 5, 3, 7, 9],
                    [4, 3, 9, 7, 8, 1, 2, 5, 6],
                    [7, 5, 6, 9, 3, 2, 8, 1, 4],
                    [9, 6, 7, 5, 1, 3, 4, 8, 2],
                    [1, 2, 8, 6, 4, 7, 5, 9, 3],
                    [3, 4, 5, 2, 9, 8, 7, 6, 1]]
        return (sudoku, solution)

    def check_nr(self, nr, address, username):
        x = int(address[1])
        y = int(address[4])
        try:
            if self.game_field[x][y] == int(nr):
                return False
            if self.solution[x][y] == int(nr):
                self.__add_nr(nr, (x, y))
                self.players[username].increase_score()
                return True
        except ValueError:
            return False
        self.players[username].decrease_score()
        return False

    def __add_nr(self, nr, address):
        x, y = address
        self.game_field[x][y] = int(nr)

    def game_over(self):
        if self.game_field == self.solution:
            return True
        if len(self.players) < 1:
            return True
        return False

    def get_winner(self):
        winner = None
        for player in self.players.values():
            if winner == None or int(winner.get_score()) < int(player.get_score()):
                winner = player
        if winner is None:
            return ""
        return winner.get_username()

    def add_player(self, username):
        if self.players.has_key(username):
            raise LogicException("There is already someone in this game named {}".format(username))

        if len(self.players.values()) >= self.max_players:
            raise LogicException("Maximum number of players reached!")
        player = Player(username)
        self.players[username] = player
        self.trigger_field_change()

    def remove_player(self, username):
        del self.players[username]
        self.trigger_field_change()

    def get_game_field(self):
        return self.game_field

    def get_players(self):
        return self.players

    def trigger_field_change(self):
        self.field_change_func(self.__id)
