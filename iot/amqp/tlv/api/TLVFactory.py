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
from iot.amqp.avps.AMQPType import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.constructor.SimpleConstructor import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.TLVArray import *
from iot.amqp.tlv.impl.TLVList import *
from iot.amqp.tlv.impl.TLVMap import *
from iot.amqp.tlv.impl.TLVFixed import *
from iot.amqp.tlv.impl.TLVVariable import *
from iot.amqp.tlv.impl.TLVNull import *
from iot.classes.NumericUtil import NumericUtil as util

class TLVFactory(object):
    def __init__(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def getTlv(self, buf):
        constructor = self.getConstructor(buf)
        tlv = self.getElement(constructor, buf)
        return tlv

    def getConstructor(self, buf):
        code = None
        constructor = None
        codeByte = util.getByte(buf, self.index)
        self.index += 1
        if codeByte == 0:
            descriptor = self.getTlv(buf)
            code = AMQPType(util.getByte(buf, self.index) & 0xff)
            self.index += 1
            constructor = DescribedConstructor(code, descriptor)
        else:
            code = AMQPType(codeByte & 0xff)
            constructor = SimpleConstructor(code)
        return constructor

    def getElement(self, constructor, buf):
        tlv = None
        code = constructor.getCode()
        if isinstance(code, AMQPType):
            if code == AMQPType.NULL:
                tlv = TLVNull()
            elif code in (AMQPType.BOOLEAN_TRUE,AMQPType.BOOLEAN_FALSE,AMQPType.UINT_0,AMQPType.ULONG_0):
                tlv = TLVFixed(code, bytearray())
            elif code in (AMQPType.BOOLEAN,AMQPType.UBYTE,AMQPType.BYTE,AMQPType.SMALL_UINT,AMQPType.SMALL_INT,AMQPType.SMALL_ULONG,AMQPType.SMALL_LONG):
                value1 = util.getByte(buf,self.index)
                self.index += 1
                tlv = TLVFixed(code, value1)
            elif code in (AMQPType.SHORT,AMQPType.USHORT):
                value2 = buf[self.index:self.index + 2]
                self.index += 2
                tlv = TLVFixed(code, value2)
            elif code in (AMQPType.UINT,AMQPType.INT,AMQPType.FLOAT,AMQPType.DECIMAL_32,AMQPType.CHAR):
                value4 = buf[self.index: self.index+4]
                self.index += 4
                tlv = TLVFixed(code, value4)
            elif code in (AMQPType.ULONG,AMQPType.LONG,AMQPType.DECIMAL_64,AMQPType.DOUBLE,AMQPType.TIMESTAMP):
                value8 = buf[self.index: self.index+8]
                self.index += 8
                tlv = TLVFixed(code, value8)
            elif code in (AMQPType.DECIMAL_128, AMQPType.UUID):
                value16 = buf[self.index: self.index + 16]
                self.index += 16
                tlv = TLVFixed(code, value16)
            elif code in (AMQPType.STRING_8, AMQPType.SYMBOL_8, AMQPType.BINARY_8):
                varlen = util.getByte(buf,self.index) & 0xff
                self.index += 1
                varValue8 = buf[self.index: self.index + int(varlen)]
                self.index += int(varlen)
                tlv = TLVVariable(code, varValue8)
            elif code in (AMQPType.STRING_32, AMQPType.SYMBOL_32, AMQPType.BINARY_32):
                var32len = util.getInt(buf[self.index:self.index+4])
                self.index += 4
                varValue32 = buf[self.index: self.index + int(var32len)]
                self.index += int(var32len)
                tlv = TLVVariable(code, varValue32)
            elif code is AMQPType.LIST_0:
                tlv = TLVList(None, None)
            elif code is AMQPType.LIST_8:
                list8size = util.getByte(buf,self.index) & 0xff
                self.index += 1
                list8count = util.getByte(buf,self.index) & 0xff
                self.index += 1
                list8values = []
                for i in range(0,list8count):
                    entity = self.getTlv(buf)
                    list8values.append(entity)
                tlv = TLVList(code, list8values)
            elif code is AMQPType.LIST_32:
                list32size = util.getInt(buf[self.index:self.index+4])
                self.index += 4
                list32count = util.getInt(buf[self.index:self.index+4])
                self.index += 4
                list32values = []
                for i in range(0, list32count):
                    list32values.append(self.getTlv(buf))
                tlv = TLVList(code, list32values)
            elif code is AMQPType.MAP_8:
                map8size = util.getByte(buf,self.index) & 0xff
                self.index += 1
                map8count = util.getByte(buf,self.index) & 0xff
                self.index += 1
                stop8 = self.index + map8size - 1
                map8 = TLVMap(None,None)
                while self.index < stop8:
                    map8.putElement(self.getTlv(buf), self.getTlv(buf))
                tlv = TLVMap(code, map8)
            elif code is AMQPType.MAP_32:
                map32size = util.getInt(buf[self.index:self.index + 4])
                self.index += 4
                map32count = util.getInt(buf[self.index:self.index + 4])
                self.index += 4
                stop32 = self.index + map32size - 4
                map32 = TLVMap(None, None)
                while self.index < stop32:
                    map32.putElement(self.getTlv(buf), self.getTlv(buf))
                tlv = TLVMap(code, map32)
            elif code is AMQPType.ARRAY_8:
                array8size = util.getByte(buf,self.index) & 0xff
                self.index += 1
                array8count = util.getByte(buf,self.index) & 0xff
                self.index += 1
                arr8 = []
                arr8constructor = self.getConstructor(buf)
                for i in range(0,array8count):
                    arr8.append(self.getElement(arr8constructor,buf))
                tlv = TLVArray(code, arr8)
            elif code is AMQPType.ARRAY_32:
                arr32size = util.getInt(buf[self.index:self.index+4])
                self.index += 4
                arr32count = util.getInt(buf[self.index:self.index+4])
                self.index += 4
                arr32 = []
                arr32constructor = self.getConstructor(buf)
                for i in range(0, arr32count):
                    arr32.append(self.getElement(arr32constructor, buf))
                tlv = TLVArray(code, arr32)

            if isinstance(constructor,DescribedConstructor):
                tlv.setConstructor(constructor)

            return tlv
