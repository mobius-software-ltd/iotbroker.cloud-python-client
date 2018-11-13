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
from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *

class MessageHeader(AMQPSection):
    def __init__(self,durable,priority,milliseconds,firstAquirer,deliveryCount):
        self.durable = durable
        self.priority = priority
        self.milliseconds = milliseconds
        self.firstAquirer = firstAquirer
        self.deliveryCount = deliveryCount

    def getValue(self):
        list = TLVList(None, None)

        if self.durable is not None:
            list.addElement(0, AMQPWrapper.wrap(self.durable))
        if self.priority is not None:
            list.addElement(1, AMQPWrapper.wrap(self.priority))
        if self.milliseconds is not None:
            list.addElement(2, AMQPWrapper.wrap(self.milliseconds))
        if self.firstAquirer is not None:
            list.addElement(3, AMQPWrapper.wrap(self.firstAquirer))
        if self.deliveryCount is not None:
            list.addElement(4, AMQPWrapper.wrap(self.deliveryCount))

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x70))
        list.setConstructor(constructor)
        return list

    def fill(self, value):
        list = value
        if isinstance(list, TLVList):
            if len(list.getList()) > 0:
                element = list.getList()[0]
                if element is not None:
                    self.durable = AMQPUnwrapper.unwrapBool(element)
            if len(list.getList()) > 1:
                element = list.getList()[1]
                if element is not None:
                    self.priority = AMQPUnwrapper.unwrapUByte(element)
            if len(list.getList()) > 2:
                element = list.getList()[2]
                if element is not None:
                    self.milliseconds = AMQPUnwrapper.unwrapUInt(element)
            if len(list.getList()) > 3:
                element = list.getList()[3]
                if element is not None:
                    self.firstAquirer = AMQPUnwrapper.unwrapBool(element)
            if len(list.getList()) > 4:
                element = list.getList()[4]
                if element is not None:
                    self.deliveryCount = AMQPUnwrapper.unwrapUInt(element)

    def getCode(self):
        return SectionCode.HEADER

    def toString(self):
        return 'MessageHeader [durable=' + str(self.durable) + ', priority=' + str(self.priority) + ', milliseconds=' + str(self.milliseconds) + ', firstAquirer=' + str(self.firstAquirer) + ', deliveryCount=' + str(self.deliveryCount) + ']'

    def getDurable(self):
        return self.durable

    def setDurable(self, durable):
        self.durable = durable

    def getPriority(self):
        return self.priority

    def setPriority(self, priority):
        self.priority = priority

    def getMilliseconds(self):
        return self.milliseconds

    def setMilliseconds(self, milliseconds):
        self.milliseconds = milliseconds

    def getFirstAquirer(self):
        return self.firstAquirer

    def setFirstAquirer(self, firstAquirer):
        self.firstAquirer = firstAquirer

    def getDeliveryCount(self):
        return self.deliveryCount

    def setDeliveryCount(self, deliveryCount):
        self.deliveryCount = deliveryCount
