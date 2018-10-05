import abc

class ProtocolMessage(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getProtocol(self):
        return

    @abc.abstractmethod
    def getLength(self):
        return

    @abc.abstractmethod
    def getType(self):
        return

    @abc.abstractmethod
    def getPacketID(self):
        return

    @abc.abstractmethod
    def setPacketID(self, packetID):
        return

    @abc.abstractmethod
    def processBy(self, MQDevice):
        return