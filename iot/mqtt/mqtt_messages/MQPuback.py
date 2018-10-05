class MQPuback(object):
    def __init__(self, packetID):
        self.packetID = packetID

    def getLength(self):
        return 2

    def getType(self):
        return 4

    def getProtocol(self):
        return 1