import abc

class UIClient():

    def __init__(self):
        self._subject = None
        self._client_state = None

    @abc.abstractmethod
    def dataReceived(self, arg):
        pass