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
from iot.amqp.avps.StateCode import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.TLVArray import *
from iot.amqp.tlv.impl.TLVList import *
from iot.amqp.tlv.impl.TLVMap import *
from iot.amqp.tlv.impl.TLVFixed import *
from iot.amqp.tlv.impl.TLVVariable import *
from iot.amqp.tlv.impl.AMQPAccepted import *
from iot.amqp.tlv.impl.AMQPModified import *
from iot.amqp.tlv.impl.AMQPReceived import *
from iot.amqp.tlv.impl.AMQPRejected import *
from iot.amqp.tlv.impl.AMQPReleased import *
from iot.amqp.tlv.api.TLVFactory import *
from iot.amqp.header.api.AMQPHeader import *
from iot.amqp.sections.ApplicationProperties import *
from iot.amqp.sections.AMQPData import *
from iot.amqp.sections.DeliveryAnnotations import *
from iot.amqp.sections.AMQPFooter import *
from iot.amqp.sections.MessageHeader import *
from iot.amqp.sections.MessageAnnotations import *
from iot.amqp.sections.AMQPProperties import *
from iot.amqp.sections.AMQPSequence import *
from iot.amqp.sections.AMQPValue import *
from iot.amqp.header.impl.SASLMechanisms import *
from iot.amqp.header.impl.SASLChallenge import *
from iot.amqp.header.impl.SASLInit import *
from iot.amqp.header.impl.SASLOutcome import *
from iot.amqp.header.impl.SASLResponse import *
from iot.amqp.header.impl.AMQPOpen import *
from iot.amqp.header.impl.AMQPBegin import *
from iot.amqp.header.impl.AMQPEnd import *
from iot.amqp.header.impl.AMQPClose import *
from iot.amqp.header.impl.AMQPAttach import *
from iot.amqp.header.impl.AMQPTransfer import *
from iot.amqp.header.impl.AMQPDetach import *
from iot.amqp.header.impl.AMQPDisposition import *
from iot.amqp.header.impl.AMQPFlow import *

class HeaderFactory(object):
    def __init__(self, index):
        self.index = index
        self.tlvFactory = TLVFactory(index)

    def getIndex(self):
        return self.index

    def setIndex(self,index):
        self.index = index

    def getAMQP(self, buf):
        list = self.tlvFactory.getTlv(buf)
        self.index = self.tlvFactory.getIndex()


        if list is not None and isinstance(list,TLVAmqp):
            code  = list.getCode()

            if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                raise ValueError('Received amqp-header with malformed arguments')

            byteCode = list.getConstructor().getDescriptorCode()
            code = HeaderCode(byteCode)

            if code == HeaderCode.ATTACH:
                header = AMQPAttach(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
            elif code == HeaderCode.BEGIN:
                header = AMQPBegin(None,None,None,None,None,None,None,None,None,None,None,None)
            elif code == HeaderCode.CLOSE:
                header = AMQPClose(None,None,None,None,None)
            elif code == HeaderCode.DETACH:
                header = AMQPDetach(None,None,None,None,None,None,None)
            elif code == HeaderCode.DISPOSITION:
                header = AMQPDisposition(None,None,None,None,None,None,None,None,None,None)
            elif code == HeaderCode.END:
                header = AMQPEnd(None,None,None,None,None)
            elif code == HeaderCode.FLOW:
                header = AMQPFlow(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
            elif code == HeaderCode.OPEN:
                header = AMQPOpen(None,None,None,None,None,None,None,None,None,None,None,None,None,None)
            elif code == HeaderCode.TRANSFER:
                header = AMQPTransfer(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)

            if isinstance(header, AMQPHeader):
                header.fromArgumentsList(list)
                return header
        return None

    def getSASL(self, buf):
        list = self.tlvFactory.getTlv(buf)
        self.index = self.tlvFactory.getIndex()
        if list is not None and isinstance(list,TLVAmqp):
            code  = list.getCode()
            if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                raise ValueError('Received sasl-header with malformed arguments')
            byteCode = list.getConstructor().getDescriptorCode()
            code = HeaderCode(byteCode)

            if code == HeaderCode.CHALLENGE:
                header = SASLChallenge(None,None,None,None,None)
            elif code == HeaderCode.INIT:
                header = SASLInit(None,None,None,None,None,None,None)
            elif code == HeaderCode.MECHANISMS:
                header = SASLMechanisms(None,None,None,None,None)
            elif code == HeaderCode.OUTCOME:
                header = SASLOutcome(None,None,None,None,None,None)
            elif code == HeaderCode.RESPONSE:
                header = SASLResponse(None,None,None,None,None)

            if isinstance(header, AMQPHeader):
                header.fromArgumentsList(list)
                return header

    def getSection(self, buf):
        value = self.tlvFactory.getTlv(buf)
        section = None
        self.index = self.tlvFactory.getIndex()
        byteCode = value.getConstructor().getDescriptorCode()
        code = SectionCode(byteCode)
        if code == SectionCode.APPLICATION_PROPERTIES:
            section = ApplicationProperties(None)
        elif code == SectionCode.DATA:
            section = AMQPData(None)
        elif code == SectionCode.DELIVERY_ANNOTATIONS:
            section = DeliveryAnnotations(None)
        elif code == SectionCode.FOOTER:
            section = AMQPFooter(None)
        elif code == SectionCode.HEADER:
            section = MessageHeader(None)
        elif code == SectionCode.MESSAGE_ANNOTATIONS:
            section = MessageAnnotations(None)
        elif code == SectionCode.PROPERTIES:
            section = AMQPProperties(None)
        elif code == SectionCode.SEQUENCE:
            section = AMQPSequence(None)
        elif code == SectionCode.VALUE:
            section = AMQPValue(None)
        else:
            raise ValueError('Received header with unrecognized message section code')

        section.fill(value)
        return section