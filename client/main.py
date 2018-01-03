from Tkinter import *
from client.client_gui import Application
from client.multiplayer_game import MultiplayerGame

'''
The main endpoint for client application. It starts GUI.
'''


class ContainerApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        app = Application(master=container, controller=self)
        app.grid(row=0, column=0, sticky="nsew")
        self.show_frame(app)

    def show_frame(self, frame):
        frame.tkraise()


if __name__ == "__main__":
    app = ContainerApp()
    app.mainloop()
