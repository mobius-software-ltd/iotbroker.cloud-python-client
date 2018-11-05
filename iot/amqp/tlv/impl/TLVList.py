from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.SimpleConstructor import *
from venv.iot.amqp.tlv.impl.TLVNull import *
from venv.iot.amqp.tlv.impl.TLVMap import *
from venv.iot.amqp.tlv.impl.TLVArray import *

from venv.iot.classes.NumericUtil import NumericUtil as util

class TLVList(TLVAmqp):
    def __init__(self, code, values):
        if code is None or values is None:
            self.width = 0
            self.count = 0
            self.size = 0
            self.values = []
            self.constructor = SimpleConstructor(AMQPType.LIST_0)
        else:
            self.values = values
            if isinstance(code, AMQPType):
                if code == AMQPType.LIST_8:
                    self.width = 1
                else:
                    self.width = 4
            self.size += self.width
            for tlv in values:
                if isinstance(tlv, TLVAmqp):
                    self.size += tlv.getLength()
            self.count = len(values)
            self.constructor = SimpleConstructor(code)

    def update(self):
        if self.width == 1 and self.size > 255:
            self.constructor.setCode(AMQPType.LIST_32)
            self.width = 4
            self.size += 3

    def addElement(self, index, element):
        if index is None or index == 0:
            if self.size == 0:
                self.constructor.setCode(AMQPType.LIST_8)
                self.width = 1
                self.size += 1
            if isinstance(self.values, list):
                self.values.append(element)
                self.count += 1
            #print('self.values ' + str(self.values) + ' ' + str(self.count))
            if isinstance(element, TLVAmqp):
                self.size += element.getLength()
            self.update()
        else:
            diff = index - len(self.values)
            while diff > 0:
                self.addElement(element=TLVNull())
                diff -= 1
            self.setElement(index, element)

    def setElement(self, index, element):
        self.size -= self.values[index].getLength()
        self.values[index] = element
        self.size += element.getLength()
        self.update()

    def addToList(self, index, elemIndex, element):
        if self.count < index:
            self.addElement(index, element = TLVList(None,None))
        list = self.values[index]
        if list is None:
            self.setElement(index, element = TLVList(None,None))
        values = self.values[index]
        if isinstance(values, TLVList):
            values.addElement(elemIndex, element)
            self.size += element.getLength()
        self.update()

    def addToMap(self, index, key, value):
        if self.count < index:
            self.addElement(index, element = TLVMap(None,None))
        map = self.values[index]
        if map is None:
            self.setElement(index, element = TLVMap(None,None))
        values = self.values[index]
        if isinstance(values, TLVMap):
            values.putElement(key, value)
            self.size += key.getLength() + value.getLength()
        self.update()

    def addToArray(self, index, element):
        if self.count < index:
            self.addElement(index, element = TLVArray(None,None))
        array = self.values[index]
        if array is None:
            self.setElement(index, element = TLVArray(None,None))
        values = self.values[index]
        if isinstance(values, TLVMap):
            values.addElement(element)
            self.size += element.getLength()
        self.update()

    def getBytes(self):
        constructorBytes = self.constructor.getBytes()

        sizeBytes = bytearray()
        if self.width == 1:
            sizeBytes = util.addByte(sizeBytes, self.size)
        elif self.width != 0:
            sizeBytes = util.addInt(sizeBytes, self.size)

        countBytes = bytearray()
        if self.width == 1:
            countBytes = util.addByte(countBytes, self.count)
        elif self.width != 0:
            countBytes = util.addInt(countBytes, self.count)

        valueBytes = bytearray()
        pos = 0
        if self.values is not None:
            for tlv in self.values:
                if isinstance(tlv, TLVAmqp):
                    tlvBytes = tlv.getBytes()
                    valueBytes[pos:len(tlvBytes)-1] = tlvBytes[0:len(tlvBytes)]
                    pos += len(tlvBytes)

        data = bytearray()
        #print(str(constructorBytes[0]))
        data.append(constructorBytes[0])
        if self.size > 0:
            data += sizeBytes
            data += countBytes
            data += valueBytes

        print('TLVList getBytes ' + str(data))
        return data

    def getList(self):
        return self.values

    def getValue(self):
        return None

    def getLength(self):
        #print('getLength ' + str(self.constructor.getLength()) + ' ' + str(self.width) + ' ' + str(self.size))
        return self.constructor.getLength() + self.width + self.size

    def getCode(self):
        return self.getConstructor().getCode()

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        pass

    def setCode(self):
        pass

    def setConstructor(self, constructor):
        self.constructor = constructor
