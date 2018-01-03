import common.constants as C
import common.message_types as T

'''
This is general class for message processing. Both, client and server side extends the class by implementing more specific
functions.
The functions are executed by the name of function dynamically. These names are defined in global file (message_types)
'''


class MessageProcessor():
    def __init__(self):
        self._type = None
        self._message = None

    def __init_message(self, raw_message):
        self._type, self._message = raw_message.split(C.DELI, 1)

    def process_message(self, raw_message):
        def not_implemented():
            C.LOG.warning("This type is not implemented: {}".format(self._type))
            return self.void()

        self.__init_message(raw_message)
        function_name = T.MSG_TYPES[self._type]
        func = getattr(self, function_name, not_implemented)
        print "processing {}".format(function_name)
        return func()

    def void(self):
        return "VOID", T.RESP_VOID

    def success(self):
        if self._message is None:
            self._message = "OK"
        return self._message, T.RESP_OK

    def error(self):
        return self._message, T.RESP_ERR

    def simple_message(self):
        return self._message, T.RESP_OK
