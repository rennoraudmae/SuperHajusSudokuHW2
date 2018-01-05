from threading import Thread
import common.constants as C
from server.rpc_server_msg_processor import RpcServerMsgProcessor
from sudoku_game import SudokuGame
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import socket
import struct

'''
This class is tcp server itself. It accepts new connections from clients and assigns them to seperate threads.
If server is closed, then it stops all the threads.
'''

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class RpcServer():
    def __init__(self, server_inet_addr=C.DEFAULT_SERVER_HOST, server_port=C.DEFAULT_SERVER_PORT, server_name=None):
        # constants
        self.SERVER_PORT = server_port
        self.SERVER_INET_ADDR = server_inet_addr
        self.__DEFAULT_SERVER_TCP_CLIENTS_QUEUE = 10
        # member vars
        self.__server_socket = None
        self.__running = False
        self.__processor = RpcServerMsgProcessor(server=self)
        # init
        self.__server = None
        self.init_server()
        self.__client_threads = {}
        self.__active_games = {}
        self.server_name = server_name

        self.__discovery_thread = Thread(target=self.discovery_loop)
        self.__serving_thread = Thread(target=self.serve_forever)

    def start_server(self):
        self.__running = True
        self.__serving_thread.start()
        self.__discovery_thread.start()

    def init_server(self):
        try:
            self.__server = SimpleXMLRPCServer((self.SERVER_INET_ADDR, self.SERVER_PORT), requestHandler=RequestHandler)
            self.__server.register_introspection_functions()
            self.__server.register_instance(self.__processor)
        except Exception as e:
            C.LOG.error("Error while starting the server: {}".format(e))

    def add_new_game(self, game_name, max_players):
        sudoku_game = SudokuGame(game_name, max_players)
        self.__active_games[sudoku_game.get_id()] = sudoku_game
        return sudoku_game.get_id()

    def add_player(self, game_id, username):
        if self.__active_games.has_key(game_id):
            sudoku_game = self.__active_games[game_id]
            sudoku_game.add_player(username)
            return True
        else:
            return False

    def remove_player(self, game_id, username):
        sudoku_game = self.__active_games[game_id]
        sudoku_game.remove_player(username)

    def get_all_games(self):
        return self.__active_games.values()

    def get_game_field(self, game_id):
        sudoku_game = self.__active_games[game_id]
        return sudoku_game.get_game_field()

    def get_game_state(self, game_id):
        sudoku_game = self.__active_games[game_id]
        if sudoku_game.game_over():
            return sudoku_game.get_winner()
        else:
            return False

    def check_nr(self, game_id, username, nr, address):
        sudoku_game = self.__active_games[game_id]
        return sudoku_game.check_nr(nr, address, username)

    def get_game_player_list(self, game_id):
        sudoku_game = self.__active_games[game_id]
        return sudoku_game.get_players()

    def serve_forever(self):
        try:
            self.__server.serve_forever()
        finally:
            C.LOG.info('Server stopped')

    def discovery_loop(self):
        # init multicast
        multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        multicast_sock.bind(('', C.MULTICAST_GROUP_PORT))
        group = socket.inet_aton(C.MULTICAST_GROUP_ADDR)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            data, address = multicast_sock.recvfrom(1024)
            if data == C.WHO_IS_THERE:
                message = '%s:%s:%s' % (self.server_name, self.SERVER_INET_ADDR, self.SERVER_PORT)
                multicast_sock.sendto(message, address)

    def stop_server(self):
        self.__running = False
        self.__server.shutdown()
        self.__server.server_close()
        self.__serving_thread.join()

        for client_thread in self.__client_threads.values():
            client_thread.stop()
            client_thread.join()
        C.LOG.info('Server closed')
