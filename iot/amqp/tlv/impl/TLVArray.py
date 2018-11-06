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
            self.elementConstructor = None
            self.constructor = SimpleConstructor(AMQPType.ARRAY_8)
        else:
            self.constructor = SimpleConstructor(code)
            self.values = values
            self.size = 0
            self.elementConstructor = None
            if isinstance(code, AMQPType):
                if code == AMQPType.ARRAY_8:
                    self.width = 1
                else:
                    self.width = 4
            self.size += self.width
            for tlv in values:
                if isinstance(tlv, TLVAmqp):
                    self.size += tlv.getLength() - tlv.getConstructor().getLength()
                    if self.elementConstructor is None and tlv is not None:
                        self.elementConstructor = tlv.getConstructor()
            self.size += self.elementConstructor.getLength()
            self.count = len(values)

    def getElementConstructor(self):
        return self.elementConstructor

    def getElemetsCode(self):
        return self.elementConstructor.getCode()

    def addElement(self, element):
        if self.values is not None and len(self.values) == 0:
            if isinstance(element, TLVAmqp):
                self.elementConstructor = element.getConstructor()
                self.size += self.width
                self.size += self.elementConstructor.getLength()
        if isinstance(self.values, list):
            self.values.append(element)
            self.count += 1
            self.size += element.getLength() - self.elementConstructor.getLength()
        if self.width == 1 and self.size > 255:
            self.constructor.setCode(AMQPType.ARRAY_32)
            self.width = 4
            self.size += 3

    def getBytes(self):
        constructorBytes = self.constructor.getBytes()
        #print('Array constructorBytes= ' + str(constructorBytes) + ' count=' + str(self.count) + ' size=' + str(self.size) + ' width=' + str(self.width))

        sizeBytes = bytearray()
        if self.width == 1:
            sizeBytes = util.addByte(sizeBytes, self.size)
        elif self.width == 4:
            sizeBytes = util.addInt(sizeBytes, self.size)
        #print('sizeBytes ' + str(sizeBytes))

        countBytes = bytearray()
        if self.width == 1:
            countBytes = util.addByte(countBytes, self.count)
        elif self.width != 0 and self.width == 4:
            countBytes = util.addInt(countBytes, self.count)
        #print('countBytes ' + str(countBytes))

        elementConstructorBytes = self.elementConstructor.getBytes()
        #print(str(self.size) + '' + str(self.width))
        valueBytes = bytearray()
        pos = 0
        for tlv in self.values:
            if isinstance(tlv, TLVAmqp):
                tlvBytes = tlv.getBytes()
                #print('elementConstructorBytes ' + str(elementConstructorBytes) + ' tlvBytes= ' + str(tlvBytes))
                valueBytes += tlvBytes[1:len(tlvBytes)]
                pos += len(tlvBytes) - len(str(elementConstructorBytes))-1
        #print('valueBytes= ' + str(valueBytes))
        data = bytearray()
        data.append(constructorBytes)
        #print('Constructor data= ' + str(data))
        if self.size > 0:
            data += sizeBytes
            data += countBytes
            data = util.addByte(data,elementConstructorBytes)
            data += valueBytes

        #print('TLVArray.getBytes ' + str(data))
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
        return self.constructor.getCode()

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        pass

    def setCode(self, arg):
        pass

    def setConstructor(self, arg):
        #self.constructor = arg
        pass