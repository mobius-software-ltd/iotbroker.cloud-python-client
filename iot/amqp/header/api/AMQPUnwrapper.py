from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVArray import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVMap import *
from venv.iot.amqp.wrappers.AMQPDecimal import *
from venv.iot.amqp.wrappers.AMQPSymbol import *
from venv.iot.classes.NumericUtil import NumericUtil as util
import uuid

class AMQPUnwrapper(object):
    def __init__(self):
        pass

    def unwrapUByte(self, tlv):
        if isinstance(tlv, TLVAmqp):
            if tlv.getCode() != AMQPType.UBYTE:
                raise ValueError('Error trying to parse UBYTE: received ' + str(tlv.getCode()))
        return (tlv.getValue()[0] & 0xff)

    def unwrapByte(self, tlv):
        if isinstance(tlv, TLVAmqp):
            if tlv.getCode() != AMQPType.BYTE:
                raise ValueError('Error trying to parse BYTE: received ' + str(tlv.getCode()))
        return tlv.getValue()[0]

    def unwrapUShort(self, tlv):
        if isinstance(tlv, TLVAmqp):
            if tlv.getCode() != AMQPType.USHORT:
                raise ValueError('Error trying to parse USHORT: received ' + str(tlv.getCode()))
        return (util.getShort(tlv.getValue()) & 0xffff)

    def unwrapShort(self, tlv):
        if isinstance(tlv, TLVAmqp):
            if tlv.getCode() != AMQPType.SHORT:
                raise ValueError('Error trying to parse SHORT: received ' + str(tlv.getCode()))
        return util.getShort(tlv.getValue())

    def unwrapUInt(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.UINT,AMQPType.SMALL_UINT,AMQPType.UINT_0):
                raise ValueError('Error trying to parse UINT: received ' + str(tlv.getCode()))
            value = tlv.getValue()
            if len(value) == 0:
                return 0
            elif len(value) == 1:
                return (tlv.getValue()[0] & 0xff)
            return (util.getInt(tlv.getValue()) & 0xffffffff)

    def unwrapInt(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.INT,AMQPType.SMALL_INT):
                raise ValueError('Error trying to parse INT: received ' + str(tlv.getCode()))
            value = tlv.getValue()
            if len(value) == 0:
                return 0
            elif len(value) == 1:
                return tlv.getValue()[0]
            return util.getInt(tlv.getValue())

    def unwrapULong(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.ULONG,AMQPType.SMALL_ULONG,AMQPType.ULONG_0):
                raise ValueError('Error trying to parse ULONG: received ' + str(tlv.getCode()))
            value = tlv.getValue()
            if len(value) == 0:
                return 0
            elif len(value) == 1:
                return (tlv.getValue()[0] & 0xff)
            return util.getLong(tlv.getValue())

    def unwrapLong(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.LONG,AMQPType.SMALL_LONG):
                raise ValueError('Error trying to parse LONG: received ' + str(tlv.getCode()))
            value = tlv.getValue()
            if len(value) == 0:
                return 0
            elif len(value) == 1:
                return tlv.getValue()[0]
            return util.getLong(tlv.getValue())

    def unwrapBool(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code  == AMQPType.BOOLEAN:
                val = tlv.getValue()[0]
                if val == 0:
                    return False
                elif val == 1:
                    return True
                else:
                    raise ValueError('Invalid Boolean type value: ' + str(tlv.getCode()))
            if code == AMQPType.BOOLEAN_TRUE:
                return True
            elif code == AMQPType.BOOLEAN_FALSE:
                return False
            else:
                raise ValueError('Error trying to parse BOOLEAN: received ' + str(tlv.getCode()))

    def unwrapDouble(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code != AMQPType.DOUBLE:
                raise ValueError('Error trying to parse DOUBLE: received ' + str(tlv.getCode()))
            return util.getDouble(tlv.getValue())

    def unwrapFloat(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code != AMQPType.FLOAT:
                raise ValueError('Error trying to parse FLOAT: received ' + str(tlv.getCode()))
            return util.getFloat(tlv.getValue())

    def unwrapTimastamp(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code != AMQPType.TIMESTAMP:
                raise ValueError('Error trying to parse TIMESTAMP: received ' + str(tlv.getCode()))
            return util.getLong(tlv.getValue())

    def unwrapDecimal(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.DECIMAL_32,AMQPType.DECIMAL_64,AMQPType.DECIMAL_128):
                raise ValueError('Error trying to parse DECIMAL: received ' + str(tlv.getCode()))
            return AMQPDecimal(tlv.getValue())

    def unwrapChar(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code != AMQPType.CHAR:
                raise ValueError('Error trying to parse CHAR: received ' + str(tlv.getCode()))
            return util.getInt(tlv.getValue())

    def unwrapString(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.STRING_8,AMQPType.STRING_32):
                raise ValueError('Error trying to parse STRING: received ' + str(tlv.getCode()))
            return str(util.getString(tlv.getValue()))

    def unwrapSymbol(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.SYMBOL_8,AMQPType.SYMBOL_32):
                raise ValueError('Error trying to parse SYMBOL: received ' + str(tlv.getCode()))
            return AMQPSymbol(str(util.getString(tlv.getValue())))

    def unwrapBinary(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.BINARY_8,AMQPType.BINARY_32):
                raise ValueError('Error trying to parse BINARY: received ' + str(tlv.getCode()))
            return tlv.getValue()

    def unwrapUuid(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code != AMQPType.UUID:
                raise ValueError('Error trying to parse UUID: received ' + str(tlv.getCode()))
            return uuid.UUID(tlv.getValue())

    def unwrapList(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                raise ValueError('Error trying to parse LIST: received ' + str(tlv.getCode()))
            result = []
            if isinstance(tlv, TLVList):
                for value in tlv.getList():
                    result.append(self.unwrap(value))
            return result

    def unwrapMap(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.MAP_8,AMQPType.MAP_32):
                raise ValueError('Error trying to parse MAP: received ' + str(tlv.getCode()))
            result = {}
            if isinstance(tlv, TLVMap):
                for key, value in tlv.getMap().items():
                    k = self.unwrap(key)
                    v = self.unwrap(value)
                    result[k] = v
            return result

    def unwrapArray(self, tlv):
        if isinstance(tlv, TLVAmqp):
            code = tlv.getCode()
            if code not in (AMQPType.ARRAY_8,AMQPType.ARRAY_32):
                raise ValueError('Error trying to parse ARRAY: received ' + str(tlv.getCode()))
            result = []
            if isinstance(tlv, TLVArray):
                for value in tlv.getElements():
                    result.append(self.unwrap(value))
            return result

    def unwrap(self, value):
        if isinstance(value, TLVAmqp):
            code = value.getCode()
            if code == AMQPType.NULL:
                return None
            if code in(AMQPType.ARRAY_8,AMQPType.ARRAY_32):
                return self.unwrapArray(value)
            if code in(AMQPType.BINARY_8,AMQPType.BINARY_32):
                return self.unwrapBinary(value)
            if code == AMQPType.UBYTE:
                return self.unwrapUByte(value)
            if code in(AMQPType.BOOLEAN,AMQPType.BOOLEAN_TRUE,AMQPType.BOOLEAN_FALSE):
                return self.unwrapBool(value)
            if code == AMQPType.BYTE:
                return self.unwrapByte(value)
            if code == AMQPType.CHAR:
                return self.unwrapChar(value)
            if code == AMQPType.DOUBLE:
                return self.unwrapDouble(value)
            if code == AMQPType.FLOAT:
                return self.unwrapFloat(value)
            if code in (AMQPType.INT,AMQPType.SMALL_INT):
                return self.unwrapInt(value)
            if code in(AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                return self.unwrapList(value)
            if code in (AMQPType.LONG, AMQPType.SMALL_LONG):
                return self.unwrapLong(value)
            if code in (AMQPType.MAP_8, AMQPType.MAP_32):
                return self.unwrapMap(value)
            if code == AMQPType.SHORT:
                return self.unwrapShort(value)
            if code in (AMQPType.STRING_8, AMQPType.STRING_32):
                return self.unwrapString(value)
            if code in (AMQPType.SYMBOL_8, AMQPType.SYMBOL_32):
                return self.unwrapSymbol(value)
            if code == AMQPType.TIMESTAMP:
                return self.unwrapTimastamp(value)
            if code in(AMQPType.UINT,AMQPType.SMALL_UINT,AMQPType.UINT_0):
                return self.unwrapUInt(value)
            if code in (AMQPType.ULONG, AMQPType.SMALL_ULONG, AMQPType.ULONG_0):
                return self.unwrapULong(value)
            if code == AMQPType.USHORT:
                return self.unwrapUShort(value)
            if code == AMQPType.UUID:
                return self.unwrapUuid(value)
            if code in (AMQPType.DECIMAL_32, AMQPType.DECIMAL_64, AMQPType.DECIMAL_128):
                return self.unwrapDecimal(value)
            raise ValueError('Error received unrecognized type ' + str(code))
