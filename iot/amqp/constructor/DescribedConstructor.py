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
from iot.amqp.avps.AMQPType import *
from iot.amqp.constructor.SimpleConstructor import *
from iot.amqp.tlv.api.TLVAmqp import *

class DescribedConstructor(SimpleConstructor):
    def __init__(self, code, descriptor):
        self.code = code
        self.descriptor = descriptor

    def getDescriptor(self):
        if isinstance(self.descriptor, TLVAmqp):
            return self.descriptor

    def setCode(self, code):
        self.code = code

    def getLength(self):
        if isinstance(self.descriptor, TLVAmqp):
            return self.descriptor.getLength() + 2

    def getBytes(self):
        data = bytearray(1)
        if isinstance(self.descriptor, TLVAmqp):
            descriptorBytes = self.descriptor.getBytes()
            data += descriptorBytes
            if isinstance(self.code, AMQPType):
                data.append(self.code.value)
        return data

    def getDescriptorCode(self):
        if isinstance(self.descriptor, TLVAmqp):
            return self.descriptor.getBytes()[1]