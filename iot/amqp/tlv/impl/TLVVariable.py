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
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.avps.AMQPType import *
from iot.amqp.constructor.SimpleConstructor import *
from iot.amqp.constructor.DescribedConstructor import *

from iot.classes.NumericUtil import NumericUtil as util

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
        widthBytes = bytearray()
        if self.width == 1:
            widthBytes.append(len(self.value))
        elif self.width == 4:
            widthBytes = util.addInt(widthBytes, len(self.value))

        data = bytearray()
        if isinstance(self.constructor, DescribedConstructor):
            data += constructorBytes
        else:
            data.append(constructorBytes)

        data += widthBytes
        if len(self.value) > 0:
            data += self.value
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

    def setConstructor(self, constructor):
        self.constructor = constructor