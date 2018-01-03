import common.constants as C
import common.message_types as TYPES
from socket import SHUT_WR, SHUT_RD
from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_err

'''
This class is helper class for publishing messages. It checks wether the message to be sent is valid before sending it
to opponent side.
It also formats the message according to protocol {message type}{type delimiter}{message content}{message terminator}
'''


class MessagePublisher():
    def __init__(self, socket):
        self.__socket = socket

    def publish(self, message_and_type):
        message, type = message_and_type

        if type not in TYPES.MSG_TYPES:
            raise Exception("Wrong message type: {}".format(type))

        message = "{}{}{}{}".format(type, C.DELI, message, C.MESSAGE_TERMINATOR)
        self.__socket.send(message)
