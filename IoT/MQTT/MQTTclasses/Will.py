class Will(object):
    def __init__(self, topic, content, retain):
        self.topic = topic
        self.content = content
        self.retain = retain

    def getLength(self):
        totalLength=0;
        if self.topic.getLength()>0:
            totalLength+=self.topic.getLength() + 2

        if len(self.content) > 0:
            totalLength += len(self.content) + 2

        return totalLength

    def valid(self):
        if (self.topic is not None) & (self.topic.getLength() > 0) & (self.content is not None) & (self.topic.getQoS() is not None):
            return True
        return False

    def getTopic(self):
        return self.topic

    def getRetain(self):
        return self.retain