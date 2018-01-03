from Tkinter import *
import common.constants as C
from server.tcp_server import TcpServer

'''
Here is defined server GUI
'''

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.server = None
        self.pack()
        self.host_input = None
        self.port_input = None
        self.files_input = None
        self.start_server_btn = None
        self.create_widgets()

    def start_server(self):
        host = self.host_input.get()
        port = int(self.port_input.get())
        self.server = TcpServer(server_inet_addr=host, server_port=port)
        self.server.start_server()
        self.start_server_btn['state'] = DISABLED

    def stop_server(self):
        if self.server != None:
            self.server.stop_server()
        self.quit()

    def create_widgets(self):
        QUIT = Button(self)
        QUIT["text"] = "QUIT"
        QUIT["fg"] = "red"
        QUIT["command"] = self.stop_server
        QUIT.grid(row=3, column=1)

        Label(self, text="Server port").grid(row=0)
        self.port_input = Entry(self)
        self.port_input.insert(0, str(C.DEFAULT_SERVER_PORT))
        self.port_input.grid(row=0, column=1)

        Label(self, text="Server host").grid(row=1)
        self.host_input = Entry(self)
        self.host_input.insert(0, str(C.DEFAULT_SERVER_HOST))
        self.host_input.grid(row=1, column=1)

        self.start_server_btn = Button(self)
        self.start_server_btn["text"] = "Start server"
        self.start_server_btn["command"] = self.start_server
        self.start_server_btn.grid(row=3, column=0)
