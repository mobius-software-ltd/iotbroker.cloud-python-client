from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVArray import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVMap import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.wrappers.AMQPDecimal import *
from venv.iot.amqp.wrappers.AMQPSymbol import *
from venv.iot.classes.NumericUtil import NumericUtil as util
import uuid
import numpy as np

class AMQPWrapper(object):
    def __init__(self):
        pass

    def wrap(self, obj):
        result = None

        if isinstance(obj, None):
            return TLVNull()

        if isinstance(obj, np.int8):
            result = self.wrapByte(obj)


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

    

    def convertUInt(self, i):
        data = bytearray()
        if i == 0:
            return data
        elif i > 0 and i <= 255:
            return i
        else:
            data = util.addInt(data, i)
            return data

