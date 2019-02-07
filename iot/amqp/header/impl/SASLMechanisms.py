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
from iot.amqp.avps.HeaderCode import *
from iot.amqp.avps.SectionCode import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.header.api.AMQPHeader import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.TLVFixed import *
from iot.amqp.tlv.impl.TLVList import *

class SASLMechanisms(AMQPHeader):
    def __init__(self,code,doff,type,channel,mechanisms):

        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.MECHANISMS
        if doff is not None:
            self.doff = doff
        else:
            self.doff = 2
        if type is not None:
            self.type = type
        else:
            self.type = 1
        if channel is not None:
            self.channel = channel
        else:
            self.channel = 0
        self.mechanisms = mechanisms

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.mechanisms == None:
            raise ValueError("At least one SASL Mechanism must be specified")
        wrapper = AMQPWrapper()
        list.addElement(0,wrapper.wrapArray(self.mechanisms))
        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x40))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size > 0:
                element = list.getList()[0]
                if element is None and not element.isNull():
                    raise ValueError("Received malformed SASL-Init header: mechanism can't be null")
                unwrapper = AMQPUnwrapper()
                self.mechanisms = unwrapper.unwrapArray(element)

    def toString(self):
        return "SASLMechanisms [mechanisms=" + str(self.mechanisms) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setMechanisms(self, mechanisms):
        self.mechanisms = mechanisms

    def getMechanisms(self):
        return self.mechanisms


