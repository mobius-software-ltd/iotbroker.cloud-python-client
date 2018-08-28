from venv.IoT.Classes.Topic import *
from venv.IoT.Classes.QoS import *

class MQTopic(Topic):
    def __init__(self, name, qos):
        self.name = name
        self.qos = QoS(qos)

    def getType(self):
        return 'SN_UNKNOWN_TOPIC_TYPE'

    def getQoS(self):
        return self.qos

    def encode(self):
        return self.name

    def getLength(self):
        return len(self.name)

    def getName(self):
        return self.name