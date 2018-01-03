from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_error, timeout
from threading import Thread
import common.constants as C
from server.server_msg_processor import ServerMsgProcessor
from server.single_client_handler import SingleClientHandler
from sudoku_game import SudokuGame

'''
This class is tcp server itself. It accepts new connections from clients and assigns them to seperate threads.
If server is closed, then it stops all the threads.
'''


class TcpServer():
    def __init__(self, server_inet_addr=C.DEFAULT_SERVER_HOST, server_port=C.DEFAULT_SERVER_PORT):
        # constants
        self.SERVER_PORT = server_port
        self.SERVER_INET_ADDR = server_inet_addr
        self.__DEFAULT_SERVER_TCP_CLIENTS_QUEUE = 10
        # member vars
        self.__server_socket = None
        self.__running = False
        # init
        self.init_server()
        self.__client_threads = {}
        self.__active_games = {}

        self.__serving_thread = Thread(target=self.serve_forever)

    def start_server(self):
        self.__running = True
        self.__serving_thread.start()

    def init_server(self):
        self.__server_socket = socket(AF_INET, SOCK_STREAM)
        self.__server_socket.settimeout(2)
        C.LOG.debug('Server socket created, descriptor %d' % self.__server_socket.fileno())
        try:
            self.__server_socket.bind((self.SERVER_INET_ADDR, self.SERVER_PORT))
        except soc_error as e:
            C.LOG.error('Can\'t start server, error : %s' % str(e))
            exit(1)

        C.LOG.debug('Server socket bound on %s:%d' % self.__server_socket.getsockname())
        self.__server_socket.listen(self.__DEFAULT_SERVER_TCP_CLIENTS_QUEUE)
        C.LOG.info('Accepting requests on TCP %s:%d' % self.__server_socket.getsockname())

    def add_new_game(self, game_name, max_players):
        sudoku_game = SudokuGame(game_name, max_players)
        self.__active_games[sudoku_game.get_id()] = sudoku_game
        return sudoku_game.get_id()

    def add_player(self, game_id, username, source):
        if self.__active_games.has_key(game_id):
            sudoku_game = self.__active_games[game_id]
            sudoku_game.add_player(username, source)
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
        while self.__running:
            try:
                client_socket, source = self.__server_socket.accept()
                client_thread = SingleClientHandler(
                    kwargs={'source': source, 'client_socket': client_socket, 'server': self})
                client_thread.start()
                self.__client_threads[source] = client_thread

            except (timeout):
                C.LOG.info('Awaiting connections...')
            except (soc_error) as e:
                C.LOG.error('Interrupted receiving the data from %s:%d, ' \
                            'error: %s' % (source + (e,)))
                continue

    def stop_server(self):
        self.__running = False
        self.__server_socket.close()
        self.__serving_thread.join()
        for client_thread in self.__client_threads.values():
            client_thread.stop()
            client_thread.join()
        C.LOG.info('Server closed')
