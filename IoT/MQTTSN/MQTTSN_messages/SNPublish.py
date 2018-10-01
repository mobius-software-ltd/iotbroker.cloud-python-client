from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNPublish(object):
    def __init__(self, messageID, topic, content, dup, retain):
        self.messageID = messageID
        self.topic = topic
        self.content = content
        self.dup = dup
        self.retain = retain

    def getLength(self):
        length = 7
        if self.content is not None and len(self.content) > 0:
            length += len(self.content)
        if len(self.content) > 248:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_PUBLISH.value[0]

    def getMessageID(self):
        return self.messageID

    def setMessageID(self, messageID):
        self.messageID = messageID

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def isDup(self):
        return self.dup

    def setDup(self, dup):
        self.dup = dup

    def isRetain(self):
        return self.retain

    def setRetain(self, retain):
        self.retain = retain