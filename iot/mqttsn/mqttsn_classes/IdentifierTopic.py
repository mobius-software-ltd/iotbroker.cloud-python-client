from venv.iot.classes.Topic import *
from venv.iot.mqttsn.mqttsn_classes.TopicType import *

class IdentifierTopic(Topic):
    def __init__(self, value, qos):
        self.value = value
        self.qos = qos

    def getType(self):
        return TopicType.ID

    def getLength(self):
        return 2

    def getQoS(self):
        return self.qos

    def setQoS(self, qos):
        self.qos = qos

    def encode(self):
        return self.value

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value