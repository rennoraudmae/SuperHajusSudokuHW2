from Tkinter import *
import tkMessageBox
import common.constants as C
from client.rpc_client import RpcClient
from multiplayer_game import MultiplayerGame
import socket
import struct
from time import sleep
'''
Here is defined client GUI.
'''


class Application(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.host_input = None
        self.port_input = None
        self.user_input = None

        #
        self.client = None
        #self.pack()
        self.user_listbox_var = StringVar(self)
        self.create_widgets()
        self.host = None
        self.port = None
        self.available_servers = {}
        self.username = None



    def connect_to_server(self):
        self.username = self.user_input.get()

        if len(self.server_list.curselection()) == 0:
            self.show_info("Error: No server selected.")
            return
        else:
            index = int(self.server_list.curselection()[0])
            serv_name = self.server_list.get(index)
            self.host, self.port = self.available_servers[serv_name]
            C.LOG.info('Connecting to %s:%s' % (self.host, self.port))

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
        self.server_list.grid_forget()
        multiplayer_game = MultiplayerGame(client=self.client, username=self.username, master=self.master,
                                           controller=self.controller)
        multiplayer_game.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame(multiplayer_game)

    def check_username(self):
        self.username = self.user_input.get()

        if not re.match('^[a-zA-Z0-9_]+$', self.username) or len(self.username) > 8:
            return False

        return True

    def __timeout_callback(self):
        self.receive_channel.close()

    def who_is_there(self):
        #code based on: https://pymotw.com/2/socket/multicast.html
        multicast_group = (C.MULTICAST_GROUP_ADDR, C.MULTICAST_GROUP_PORT)
        multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        multicast_sock.settimeout(0.2)
        ttl = struct.pack('b', 1)
        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.server_list.delete(1,END)
        self.available_servers = {}
        try:
            multicast_sock.sendto(C.WHO_IS_THERE, multicast_group)
            while True:
                try:
                    data, server = multicast_sock.recvfrom(1024)
                except socket.timeout:
                    break
                else:
                    data = data.split(C.DELI)
                    name = data[0]
                    addr = data[1]
                    port = int(data[2])
                    if len(name) == 0:
                        name = 'nameless'
                    while name in self.available_servers:
                        name = name + '0'
                    self.server_list.insert(END, name)
                    self.available_servers[name] = (addr, port)
        finally:
            multicast_sock.close()
    def create_widgets(self):
        QUIT = Button(self)
        QUIT["text"] = "QUIT"
        QUIT["fg"] = "red"
        QUIT["command"] = self.quit
        QUIT.grid(row=4, column=1)

        Label(self, text="Username").grid(row=2)
        self.user_input = Entry(self)
        self.user_input.insert(0, "(insert user name)")
        self.user_input.grid(row=2, column=1)

        connect_to_server_btn = Button(self)
        connect_to_server_btn["text"] = "CONNECT TO SERVER"
        connect_to_server_btn["command"] = self.connect_to_server
        connect_to_server_btn.grid(row=4, column=0)

        get_server_list = Button(self)
        get_server_list["text"] = "Find servers"
        get_server_list["command"] = self.who_is_there
        get_server_list.grid(row=3, column=0)

        self.server_list = Listbox(self.master, selectmode=SINGLE, height=5, width=40)
        self.server_list.grid(row=3, column=0)


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
