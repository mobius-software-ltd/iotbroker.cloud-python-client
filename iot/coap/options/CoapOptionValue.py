import abc

class CoapOptionValue(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, type, length, value):
        self.type = type
        self.length = length
        self.value = value

    @abc.abstractmethod
    def getType(self):
        return self.type

    @abc.abstractmethod
    def getLength(self):
        return self.length

    @abc.abstractmethod
    def getValue(self):
        return self.value