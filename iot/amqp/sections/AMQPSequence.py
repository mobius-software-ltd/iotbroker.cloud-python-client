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

class AMQPSequence(AMQPSection):
    def __init__(self, sequence):
        self.sequence = sequence

    def getValue(self):
        list = TLVList(None, None)

        if self.sequence is not None and len(self.sequence) > 0:
            list = AMQPWrapper.wrapList(self.sequence)

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x76))
        list.setConstructor(constructor)
        return list

    def fill(self, list):
        if list is not None:
            self.sequence = AMQPUnwrapper.unwrapList(list)

    def getCode(self):
        return SectionCode.SEQUENCE

    def toString(self):
        return 'AMQPSequence [sequence=' + str(self.sequence) + ']'

    def getSequence(self):
        return self.sequence

    def setSequence(self, sequence):
        self.sequence = sequence

