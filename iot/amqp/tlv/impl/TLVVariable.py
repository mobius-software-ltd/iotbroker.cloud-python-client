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
        #print('Varialble constructorBytes= ' + str(constructorBytes))

        widthBytes = bytearray()
        if self.width == 1:
            widthBytes.append(len(self.value))
        elif self.width == 4:
            widthBytes = util.addInt(widthBytes, len(self.value))

        data = bytearray()
        data.append(constructorBytes)
        data += widthBytes
        if len(self.value) > 0:
            data += self.value
        #print('TLVVariable.getBytes ' + str(data) + ' length= ' + str(self.getLength()))
        return data

    def getLength(self):
        return len(self.value) + self.constructor.getLength() + self.width

    def getValue(self):
        return self.value

    def getCode(self):
        return self.constructor.getCode()

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        pass

    def setCode(self, arg):
        pass

    def setConstructor(self, arg):
        pass