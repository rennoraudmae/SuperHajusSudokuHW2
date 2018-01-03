from server.tcp_server import TcpServer
from Tkinter import *
from server.server_gui import Application

'''
The main endpoint for server application. It starts GUI.
'''

def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()


if __name__ == "__main__":
    main()
