import ntpath
import common.constants as C
from common.custom_exceptions import CommunicationException, LogicException
from common.message_publisher import MessagePublisher
from common.message_receiver import MessageReceiver
from common.object_factory import ObjectFactory
from client.client_msg_processor import ClientMsgProcessor
import common.message_types as T
from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_error, timeout
import threading
import time
import sys

'''
This is main class for TCP client. It establishes a connection with server.
It also initializes sending different commands to server and receives responses from server.
'''


class TcpClient():
    def __init__(self, host=C.DEFAULT_SERVER_HOST, port=C.DEFAULT_SERVER_PORT):
        self.__host = host
        self.__port = port
        self.__connected = False
        self.__running = True
        self.__game_field = []
        self.__lock = threading.Lock()

        try:
            self.__socket = socket(AF_INET, SOCK_STREAM)
            self.__socket.connect((self.__host, self.__port))
            self.__socket.settimeout(60)
            self.__connected = True
        except Exception as e:
            C.LOG.error('Can\'t connect to server, error : %s' % str(e))
            return

        self.__message_publisher = MessagePublisher(socket=self.__socket)
        self.__message_receiver = MessageReceiver(socket=self.__socket, processor=ClientMsgProcessor(self))

    def is_connected(self):
        return self.__connected

    def update_field(self, field):
        self.__game_field = field

    def request_game_state(self, game_id):
        msg, type = self.__send_message_threadsafe(game_id, T.REQ_GAME_STATE)
        if type == T.RESP_OK:
            C.LOG.info("Game still running")
            return False
        else:
            return msg

    def send_message(self, message):
        msg, type = self.__send_message_threadsafe(message, T.REQ_SIMPLE_MESSAGE)
        if type == T.RESP_OK:
            C.LOG.info("Got answer to simple message: {}".format(msg))
        else:
            C.LOG.warning(msg)

    def new_game_request(self, game_name, max_players):
        msg, type = self.__send_message_threadsafe("{}:{}".format(game_name, max_players), T.REQ_NEW_GAME)
        if type == T.RESP_OK:
            C.LOG.info("New game created with id: {}".format(msg))
            return msg
        else:
            C.LOG.warning(msg)
            raise LogicException("New game creation failed with message: {}".format(msg))

    def join_game(self, game_id, username):
        msg, type = self.__send_message_threadsafe("{}:{}".format(game_id, username), T.REQ_JOIN_GAME)
        if type == T.RESP_OK:
            C.LOG.info("Joined game with id: {}".format(game_id))
        else:
            C.LOG.warning(msg)
            raise LogicException("New game creation failed with message: {}".format(msg))

    def leave_game(self, game_id, username):
        msg, type = self.__send_message_threadsafe("{}:{}".format(game_id, username), T.REQ_LEAVE_GAME)
        if type == T.RESP_OK:
            C.LOG.info("Left game with id: {}".format(game_id))
        else:
            C.LOG.warning(msg)
            raise LogicException("Leaving game failed with: {}".format(msg))

    def get_all_games(self):
        msg, type = self.__send_message_threadsafe(" ", T.REQ_ALL_GAMES)
        if type == T.RESP_OK:
            return msg
        else:
            C.LOG.warning(msg)
            raise LogicException("Game requesting failed with error: {}".format(msg))
    
    def check_nr(self, nr, address, username, game_id):
        msg, type = self.__send_message_threadsafe("{}:{}:{}:{}".format(nr, address, game_id, username), T.REQ_CHECK_NR)
        if type == T.RESP_OK:
            return msg
        if type == T.RESP_NOK:
            return msg
        else:
            C.LOG.warning(msg)
            raise LogicException("Game requesting failed with error: {}".format(msg))
    
    def get_game_field(self):
        return self.__game_field

    def request_game_field(self, game_id):
        msg, type = self.__send_message_threadsafe(game_id, T.UPDATE_FIELD)
        if type == T.RESP_OK:
            return ObjectFactory.field_from_json(msg)
        else:
            C.LOG.warning(msg)
            raise LogicException("Could not retreive new field from server: {}".format(msg))

    def request_players(self, game_id):
        msg, type = self.__send_message_threadsafe(game_id, T.REQ_PLAYER_LIST)
        if type == T.RESP_OK:
            return ObjectFactory.players_from_json(msg)
        else:
            C.LOG.warning(msg)
            raise LogicException("Could not retreive players list from server: {}".format(msg))

    def send_new_nr(self, nr, address):
        msg, type = self.__send_message("{}:{}".format(nr, address), T.REQ_CHECK_NR)
        return type

    def __send_message_threadsafe(self, message, type):
        with self.__lock:
            if not self.__connected:
                raise CommunicationException("Server not connected")

            if len(type) > 0:
                try:
                    self.__message_publisher.publish(message_and_type=(message, type))
                    received_message = self.__message_receiver.receive()
                    return received_message
                except soc_error as e:
                    C.LOG.error('Couldn\'t get response from server, error : %s' % str(e))
                except Exception as e:
                    C.LOG.error("Exception on processing response: {}".format(e))
