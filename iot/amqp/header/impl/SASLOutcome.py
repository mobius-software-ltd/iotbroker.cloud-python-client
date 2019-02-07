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
from iot.amqp.avps.OutcomeCode import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.header.api.AMQPHeader import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.TLVFixed import *
from iot.amqp.tlv.impl.TLVList import *

class SASLOutcome(AMQPHeader):
    def __init__(self,code,doff,type,channel,outcomeCode,additionalData):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.OUTCOME
        if doff is not None:
            self.doff = doff
        else:
            self.doff = 2
        if type is not None:
            self.type = type
        else:
            self.type = 0
        if channel is not None:
            self.channel = channel
        else:
            self.channel = 0
        self.outcomeCode = outcomeCode
        self.additionalData = additionalData

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.outcomeCode == None and isinstance(self.outcomeCode,OutcomeCode):
            raise ValueError("SASL-Outcome header's code can't be null")
        list.addElement(0,AMQPWrapper.wrap(self.outcomeCode.value))

        if self.additionalData is not None:
            list.addElement(1, AMQPWrapper.wrap(self.additionalData))

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x44))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        unwrapper = AMQPUnwrapper()
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size == 0:
                raise ValueError("Received malformed SASL-Outcome header: code can't be null")
            if size > 2:
                raise ValueError('Received malformed SASL-Outcome header. Invalid number of arguments: ' + str(size))

            if size > 0:
                element = list.getList()[0]
                if element is None or element.isNull():
                    raise ValueError("Received malformed SASL-Outcome header: code can't be null")
                self.outcomeCode = OutcomeCode(unwrapper.unwrapUByte(element)).value

            if size > 1:
                element = list.getList()[1]
                if element is not None:
                    self.additionalData = unwrapper.unwrapBinary(element)


    def toString(self):
        return "SASLOutcome [outcomeCode=" + str(self.outcomeCode) + ", additionalData=" + str(self.additionalData) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setOutcomeCode(self, outcomeCode):
        self.outcomeCode = outcomeCode

    def getOutcomeCode(self):
        return self.outcomeCode

    def setAdditionalData(self, additionalData):
        self.additionalData = additionalData

    def getAdditionalData(self):
        return self.additionalData


