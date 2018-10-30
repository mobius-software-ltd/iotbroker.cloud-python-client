from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.SimpleConstructor import *
from venv.iot.amqp.tlv.impl.TLVNull import *
from venv.iot.amqp.tlv.impl.TLVMap import *

from venv.iot.classes.NumericUtil import NumericUtil as util

class TLVArray(TLVAmqp):
    def __init__(self, code, values):
        if code is None or values is None:
            self.width = 1
            self.count = 0
            self.size = 0
            self.values = None
            self.constructor = SimpleConstructor(AMQPType.ARRAY_8)
        else:
            self.constructor = SimpleConstructor(code)
            self.values = values
            if isinstance(code, AMQPType):
                if code == AMQPType.ARRAY_8:
                    self.width = 1
                else:
                    self.width = 4
            self.size += self.width
            for tlv in values:
                if isinstance(tlv, TLVAmqp):
                    self.size += tlv.getLength() - tlv.getConstructor().getLength()
                    if self.constructor is None:
                        self.constructor = tlv.getConstructor()
            self.size += self.constructor.getLength()
            self.count = len(values)

    def getElementConstructor(self):
        return self.constructor

    def addElement(self, element):
        if len(self.values) == 0:
            if isinstance(element, TLVAmqp):
                self.constructor = element.getConstructor()
                self.size += self.width
                self.size += self.constructor.getLength()
        if isinstance(self.values, list):
            self.values.append(element)
            self.count += 1
            self.size += element.getLength() + self.constructor.getLength()
        if self.width == 1 and self.size > 255:
            self.constructor.setCode(AMQPType.ARRAY_32)
            self.width = 4
            self.size += 3


    def getBytes(self):
        constructorBytes = self.constructor.getBytes()

        sizeBytes = bytearray(self.width)
        if self.width == 1:
            sizeBytes = util.addByte(sizeBytes, self.size)
        elif self.width != 0 and self.width == 4:
            sizeBytes = util.addInt(sizeBytes, self.size)

        countBytes = bytearray(self.width)
        if self.width == 1:
            countBytes = util.addByte(countBytes, self.count)
        elif self.width != 0 and self.width == 4:
            countBytes = util.addInt(countBytes, self.count)

        elementConstructorBytes = self.constructor.getBytes()
        valueBytes = bytearray(self.size - self.width)
        pos = 0
        for tlv in self.values:
            if isinstance(tlv, TLVAmqp):
                tlvBytes = tlv.getBytes()
                valueBytes[pos:len(tlvBytes)-len(elementConstructorBytes)-1] = tlvBytes[len(elementConstructorBytes)-1:len(tlvBytes)-len(elementConstructorBytes)]
                pos += len(tlvBytes) - len(elementConstructorBytes)-1

        data = bytearray(len(constructorBytes) + len(sizeBytes) + len(countBytes) + len(valueBytes))
        data[0:len(constructorBytes)-1] = constructorBytes[0:len(constructorBytes)-1]
        if self.size > 0:
            data[len(constructorBytes):len(sizeBytes)-1] = sizeBytes[0:len(sizeBytes) - 1]
            data[len(constructorBytes)+len(sizeBytes)-1:len(countBytes) - 1] = countBytes[0:len(countBytes) - 1]
            data[len(constructorBytes) + len(sizeBytes) + len(valueBytes)- 1:len(valueBytes) - 1] = valueBytes[0:len(valueBytes) - 1]

        return data

    def getElements(self):
        return self.values

    def getValue(self):
        return None

    def getLength(self):
        return self.constructor.getLength() + self.width + self.size

    def isNull(self):
        code = self.constructor.getCode()
        if code == AMQPType.NULL:
            return True
        if code == AMQPType.ARRAY_8 or AMQPType.ARRAY_32:
            if len(self.values) == 0:
                return True
        return False

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