from httplib import ResponseNotReady, CannotSendRequest

import common.constants as C
from common.custom_exceptions import CommunicationException, LogicException
from common.object_factory import ObjectFactory
import common.message_types as T
import threading
from xmlrpclib import ServerProxy


'''
This is main class for TCP client. It establishes a connection with server.
It also initializes sending different commands to server and receives responses from server.
'''


class RpcClient():
    def __init__(self, host=C.DEFAULT_SERVER_HOST, port=C.DEFAULT_SERVER_PORT):
        self.__host = host
        self.__port = port
        self.__proxy = None
        self.__connected = False
        self.__running = True
        self.__game_field = []
        self.__lock = threading.Lock()
        self.__server_name = None
        self.start_client()

    def start_client(self):
        try:
            self.__proxy = ServerProxy("http://{}:{}".format(self.__host, self.__port))
            self.__connected = True
        except Exception as e:
            C.LOG.error('Can\'t connect to server, error : %s' % str(e))
            return

        C.LOG.info("Connected to server!")

        methods = filter(lambda x: 'system.' not in x, self.__proxy.system.listMethods())
        C.LOG.debug("Remote methods are: {}".format(methods))

    def is_connected(self):
        return self.__connected

    def update_field(self, field):
        self.__game_field = field

    def request_game_state(self, game_id):
        msg, type = self.__call_proxy("game_state", game_id)
        if type == T.RESP_OK:
            C.LOG.info("Game still running")
            return False
        else:
            return msg

    def send_message(self, message):
        msg, type = self.__call_proxy("simple_message", message)
        if type == T.RESP_OK:
            C.LOG.info("Got answer to simple message: {}".format(msg))
        else:
            C.LOG.warning(msg)

    def new_game_request(self, game_name, max_players):
        msg, type = self.__call_proxy("new_game", "{}:{}".format(game_name, max_players))
        if type == T.RESP_OK:
            C.LOG.info("New game created with id: {}".format(msg))
            return msg
        else:
            C.LOG.warning(msg)
            raise LogicException("New game creation failed with message: {}".format(msg))

    def join_game(self, game_id, username):
        msg, type = self.__call_proxy("join_game", "{}:{}".format(game_id, username))
        if type == T.RESP_OK:
            C.LOG.info("Joined game with id: {}".format(game_id))
        else:
            C.LOG.warning(msg)
            raise LogicException("New game creation failed with message: {}".format(msg))

    def leave_game(self, game_id, username):
        msg, type = self.__call_proxy("leave_game", "{}:{}".format(game_id, username))
        if type == T.RESP_OK:
            C.LOG.info("Left game with id: {}".format(game_id))
        else:
            C.LOG.warning(msg)
            raise LogicException("Leaving game failed with: {}".format(msg))

    def get_all_games(self):
        msg, type = self.__call_proxy("get_all_games")
        if type == T.RESP_OK:
            return msg
        else:
            C.LOG.warning(msg)
            raise LogicException("Game requesting failed with error: {}".format(msg))

    def check_nr(self, nr, address, username, game_id):
        msg, type = self.__call_proxy("check_nr", "{}:{}:{}:{}".format(nr, address, game_id, username))
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
        try:
            msg, type = self.__call_proxy("get_game_field", game_id)
            if type == T.RESP_OK:
                return ObjectFactory.field_from_json(msg)
            else:
                C.LOG.warning(msg)
                return self.__game_field
        except ResponseNotReady as e:
            return self.__game_field

    def request_players(self, game_id):
        msg, type = self.__call_proxy("player_list", game_id)
        if type == T.RESP_OK:
            return ObjectFactory.players_from_json(msg)
        else:
            C.LOG.warning(msg)
            raise LogicException("Could not retreive players list from server: {}".format(msg))

    def __call_proxy(self, func_name, args=None):
        try:
            func = getattr(self.__proxy, func_name)
            if args is not None:
                return func(args)
            else:
                return func()
        except AttributeError:
            C.LOG.error("{} not found".format(func_name))
            return " ", T.RESP_ERR
        except ResponseNotReady as e:
            return e, T.RESP_ERR
        except CannotSendRequest as e:
            return e, T.RESP_ERR
