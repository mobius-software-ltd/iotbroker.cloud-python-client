class MQUnsuback(object):
    def __init__(self, packetID):
        self.packetID = packetID

    def getLength(self):
        return 2

    def getType(self):
        return 11

    def getProtocol(self):
        return 1