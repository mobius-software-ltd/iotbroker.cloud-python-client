class MQUnsubscribe(object):
    def __init__(self, packetID,listTopics):
        self.packetID = packetID
        self.listTopics = listTopics

    def getLength(self):
        length = 2
        for name in self.listTopics:
            length += len(name) + 2
        return length

    def getType(self):
        return 10

    def getProtocol(self):
        return 1