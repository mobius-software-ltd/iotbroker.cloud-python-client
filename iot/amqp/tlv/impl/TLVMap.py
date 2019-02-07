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
from iot.amqp.tlv.impl.TLVNull import *
from iot.classes.NumericUtil import NumericUtil as util

class TLVMap(TLVAmqp):
    def __init__(self, code, map):
        if code is None or map is None:
            self.width = 1
            self.count = 0
            self.size = 1
            self.map = None
            self.constructor = SimpleConstructor(AMQPType.MAP_8)
        else:
            self.map = map
            if isinstance(code, AMQPType):
                if code == AMQPType.MAP_8:
                    self.width = 1
                else:
                    self.width = 4
            self.size += self.width

            if isinstance(map, dict):
                for key, value in map.items():
                    if isinstance(key, TLVAmqp) and isinstance(value, TLVAmqp):
                        self.size += key.getLength()
                        self.size += value.getLength()

            self.count = len(self.map)
            self.constructor = SimpleConstructor(code)

    def update(self):
        if self.width == 1 and self.size > 255:
            self.constructor.setCode(AMQPType.MAP_32)
            self.width = 4
            self.size += 3

    def putElement(self, key, value):
        if isinstance(self.map, dict):
            self.map[key] = value
        if isinstance(key, TLVAmqp) and isinstance(value, TLVAmqp):
            self.size += key.getLength() + value.getLength()
        self.count += 1
        self.update()

    def getBytes(self):
        constructorBytes = self.constructor.getBytes()

        sizeBytes = bytearray()
        if self.width == 1:
            sizeBytes = util.addByte(sizeBytes, self.size)
        else:
            sizeBytes = util.addInt(sizeBytes, self.size)

        countBytes = bytearray()
        if self.width == 1:
            countBytes = util.addByte(countBytes, self.count*2)
        else:
            countBytes = util.addInt(countBytes, self.count*2)

        valueBytes = bytearray()
        pos = 0
        if isinstance(self.map, dict):
            for key, value in self.map.items():
                if isinstance(key, TLVAmqp) and isinstance(value, TLVAmqp):
                    keyBytes = key.getBytes()
                    valBytes = value.getBytes()
                    valueBytes.append(keyBytes)
                    pos += len(keyBytes)
                    valueBytes.append(valBytes)
                    pos += len(valBytes)

        data = bytearray()
        data.append(constructorBytes)
        if self.size > 0:
            data += sizeBytes
            data += countBytes
            data += valueBytes
        return data

    def getMap(self):
        return self.map

    def getValue(self):
        return None

    def getLength(self):
        return self.constructor.getLength() + self.width + self.size

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