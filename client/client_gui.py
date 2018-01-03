from Tkinter import *
import tkMessageBox
import common.constants as C
from client.rpc_client import RpcClient
from multiplayer_game import MultiplayerGame

'''
Here is defined client GUI.
'''


class Application(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.host_input = None
        self.port_input = None
        self.user_input = None
        self.user_listbox_var = StringVar(self)
        #
        self.client = None
        self.pack()
        self.create_widgets()
        self.host = None
        self.port = None
        self.username = None

    def connect_to_server(self):
        self.host = self.host_input.get()
        self.port = int(self.port_input.get())
        self.username = self.user_input.get()

        if self.host is None:
            self.show_info("Error: no server host specified")
            return

        if self.port is None:
            self.show_info("Error: no server port specified")
            return

        if not self.check_username():
            self.show_info(
                "Error: username {} not valid. It should containt only alphanumeric characters and must not be longer than 8 characters.".format(
                    self.username))
            return

        self.client = RpcClient(host=self.host, port=self.port)
        if self.client.is_connected():
            self.show_info("Connected to server!")
            self.open_multiplayer_game()
        else:
            self.show_info("Error: connecting to server failed!")

    def open_multiplayer_game(self):
        multiplayer_game = MultiplayerGame(client=self.client, username=self.username, master=self.master,
                                           controller=self.controller)
        multiplayer_game.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame(multiplayer_game)

    def check_username(self):
        self.username = self.user_input.get()

        if not re.match('^[a-zA-Z0-9_]+$', self.username) or len(self.username) > 8:
            return False

        return True

    def create_widgets(self):
        QUIT = Button(self)
        QUIT["text"] = "QUIT"
        QUIT["fg"] = "red"
        QUIT["command"] = self.quit
        QUIT.grid(row=3, column=1)

        Label(self, text="Server port").grid(row=0)
        self.port_input = Entry(self)
        self.port_input.insert(0, str(C.DEFAULT_SERVER_PORT))
        self.port_input.grid(row=0, column=1)

        Label(self, text="Server host").grid(row=1)
        self.host_input = Entry(self)
        self.host_input.insert(0, str(C.DEFAULT_SERVER_HOST))
        self.host_input.grid(row=1, column=1)

        Label(self, text="Username").grid(row=2)
        self.user_input = Entry(self)
        self.user_input.insert(0, "(insert user name)")
        self.user_input.grid(row=2, column=1)

        connect_to_server = Button(self)
        connect_to_server["text"] = "CONNECT TO SERVER"
        connect_to_server["command"] = self.connect_to_server
        connect_to_server.grid(row=3, column=0)

        self.user_listbox_var.set("Choose a nickname")
        self.user_listbox_var.trace('w', self.on_dropdown_changed)
        self.user_listbox = OptionMenu(self, self.user_listbox_var, "Brain112", "Sudoku15", "WhatYou")
        self.user_listbox.grid(row=2, column=2)

    def on_dropdown_changed(self, index, value, op):
        self.user_input.delete(0, 'end')
        self.user_input.insert(0, self.user_listbox_var.get())

    def show_info(self, info_msg):
        C.LOG.info(info_msg)
        tkMessageBox.showinfo("Message", info_msg)
