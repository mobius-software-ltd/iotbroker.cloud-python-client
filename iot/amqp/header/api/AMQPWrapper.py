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
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.TLVArray import *
from iot.amqp.tlv.impl.TLVList import *
from iot.amqp.tlv.impl.TLVMap import *
from iot.amqp.tlv.impl.TLVFixed import *
from iot.amqp.tlv.impl.TLVVariable import *
from iot.amqp.wrappers.AMQPDecimal import *
from iot.amqp.wrappers.AMQPSymbol import *
from iot.classes.NumericUtil import NumericUtil as util
import uuid
import numpy as np

class AMQPWrapper(object):
    def __init__(self):
        pass

    def wrap(self, obj):
        result = None
        if obj is None:
            return TLVNull()

        if isinstance(obj, np.int8):
            result = self.wrapByte(obj)
        elif isinstance(obj, np.int16):
            if obj >= 0:
                result = self.wrapUByte(obj)
            else:
                result = self.wrapShort(obj)
        elif isinstance(obj, np.int32):
            if obj > 0:
                result = self.wrapUShort(obj)
            else:
                result = self.wrapInt(obj)
        elif isinstance(obj, np.int64):
            if obj >= 0:
                result = self.wrapUInt(obj)
            else:
                result = self.wrapLong(obj)
        elif isinstance(obj, np.complex128):
            result = self.wrapULong(obj)
        elif isinstance(obj, str):
            result = self.wrapString(obj)
        elif isinstance(obj, AMQPSymbol):
            result = self.wrapSymbol(obj)
        elif isinstance(obj, bytearray) or isinstance(obj, bytes):
            result = self.wrapBinary(obj)
        elif isinstance(obj, bool):
            result = self.wrapBool(obj)
        elif isinstance(obj, np.chararray) :
            result = self.wrapChar(obj)
        elif isinstance(obj, np.float64):
            result = self.wrapDouble(obj)
        elif isinstance(obj, np.float32):
            result = self.wrapFloat(obj)
        elif isinstance(obj, uuid.UUID):
            result = self.wrapUuid(obj)
        elif isinstance(obj, np.datetime64):
            result = self.wrapTimestamp(obj)
        elif isinstance(obj, AMQPDecimal):
            val = obj.getValue()
            if len(val) == 4:
                result = self.wrapDecimal32(obj)
            elif len(val) == 8:
                result = self.wrapDecimal64(obj)
            elif len(val) == 16:
                result = self.wrapDecimal128(obj)
        else:
            raise ValueError('Wrapper received unrecognized type ' + str(obj))

        return result

    def wrapBool(self, bool):
        value = bytearray()
        if bool:
            code = AMQPType.BOOLEAN_TRUE
        else:
            code = AMQPType.BOOLEAN_FALSE
        return TLVFixed(code, value)

    def wrapUByte(self, bt):
        if bt < 0:
            raise ValueError('Error negative value of ' + str(bt) + ' cannot be assigned to UBYTE type')
        return TLVFixed(AMQPType.UBYTE, bt)

    def wrapByte(self, bt):
        return TLVFixed(AMQPType.BYTE, bt)

    def wrapUInt(self, i):
        if i < 0:
            raise ValueError('Error negative value of ' + str(i) + ' cannot be assigned to UINT type')
        value = self.convertUInt(i)
        code = None
        if len(value) == 0:
            code = AMQPType.UINT_0
        elif len(value) == 1:
            code = AMQPType.SMALL_UINT
        elif len(value) > 1:
            code = AMQPType.UINT
        return TLVFixed(code, value)

    def wrapInt(self, i):
        value = self.convertUInt(i)
        code = None
        if len(value) > 0:
            code = AMQPType.INT
        else:
            code = AMQPType.SMALL_INT
        return TLVFixed(code, value)

    def wrapULong(self, l):
        if l is None:
            raise ValueError('Wrapper cannot wrap ulong null')
        if l < 0:
            raise ValueError('negative value of ' + str(l) + ' cannot be assignet to ULONG type')
        value = self.convertULong(l)
        code = None
        if len(value) == 0:
            code = AMQPType.ULONG_0
        elif len(value) == 1:
            code = AMQPType.SMALL_ULONG
        else:
            code = AMQPType.ULONG
        return TLVFixed(code, value)

    def wrapLong(self, l):
        value = self.convertULong(l)
        code = None
        if len(value) > 1:
            code = AMQPType.LONG
        else:
            code = AMQPType.SMALL_LONG
        return TLVFixed(code, value)

    def wrapBinary(self, bt):
        if bt is None:
            raise ValueError('Wrapper cannot wrap binary null')
        code = None
        if len(bt) > 255:
            code = AMQPType.BINARY_32
        else:
            code = AMQPType.BINARY_8
        return TLVVariable(code, bt)

    def wrapUuid(self, uuid):
        if uuid is None:
            raise ValueError('Wrapper cannot wrap uuid null')
        return TLVFixed(AMQPType.UUID, bytes(uuid, 'utf-8'))

    def wrapUShort(self, sh):
        if sh < 0:
            raise ValueError('negative value of ' + str(sh) + ' cannot be assignet to UShort type')
        data = bytearray()
        data = util.addShort(data, sh)
        return TLVFixed(AMQPType.USHORT, data)

    def wrapShort(self, sh):
        data = bytearray()
        data = util.addShort(data, sh)
        return TLVFixed(AMQPType.USHORT, data)

    def wrapDouble(self, db):
        data = bytearray()
        data = util.addDouble(data, db)
        return TLVFixed(AMQPType.DOUBLE, data)

    def wrapFloat(self, f):
        data = bytearray()
        data = util.addFloat(data, f)
        return TLVFixed(AMQPType.FLOAT, data)

    def wrapChar(self, ch):
        data = bytearray()
        data = util.addInt(data, ch)
        return TLVFixed(AMQPType.CHAR, data)

    def wrapTimestamp(self, stamp):
        if stamp is None:
            raise ValueError('Wrapper cannot wrap timestamp null')
        data = bytearray()
        ts = (stamp - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        data = util.addLong(data, ts)
        return TLVFixed(AMQPType.TIMESTAMP, data)

    def wrapDecimal32(self, d):
        if d is None:
            raise ValueError('Wrapper cannot wrap decimal32 null')
        if isinstance(d, AMQPDecimal):
            return TLVFixed(AMQPType.DECIMAL_32, d.getValue())

    def wrapDecimal64(self, d):
        if d is None:
            raise ValueError('Wrapper cannot wrap decimal64 null')
        if isinstance(d, AMQPDecimal):
            return TLVFixed(AMQPType.DECIMAL_64, d.getValue())

    def wrapDecimal128(self, d):
        if d is None:
            raise ValueError('Wrapper cannot wrap decimal128 null')
        if isinstance(d, AMQPDecimal):
            return TLVFixed(AMQPType.DECIMAL_128, d.getValue())

    def wrapString(self, s):
        if s is None:
            raise ValueError('Wrapper cannot wrap string null')
        value = bytes(s,'utf-8')
        code = None
        if len(value) > 255:
            code = AMQPType.STRING_32
        else:
            code = AMQPType.STRING_8
        return TLVVariable(code, value)

    def wrapSymbol(self, s):
        if s is None:
            raise ValueError('Wrapper cannot wrap symbol null')
        if isinstance(s, AMQPSymbol):
            value = bytes(s.getValue(),'utf-8')
            code = None
            if len(value) > 255:
                code = AMQPType.SYMBOL_32
            else:
                code = AMQPType.SYMBOL_8
            return TLVVariable(code, value)

    def wrapList(self, input):
        if input is None:
            raise ValueError('Wrapper cannot wrap null list')
        list = TLVList(None,None)
        for obj in input:
            list.addElement(self.wrap(obj))
        return list

    def wrapMap(self, input):
        if input is None:
            raise ValueError('Wrapper cannot wrap null map')
        map = TLVMap(None,None)
        if isinstance(input, dict):
            for key, value in input.items():
                map[self.wrap(key)] = self.wrap(value)
        return map

    def wrapArray(self, input):
        if input is None:
            raise ValueError('Wrapper cannot wrap null array')
        array = TLVArray(None,None)
        for obj in input:
            res = self.wrap(obj)
            array.addElement(res)
        return array

    def convertUInt(self, i):
        data = bytearray()
        if i == 0:
            return data
        elif i > 0 and i <= 255:
            data = util.addByte(data, i)
            return data
        else:
            data = util.addInt(data, i)
            return data

    def convertInt(self, i):
        data = bytearray()
        if i == 0:
            return data
        elif i >= -128 and i <= 127:
            return i
        else:
            data = util.addInt(data, i)
            return data

    def convertULong(self, l):
        data = bytearray()
        if l == 0:
            return data
        elif l > 0 and l <= 255:
            return l
        else:
            data = util.addLong(data, l)
            return data

    def convertLong(self, l):
        data = bytearray()
        if l == 0:
            return data
        elif l >= -128 and l <= 127:
            return l
        else:
            data = util.addLong(data, l)
            return data

