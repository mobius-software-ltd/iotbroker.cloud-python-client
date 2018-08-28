import abc

class IoTClient(metaclass=abc.ABCMeta):

    def __init__(self):
        self._subject = None
        self._client_state = None

    @abc.abstractmethod
    def dataReceived(self, arg):
        pass

    @abc.abstractmethod
    def send(self, arg):
        pass

    @abc.abstractmethod
    def goConnect(self):
        pass

    @abc.abstractmethod
    def publish(self, arg):
        pass

    @abc.abstractmethod
    def subscribeTo(self, arg):
        pass

    @abc.abstractmethod
    def unsubscribeFrom(self, arg):
        pass

    @abc.abstractmethod
    def pingreq(self):
        pass

    @abc.abstractmethod
    def disconnectWith(self, arg):
        pass

    @abc.abstractmethod
    def timeoutMethod(self):
        pass
