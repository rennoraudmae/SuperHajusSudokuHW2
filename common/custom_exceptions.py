class CommunicationException(Exception):
    def __init__(self, message):
        super(CommunicationException, self).__init__(message)


class LogicException(Exception):
    def __init__(self, message):
        super(LogicException, self).__init__(message)
