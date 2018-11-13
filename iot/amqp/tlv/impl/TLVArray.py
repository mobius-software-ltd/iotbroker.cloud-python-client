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

        sizeBytes = bytearray()
        if self.width == 1:
            sizeBytes = util.addByte(sizeBytes, self.size)
        elif self.width == 4:
            sizeBytes = util.addInt(sizeBytes, self.size)

        countBytes = bytearray()
        if self.width == 1:
            countBytes = util.addByte(countBytes, self.count)
        elif self.width != 0 and self.width == 4:
            countBytes = util.addInt(countBytes, self.count)

        elementConstructorBytes = self.elementConstructor.getBytes()
        valueBytes = bytearray()
        pos = 0
        for tlv in self.values:
            if isinstance(tlv, TLVAmqp):
                tlvBytes = tlv.getBytes()
                valueBytes += tlvBytes[1:len(tlvBytes)]
                pos += len(tlvBytes) - len(str(elementConstructorBytes))-1
        data = bytearray()
        data.append(constructorBytes)
        if self.size > 0:
            data += sizeBytes
            data += countBytes
            data = util.addByte(data,elementConstructorBytes)
            data += valueBytes
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

    def setConstructor(self, constructor):
        self.constructor = constructor