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
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.classes.NumericUtil import NumericUtil as util
import numpy as np

class TLVFixed(TLVAmqp):
    def __init__(self, code, value):
        self.value = value
        self.constructor = SimpleConstructor(code)

    def getBytes(self):
        constructorBytes = self.constructor.getBytes()
        data = bytearray()
        if isinstance(self.constructor,DescribedConstructor):
            data += constructorBytes
        else:
            data.append(constructorBytes)
        if len(str(self.value)) > 0:
            if isinstance(self.value, int) or isinstance(self.value,np.int8) or isinstance(self.value,np.int16) or isinstance(self.value,np.int64):
                    data.append(self.value)
                    return data
            elif (self.getCode() in (AMQPType.UINT,AMQPType.UINT_0,AMQPType.SMALL_UINT)) and (isinstance(self.value,bytearray) or isinstance(self.value,bytes)):
                data += self.value
                return data
            elif self.getCode() in (AMQPType.BOOLEAN_TRUE,AMQPType.BOOLEAN_FALSE):
                return data
            else:
                data.append(len(self.value))
                data += self.value
                return data

    def getLength(self):
        if self.value == b'':
            return 1
        elif isinstance(self.value,int) or isinstance(self.value,np.int8) or isinstance(self.value,np.int16) or isinstance(self.value,np.int64):
            return self.constructor.getLength() + 1
        elif (self.getCode() in (AMQPType.UINT,AMQPType.UINT_0,AMQPType.SMALL_UINT)) and (isinstance(self.value,bytearray) or isinstance(self.value,bytes)):
            return self.constructor.getLength() + len(self.value)
        elif self.getCode() in (AMQPType.BOOLEAN_TRUE,AMQPType.BOOLEAN_FALSE):
            return self.constructor.getLength()
        else:
            return self.constructor.getLength() + len(self.value) + 1

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
        return self.constructor.getCode()

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        pass

    def setCode(self, arg):
        pass

    def setConstructor(self, constructor):
        self.constructor = constructor