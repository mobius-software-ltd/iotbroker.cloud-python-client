class QoS(object):
    def __init__(self, value):
        self.qosValue = value

    def setValue(self,value):
        self.qosValue = value

    def getValue(self):
        return self.qosValue