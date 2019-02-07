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
from iot.amqp.sections.AMQPSection import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.avps.SectionCode import *

class AMQPData(AMQPSection):
    def __init__(self, data):
        self.data = data

    def getValue(self):
        wrapper = AMQPWrapper()
        bin = None
        if self.data is not None:
            bin = wrapper.wrap(self.data)
        else:
            bin = TLVNull()
        constructor = DescribedConstructor(bin.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x75))
        bin.setConstructor(constructor)
        return bin

    def fill(self, value):
        unwrapper = AMQPUnwrapper()
        if value is not None:
            self.data = unwrapper.unwrapBinary(value)

    def getCode(self):
        return SectionCode.DATA

    def toString(self):
        return 'AMQPData [data=' + str(self.data) + ']'

    def getData(self):
        return self.data

    def setValue(self, data):
        self.data = data

