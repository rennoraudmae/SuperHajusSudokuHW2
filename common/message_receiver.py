import common.constants as C
import common.message_types as T
from socket import SHUT_WR, SHUT_RD, error
import time
import re

'''
This class does low-level message receiving. It gathers data from opponent-side by blocks and concatenates these.
After that, it checks wether the message is valid (minimum length).
Finally, it gives the message for processor and receives the result.
'''


class MessageReceiver():
    def __init__(self, socket, processor):
        self.__socket = socket
        self.__message = ""
        self.__processor = processor
        self.__running = True

    def receive(self):
        terminate = False
        while self.__running:
            try:
                block = self.__socket.recv(C.TCP_RECEIVE_BUFFER_SIZE)
            except error, (value, message):
                # No data available
                time.sleep(0.2)
                continue

            if len(block) <= 0:
                # No data available
                time.sleep(0.2)
                continue

            if block.endswith(C.MESSAGE_TERMINATOR):
                block = block[:-len(C.MESSAGE_TERMINATOR)]
                terminate = True

            if (len(self.__message) + len(block)) >= C.MAX_PDU_SIZE:
                self.__socket.shutdown(SHUT_RD)
                del self.__message
                raise Exception("Remote end-point tried to exceed the MAX_PDU_SIZE ({})".format(C.MAX_PDU_SIZE))

            self.__message += block

            if terminate:
                break

        msg_copy = self.__get_message()

        if len(msg_copy) < 3:
            return "No message received", T.RESP_VOID

        return self.__processor.process_message(msg_copy)

    def __get_message(self):
        msg_copy = self.__message
        self.__message = ""
        return msg_copy

    def stop(self):
        self.__running = False
