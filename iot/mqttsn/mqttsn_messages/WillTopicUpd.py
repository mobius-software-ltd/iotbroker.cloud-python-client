from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *
from venv.iot.mqttsn.mqttsn_classes.FullTopic import *

class WillTopicUpd(object):
    def __init__(self, retain, topic):
        self.retain = retain
        self.topic = topic

    def getLength(self):
        length = 2
        if self.topic is not None:
            length += self.topic.getLength() + 1
            if self.topic.getLength() > 252:
                length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_WILL_TOPIC_UPD.value[0]

    def isRetain(self):
        return self.retain

    def setRetain(self, retain):
        self.retain = retain

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic