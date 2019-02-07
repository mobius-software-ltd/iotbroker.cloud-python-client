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
from iot.classes.NumericUtil import NumericUtil as util
import numpy as np

class AMQPMessageFormat(object):
    def __init__(self, value, messageFormat, version):
        if value != None:
            self.initValue(value)
        else:
            self.initFormat(messageFormat, version)

    def initValue(self, value):
        arr = bytearray()
        arr = util.addInt(arr, value)
        mf = bytearray(1)
        mf += arr[0:3]
        self.messageFormat = util.getInt(mf)
        self.version = util.getByte(arr[3:4],0) & 0xff

    def initFormat(self, messageFormat, version):
        self.messageFormat = messageFormat
        self.version = version

    def getMessageFormat(self):
        return self.messageFormat

    def getVersion(self):
        return self.version

    def encode(self):
        arr = bytearray()
        mf = bytearray()
        mf = util.addInt(mf, self.getMessageFormat())
        arr +=  mf[1:4]
        arr = util.addByte(arr,self.getVersion())
        return np.int64(util.getInt(arr))



