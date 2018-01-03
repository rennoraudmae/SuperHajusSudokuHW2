import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
LOG = logging.getLogger()

TCP_RECEIVE_BUFFER_SIZE = 1024 * 1024
MAX_PDU_SIZE = 200 * 1024 * 1024
DEFAULT_SERVER_PORT = 7777
DEFAULT_SERVER_HOST = '127.0.0.1'
DELI = ":"
MESSAGE_TERMINATOR = "///END"
MAX_FOLDER_CAPACITY = 1024 * 1024

#constatns to draw gamefield
CELL_SIDE = 60
PADDING = 20
FIELD_SIDE = 2 * PADDING + 9 * CELL_SIDE
