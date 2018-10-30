from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.SimpleConstructor import *

from venv.iot.classes.NumericUtil import NumericUtil as util

class TLVVariable(TLVAmqp):
    def __init__(self, code, value):
        self.value = value
        if len(value) > 255:
            self.width = 4
        else:
            self.width = 1
        self.constructor = SimpleConstructor(code)

    def getBytes(self):
        constructorBytes = self.constructor.getBytes()
        widthBytes = bytearray(self.width)
        if self.width == 1:
            widthBytes[0] = len(self.value)
        elif self.width == 4:
            widthBytes = util.addInt(widthBytes, len(self.value))

        data = bytearray(len(constructorBytes)+len(self.width)+len(self.value))

        data[0,len(constructorBytes)-1] = constructorBytes[0:len(constructorBytes)-1]
        data[len(constructorBytes):len(constructorBytes)+len(self.width)-1] = widthBytes[0:len(widthBytes) - 1]
        if len(self.value) > 0:
            data[len(constructorBytes)+len(self.width):len(constructorBytes)+len(self.value)+len(self.width)-1] = self.value[0:len(self.value)-1]
        return data

    def getLength(self):
        return len(self.value) + len(self.constructor.getLength())

    def getValue(self):
        return self.value

    def getCode(self, arg):
        pass

    def getConstructor(self, arg):
        pass

    def isNull(self):
        pass

    def setCode(self, arg):
        pass

    def setConstructor(self, arg):
        pass