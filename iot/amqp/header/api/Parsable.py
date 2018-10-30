import abc

class Parsable(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def toArgumentsList(self):
        pass

    @abc.abstractmethod
    def fromArgumentsList(self, arg):
        pass