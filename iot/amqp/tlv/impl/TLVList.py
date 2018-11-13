"""
 # Mobius Software LTD
 # Copyright 2015-2018, Mobius Software LTD
 #
 # This is free software; you can redistribute it and/or modify it
 # under the terms of the GNU Lesser General Public License as
 # published by the Free Software Foundation; either version 2.1 of
 # the License, or (at your option) any later version.
 #
 # This software is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 # Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public
 # License along with this software; if not, write to the Free
 # Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 # 02110-1301 USA, or see the FSF site: http://www.fsf.org.
"""
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
            self.size = 0
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
                self.count += 1
                if isinstance(element, TLVAmqp):
                    self.size += element.getLength()
                    self.values.append(element)
            self.update()
        else:
            diff = index - len(self.values)
            while diff >= 0:
                self.addElement(None, element=TLVNull())
                diff -= 1
            self.setElement(index, element)

    def setElement(self, index, element):
        if index < len(self.values):
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

                    if isinstance(tlvBytes,int):
                        valueBytes = util.addByte(valueBytes,tlvBytes)
                        pos += 1
                    else:
                        valueBytes += tlvBytes
                        pos += len(tlvBytes)

        data = bytearray()
        data += constructorBytes
        if self.size > 0:
            data += sizeBytes
            data += countBytes
            data += valueBytes
        return data

    def getList(self):
        return self.values

    def getValue(self):
        return None

    def getLength(self):
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
