import abc

class Topic(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getType(self):
        return

    @abc.abstractmethod
    def getQoS(self):
        return

    @abc.abstractmethod
    def encode(self):
        return

    @abc.abstractmethod
    def getLength(self):
        return