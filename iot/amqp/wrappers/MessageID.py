import abc

class MessageID(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def getString(self):
        pass

    @abc.abstractmethod
    def getBinary(self):
        pass

    @abc.abstractmethod
    def getLong(self):
        pass

    @abc.abstractmethod
    def getUuid(self):
        pass