class MQSubscribe(object):
    #listTopics - list of MQTopics from MQTTclasses
    def __init__(self,packetID,listMQTopics):
        self.packetID = packetID
        self.listMQTopics = listMQTopics

    def getLength(self):
        length = 0
        if self.packetID is not None:
            length = length + 2

        for item in self.listMQTopics:
            length += len(item.name) + 3

        return length

    def getType(self):
        return 8

    def getProtocol(self):
        return 1

    def isValidCode(self, code):
        if code == 0 | code == 1 | code == 2:
            return True
        return False
    