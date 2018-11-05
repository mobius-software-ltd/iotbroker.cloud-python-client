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
            self.values = []
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
        if self.values is not None and len(self.values) == 0:
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

        sizeBytes = bytearray()
        if self.width == 1:
            sizeBytes = util.addByte(sizeBytes, self.size)
        elif self.width != 0 and self.width == 4:
            sizeBytes = util.addInt(sizeBytes, self.size)

        countBytes = bytearray()
        if self.width == 1:
            countBytes = util.addByte(countBytes, self.count)
        elif self.width != 0 and self.width == 4:
            countBytes = util.addInt(countBytes, self.count)

        elementConstructorBytes = self.constructor.getBytes()
        #print(str(self.size) + '' + str(self.width))
        valueBytes = bytearray()
        pos = 0
        for tlv in self.values:
            if isinstance(tlv, TLVAmqp):
                tlvBytes = tlv.getBytes()
                valueBytes += tlvBytes[len(str(elementConstructorBytes)) - 1:len(tlvBytes)]
                pos += len(tlvBytes) - len(str(elementConstructorBytes))-1

        data = bytearray()
        data.append(constructorBytes)
        if self.size > 0:
            data += sizeBytes
            data += countBytes
            data += valueBytes

        print('TLVArray.getBytes ' + str(data))
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

    def getCode(self):
        pass

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        pass

    def setCode(self, arg):
        pass

    def setConstructor(self, arg):
        self.constructor = arg