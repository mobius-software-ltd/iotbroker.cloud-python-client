from venv.iot.classes.Topic import *
from venv.iot.classes.QoS import *

class CoapTopic(Topic):
    def __init__(self, name, qos):
        self.name = name
        self.qos = QoS(qos)

    def getType(self):
        return 'COAP_TOPIC_TYPE'

    def getQoS(self):
        return self.qos

    def encode(self):
        return self.name

    def getLength(self):
        return len(self.name)

    def getName(self):
        return self.name