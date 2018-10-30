import numpy as np
from venv.iot.classes.NumericUtil import NumericUtil as util

class AMQPDecimal(object):
    def __init__(self, value):
        data = bytearray()
        if isinstance(value, bytearray):
            data = value
        if isinstance(value, np.int8):
            data = util.addByte(data, value)
        if isinstance(value, np.int16):
            data = util.addShort(data, value)
        if isinstance(value, np.int32):
            data = util.addInt(data, value)
        if isinstance(value, np.int64):
            data = util.addLong(data, value)
        if isinstance(value, np.float32):
            data = util.addFloat(data, value)
        if isinstance(value, np.complex128):
            data = util.addDouble(data, value)
        self.value = data

    def getByte(self):
        return util.getByte(self.value, 0)

    def getShort(self):
        return util.getShort(self.value)

    def getInt(self):
        return util.getInt(self.value)

    def getLong(self):
        return util.getLong(self.value)

    def getFloat(self):
        return util.getFloat(self.value)

    def getDouble(self):
        return util.getDouble(self.value)

    def getValue(self):
        return self.value



