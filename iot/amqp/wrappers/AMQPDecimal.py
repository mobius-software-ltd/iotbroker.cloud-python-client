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



