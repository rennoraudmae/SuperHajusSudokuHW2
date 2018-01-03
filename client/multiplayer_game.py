from Tkinter import *
import tkMessageBox
import common.constants as C
from client.rpc_client import RpcClient
from client.game_field import GameField
from common.custom_exceptions import LogicException

"""
This is GUI for connecting and creating a new sudoku game.
"""

class MultiplayerGame(Frame):
    def __init__(self, client, username, master, controller):
        Frame.__init__(self, master=master)
        self.controller = controller
        self.master = master
        self.controller.title('SuperHajusSudoku Client')
        #
        self.game_name_input = None
        self.all_games_var = StringVar()
        self.all_games_var.set("")
        self.max_users_input = None
        self.join_session_input = None     
        #
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.client = client
        self.username = username
        self.create_widgets()
        #

    def create_widgets(self):
        # Row 0
        Label(self, text="Logged in user: {}".format(self.username)).grid(row=0, column=0)
        # Row 1

        # Row 2
        Label(self, text="Create new game").grid(row=2, column=0)
        self.game_name_input = Entry(self)
        self.game_name_input.insert(0, "(insert game name)")
        self.game_name_input.grid(row=2, column=1)
        self.max_users_input = Entry(self)
        self.max_users_input.insert(0, "(insert max players number)")
        self.max_users_input.grid(row=2, column=2)
        # Row 3
        create_new_game_button = Button(self)
        create_new_game_button["text"] = "Create new game"
        create_new_game_button["command"] = self.create_new_game
        create_new_game_button.grid(row=3, column=1)
        # Row 4
        Label(self, text="Available games:").grid(row=4, column=0)
        Label(self, textvariable=self.all_games_var).grid(row=4, column=1)
        get_games_button = Button(self)
        get_games_button["text"] = "Refresh games list",
        get_games_button["command"] = self.retreive_all_games
        get_games_button.grid(row=5, column=2)
        # Row 5,6
        Label(self, text="Join a game inserting id").grid(row=5, column=0)
        self.join_session_input = Entry(self)
        self.join_session_input.insert(0, "(insert game id)")
        self.join_session_input.grid(row=6, column=0)
        join_game_btn = Button(self)
        join_game_btn["text"] = "Join game",
        join_game_btn["command"] = self.join_game
        join_game_btn.grid(row=6, column=1)

        self.retreive_all_games()

    def join_game(self):
        game_id = self.join_session_input.get()
        if len(game_id) <= 0:
            tkMessageBox.showerror("Message", "Please provide a game ID")
            return
        try:
            self.client.join_game(game_id, self.username)
            self.open_game_frame(game_id)
        except LogicException as e:
            tkMessageBox.showerror("Error", e.message)
        
    def open_game_frame(self, game_id):
        field = GameField(master=self.master, controller=self.controller,client=self.client, game_id=game_id, username=self.username)
        field.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame(field)

    def retreive_all_games(self):
        self.all_games_var.set(self.client.get_all_games())

    def create_new_game(self):
        if len(self.game_name_input.get()) <= 0:
            tkMessageBox.showinfo("Message", "Please provide a game name")
            return
        if self.game_name_input.get() in self.all_games_var.get():
            tkMessageBox.showinfo("Message", "Game with this name allready exists.")
            return
        try:
            max_players = int(self.max_users_input.get())
        except ValueError:
            tkMessageBox.showinfo("Message", "Please provide valid max players number")
            return

        try:
            new_game_id = self.client.new_game_request(self.game_name_input.get(), max_players)
            self.retreive_all_games()
            tkMessageBox.showinfo("New game created", "New game create with id: {}".format(new_game_id))
        except LogicException as e:
            tkMessageBox.showerror("Error", e.message)

