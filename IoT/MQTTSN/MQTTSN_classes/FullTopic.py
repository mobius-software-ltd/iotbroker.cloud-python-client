from venv.IoT.Classes.Topic import *
from venv.IoT.Classes.QoS import *
from venv.IoT.MQTTSN.MQTTSN_classes.TopicType import *

class FullTopic(Topic):
    def __init__(self, value, qos):
        self.value = value
        self.qos = QoS(qos)

    def getType(self):
        return TopicType.NAMED

    def getLength(self):
        return len(self.value)

    def getQoS(self):
        return self.qos

    def setQoS(self, qos):
        self.qos = QoS(qos)

    def encode(self):
        return self.value

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value