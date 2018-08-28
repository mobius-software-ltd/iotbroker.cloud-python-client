class MQPublish(object):
    def __init__(self,packetID,topic,content,retain,dup):
        self.packetID = packetID
        self.topic = topic
        self.content = content
        self.retain = retain
        self.dup = dup

    def getLength(self):
        length = 0

        if self.packetID > 0:
            length += 2

        if self.topic is not None:
            length += self.topic.getLength() + 2

        length += len(self.content)

        return length

    def getType(self):
        return 3

    def getProtocol(self):
        return 1