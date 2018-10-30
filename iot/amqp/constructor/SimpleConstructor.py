from venv.iot.amqp.avps.AMQPType import *

class SimpleConstructor(object):
    def __init__(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getLength(self):
        return 1

    def getBytes(self):
        if isinstance(self.code, AMQPType):
            return self.code.value
        else:
            return None

    def getDescriptorCode(self):
        return None

