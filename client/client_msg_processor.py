from common.message_processor import MessageProcessor
import common.constants as C
import common.message_types as T
from common.object_factory import ObjectFactory

'''
This is client side message processor implementation, which processes only client specific messages and operations.
'''


class ClientMsgProcessor(object, MessageProcessor):
    def __init__(self, client):
        super(ClientMsgProcessor, self).__init__()
        self.client = client

    def ping(self):
        return self.success()

    def get_game_field(self):
        field_json = self._message
        field = ObjectFactory.field_from_json(field_json)
        self.client.update_field(field)

        return self.success()
    def rejected(self):
        return " ", T.RESP_NOK