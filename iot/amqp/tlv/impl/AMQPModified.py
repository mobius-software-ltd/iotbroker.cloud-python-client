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
from iot.amqp.avps.ErrorCode import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.header.api.Parsable import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.wrappers.AMQPSymbol import *

class AMQPModified(Parsable):
    def __init__(self, deliveryFailed, undeliverableHere, messageAnnotations):
        self.deliveryFailed = deliveryFailed
        self.undeliverableHere = undeliverableHere
        self.messageAnnotations = messageAnnotations

    def toArgumentsList(self):
        list = TLVList(None,None)
        if self.deliveryFailed is not None:
            list.addElement(0, AMQPWrapper.wrap(self.deliveryFailed))
        if self.undeliverableHere is not None:
            list.addElement(1, AMQPWrapper.wrap(self.undeliverableHere))
        if self.messageAnnotations is not None and isinstance(self.messageAnnotations,dict):
            if len(self.messageAnnotations) > 0:
                list.addElement(2, AMQPWrapper.wrapMap(self.messageAnnotations))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x27))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None:
                    self.deliveryFailed = AMQPUnwrapper.unwrapBool(element)
            if len(list.getList()) > 1 :
                element = list.getList()[1]
                if element is not None:
                    self.undeliverableHere = AMQPUnwrapper.unwrapBool(element)
            if len(list.getList()) > 2 :
                element = list.getList()[2]
                if element is not None:
                    self.messageAnnotations = AMQPUnwrapper.unwrapMap(element)

    def toString(self):
        return 'AMQPError [condition='+ str(self.condition) + ', description=' + str(self.description) + ', info=' + str(self.info) + ']'

    def getDeliveryFailed(self):
        return self.deliveryFailed

    def setDeliveryFailed(self, deliveryFailed):
        self.deliveryFailed = deliveryFailed

    def getUndeliverableHere(self):
        return self.undeliverableHere

    def setUndeliverableHere(self, undeliverableHere):
        self.undeliverableHere = undeliverableHere

    def getMessageAnnotations(self):
        return self.messageAnnotations

    def setMessageAnnotations(self, messageAnnotations):
        self.messageAnnotations = messageAnnotations