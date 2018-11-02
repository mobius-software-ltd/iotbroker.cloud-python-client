import abc

class AMQPSection(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def fill(self, list):
        pass

    @abc.abstractmethod
    def getValue(self):
        pass

    @abc.abstractmethod
    def getCode(self):
        pass