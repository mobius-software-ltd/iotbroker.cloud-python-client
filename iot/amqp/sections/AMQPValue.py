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

class AMQPValue(AMQPSection):
    def __init__(self, value):
        self.value = value

    def getValue(self):
        val = None
        if self.value is not None:
            val = AMQPWrapper.wrap(self.value)
        else:
            val = TLVNull()

        if val is not None:
            constructor = DescribedConstructor(val.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x77))
            val.setConstructor(constructor)
        return val

    def fill(self, value):
        if value is not None:
            self.value = AMQPUnwrapper.unwrap(value)

    def getCode(self):
        return SectionCode.VALUE

    def toString(self):
        return 'AMQPValue [value=' + str(self.value) + ']'

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

