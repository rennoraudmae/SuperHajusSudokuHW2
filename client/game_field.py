from Tkinter import *
import tkMessageBox
import common.constants as C
from client.rpc_client import RpcClient
from common.custom_exceptions import LogicException
import threading
import time

"""
This is GUI for playing the game.
"""

class GameField(Frame):
    def __init__(self, master, controller, client, game_id, username):
        Frame.__init__(self, master=master)
        self.master = master
        self.controller = controller
        self.game_matrix = []
        self.canvas = Canvas(self, width=C.FIELD_SIDE, height=C.FIELD_SIDE)
        self.canvas.grid(row=0, column=1)
        self.canvas.bind("<Button-1>", self.button_click)
        self.canvas.bind("<Key>", self.key_press)
        self.focused_cell = None
        self.draw_field()
        self.player_board = Listbox(self, height=30, width=20)
        self.draw_player_list()
        self.draw_buttons()
        self.client = client
        self.game_id = game_id
        self.username = username
        self.update_field_from_server()
        self.game_over = False
        self.game_winner = ""

        receive_thread = threading.Thread(target=self.update_field_thread, args=())
        receive_thread.start()

    def update_field_from_server(self):
        self.game_matrix = self.client.request_game_field(self.game_id)
        self.draw_numbers()

    def update_game_state_from_server(self):
        state = self.client.request_game_state(self.game_id)
        if state is False:
            return
        else:
            self.game_winner = state
            self.game_over = True

    def update_players_list_from_server(self):
        players_list = self.client.request_players(self.game_id)
        self.update_players_list(players_list)

    def update_field_thread(self):
        while not self.game_over:
            self.update_game_state_from_server()
            self.update_field_from_server()
            self.update_players_list_from_server()
            time.sleep(0.5)

    def key_press(self, event):
        key = event.char
        if key in '123456789':
            address = self.focused_cell
            self.client.check_nr(key, address, self.username, self.game_id)


    def button_click(self, event):

        if self.canvas.find_withtag(CURRENT):
            self.canvas.focus_set()
            tags = [tag for tag in self.canvas.gettags(CURRENT)]
            if 'cell' in tags:
                if self.focused_cell != None:
                    self.canvas.itemconfig('cell', width=1, outline='black')
                    self.canvas.tag_lower('cell')
                    self.canvas.update_idletasks()
                self.focused_cell = (int(tags[0][0]), int(tags[0][1]))
                self.canvas.itemconfig(CURRENT, width=3, outline='red')
                self.canvas.tag_raise(CURRENT)
                self.canvas.tag_raise('numbers')
                self.canvas.update_idletasks()


    def draw_field(self):
        #draws sudoku field on the canvas
        #each cell is drawn as rectangle and after that larger rectangles
        #are drawn on top to highlight 3x3 box borders

        for i in range(9):
            for j in range(9):
                x0 = C.PADDING + j * C.CELL_SIDE
                y0 = C.PADDING + i * C.CELL_SIDE
                x1 = x0 + C.CELL_SIDE
                y1 = y0 + C.CELL_SIDE
                self.canvas.create_rectangle(x0, y0, x1, y1, tags=('%d%d'%(i,j), 'cell'), fill='white')
        for i in range(3):
            for j in range(3):
                x0 = C.PADDING + i*3 * C.CELL_SIDE
                y0 = C.PADDING + j*3 * C.CELL_SIDE
                x1 = x0 + 3 * C.CELL_SIDE
                y1 = y0 + 3 * C.CELL_SIDE
                self.canvas.create_rectangle(x0, y0, x1, y1, width=3)

    def draw_numbers(self):
        self.canvas.delete('numbers')
        for i in range(9):
            for j in range(9):
                number = self.game_matrix[j][i]
                if not isinstance(number,int):
                    continue
                x=C.PADDING + i * C.CELL_SIDE + 0.5 * C.CELL_SIDE
                y=C.PADDING + j * C.CELL_SIDE + 0.5 * C.CELL_SIDE
                self.canvas.create_text(x, y, text=str(number), font=('Arial', 24,'bold'), tags='numbers')

    def draw_player_list(self):
        self.player_board.grid(row=0, column=0, padx=10, pady=10, sticky='wens')

    def update_players_list(self, players):
        self.player_board.delete(0, END)
        if self.game_over:
            self.player_board.insert(0, "Winner is {}".format(self.game_winner))
            return
        self.player_board.insert(0, "Player   -   Score")
        for i, player in enumerate(players):
            player_str = "{}   -   {}".format(player[0], player[1])
            self.player_board.insert(i+1,  player_str)

    def draw_buttons(self):
        create_new_game_button = Button(self)
        create_new_game_button["text"] = "Leave Game"
        create_new_game_button["command"] = self.leave_game
        create_new_game_button.grid(row=3, column=0)

    def leave_game(self):
        self.client.leave_game(self.game_id, self.username)
        self.destroy()




