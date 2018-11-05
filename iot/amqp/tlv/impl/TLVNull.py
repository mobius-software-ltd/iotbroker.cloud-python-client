from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.SimpleConstructor import *

class TLVNull(TLVAmqp):
    def __init__(self):
        self.constructor = SimpleConstructor(AMQPType.NULL)

    def getBytes(self):
        return self.constructor.getBytes()

    def getLength(self):
        return 1

    def getValue(self):
        return None

    def toString(self):
        return 'NULL'

    def getCode(self):
        pass

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        return True

    def setCode(self, arg):
        pass

    def setConstructor(self, arg):
        pass