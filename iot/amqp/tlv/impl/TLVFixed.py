from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.SimpleConstructor import *

from venv.iot.classes.NumericUtil import NumericUtil as util

class TLVFixed(TLVAmqp):
    def __init__(self, code, value):
        self.value = value
        self.constructor = SimpleConstructor(code)

    def getBytes(self):
        constructorBytes = self.constructor.getBytes()
        #data = bytearray(len(str(constructorBytes))+len(str(self.value)))
        data = bytearray()
        data.append(constructorBytes)
        print('data= ' + str(data))
        if len(str(self.value)) > 0:
            data.append(self.value)
            #data[len(constructorBytes):len(constructorBytes)+len(self.value)-1] = self.value[0:len(self.value)-1]
        return data

    def getLength(self):
        return len(str(self.value)) + self.constructor.getLength()

    def getValue(self):
        return self.value

    def toString(self):
        code = self.constructor.getCode()
        s = None
        if code == AMQPType.BOOLEAN_TRUE:
            s = '1'
        elif code in (AMQPType.BOOLEAN_FALSE,AMQPType.UINT_0,AMQPType.ULONG_0):
            s = '0'
        elif code in (AMQPType.BOOLEAN,AMQPType.BYTE,AMQPType.UBYTE,AMQPType.SMALL_INT,AMQPType.SMALL_LONG,AMQPType.SMALL_UINT,AMQPType.ULONG):
            s = str(self.value[0])
        elif code in (AMQPType.SHORT, AMQPType.USHORT):
            s = str(util.getShort(self.value))
        elif code in (AMQPType.CHAR, AMQPType.DECIMAL_32,AMQPType.FLOAT,AMQPType.INT,AMQPType.UINT):
            s = str(util.getInt(self.value))
        elif code in (AMQPType.DECIMAL_64, AMQPType.DOUBLE,AMQPType.LONG,AMQPType.ULONG,AMQPType.TIMESTAMP):
            s = str(util.getLong(self.value))
        if code == AMQPType.DECIMAL_128:
            s = 'decimal-128'
        if code == AMQPType.UUID:
            s = str(self.value)
        return s

    def getCode(self):
        pass

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        pass

    def setCode(self, arg):
        pass

    def setConstructor(self, arg):
        pass