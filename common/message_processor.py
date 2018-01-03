import common.constants as C
import common.message_types as T
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

'''
This is general class for message processing. Both, client and server side extends the class by implementing more specific
functions.
The functions are executed by the name of function dynamically. These names are defined in global file (message_types)
'''


class MessageProcessor():
    def __init__(self):
        self._type = None

    def void(self):
        return "VOID", T.RESP_VOID

    def success(self):
        return "OK", T.RESP_OK

    def error(self, msg="ERROR"):
        return msg, T.RESP_ERR

    def simple_message(self, message):
        return message, T.RESP_OK
