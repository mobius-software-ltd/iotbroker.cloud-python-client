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
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.wrappers.AMQPSymbol import *

class AMQPFlow(AMQPHeader):
    def __init__(self,code,doff,type,channel,nextIncomingId,incomingWindow,nextOutgoingId,outgoingWindow,handle,deliveryCount,linkCredit,available,drain,echo,properties):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.FLOW
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

        self.nextIncomingId = nextIncomingId
        self.nextOutgoingId = nextOutgoingId
        self.incomingWindow = incomingWindow
        self.outgoingWindow = outgoingWindow
        self.handle = handle
        self.deliveryCount = deliveryCount
        self.linkCredit = linkCredit
        self.available = available
        self.drain = drain
        self.echo = echo
        self.properties = properties

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.nextIncomingId is not None:
            list.addElement(0, AMQPWrapper.wrap(self.nextIncomingId))
        if self.incomingWindow is None:
            raise ValueError("Flow header's incoming-window can't be null")
        list.addElement(1, AMQPWrapper.wrap(self.incomingWindow))
        if self.nextOutgoingId is None:
            raise ValueError("Flow header's next-outgoing-id can't be null")
        list.addElement(2, AMQPWrapper.wrap(self.nextOutgoingId))
        if self.outgoingWindow is None:
            raise ValueError("Flow header's outgoing-window can't be null")
        list.addElement(3, AMQPWrapper.wrap(self.outgoingWindow))
        if self.handle is not None:
            list.addElement(4, AMQPWrapper.wrap(self.handle))
        if self.deliveryCount is not None:
            if self.handle is not None:
                list.addElement(5, AMQPWrapper.wrap(self.deliveryCount))
            else:
                raise ValueError("Flow headers delivery-count can't be assigned when handle is not specified")
        if self.linkCredit is not None:
            if self.handle is not None:
                list.addElement(6, AMQPWrapper.wrap(self.linkCredit))
            else:
                raise ValueError("Flow headers link-credit can't be assigned when handle is not specified")
        if self.available is not None:
            if self.handle is not None:
                list.addElement(7, AMQPWrapper.wrap(self.available))
            else:
                raise ValueError("Flow headers available can't be assigned when handle is not specified")
        if self.drain is not None:
            if self.handle is not None:
                list.addElement(8, AMQPWrapper.wrap(self.drain))
            else:
                raise ValueError("Flow headers drain can't be assigned when handle is not specified")
        if self.echo is not None:
            list.addElement(9,AMQPWrapper.wrap(self.echo))
        if self.properties is not None and len(self.properties) > 0:
            list.addElement(10, AMQPWrapper.wrapMap(self.properties))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size < 4:
                raise ValueError('Received malformed Flow header: mandatory fields incoming-window, next-outgoing-id and outgoing-window must not be null')
            if size > 11:
                raise ValueError('Received malformed Flow header. Invalid number of arguments: ' + str(size))

            if size > 0:
                element = list.getList()[0]
                if element is not None and not element.isNull():
                    self.nextIncomingId = AMQPUnwrapper.unwrapUInt(element)
            if size > 1:
                element = list.getList()[1]
                if element is not None and not element.isNull():
                    self.incomingWindow = AMQPUnwrapper.unwrapUInt(element)
                else:
                    raise ValueError("Received malformed Flow header: incoming-window can't be null")
            if size > 2:
                element = list.getList()[2]
                if element is not None and not element.isNull():
                    self.nextOutgoingId = AMQPUnwrapper.unwrapUInt(element)
                else:
                    raise ValueError("Received malformed Begin header:next-outgoing-id can't be null")
            if size > 3:
                element = list.getList()[3]
                if element is not None and not element.isNull():
                    self.outgoingWindow = AMQPUnwrapper.unwrapUInt(element)
                else:
                    raise ValueError("Received malformed Begin header: outgoing-window can't be null")
            if size > 4:
                element = list.getList()[4]
                if element is not None and not element.isNull():
                    self.handle = AMQPUnwrapper.unwrapUInt(element)
            if size > 5:
                element = list.getList()[5]
                if element is not None:
                    if self.handle is not None and not element.isNull():
                        self.deliveryCount = AMQPUnwrapper.unwrapUInt(element)
                    else:
                        raise ValueError("Received malformed Flow header: delivery-count can't be present when handle is null")
            if size > 6:
                element = list.getList()[6]
                if element is not None:
                    if self.handle is not None and not element.isNull():
                        self.linkCredit = AMQPUnwrapper.unwrapUInt(element)
                    else:
                        raise ValueError("Received malformed Flow header: link-credit can't be present when handle is null")
            if size > 7:
                element = list.getList()[7]
                if element is not None:
                    if self.handle is not None and not element.isNull():
                        self.available = AMQPUnwrapper.unwrapUInt(element)
                    else:
                        raise ValueError("Received malformed Flow header: available can't be present when handle is null")
            if size > 8:
                element = list.getList()[8]
                if element is not None:
                    if self.handle is not None and not element.isNull():
                        self.drain = AMQPUnwrapper.unwrapBool(element)
                    else:
                        raise ValueError("Received malformed Flow header: drain can't be present when handle is null")
            if size > 9:
                element = list.getList()[9]
                if element is not None and not element.isNull():
                    self.echo = AMQPUnwrapper.unwrapBool(element)
            if size > 10:
                element = list.getList()[10]
                if element is not None and not element.isNull():
                    self.properties = AMQPUnwrapper.unwrapMap(element)

    def toString(self):
        return "AMQPFlow [nextIncomingId=" + str(self.nextIncomingId) + ", incomingWindow=" + str(self.incomingWindow) + ", nextOutgoingId=" + str(self.nextOutgoingId) + ", outgoingWindow=" + str(self.outgoingWindow) + ", handle=" + str(self.handle) + ", deliveryCount=" + str(self.deliveryCount) + ", linkCredit=" + str(self.linkCredit) + ", avaliable=" + str(self.avaliable) + ", drain=" + str(self.drain) + ", echo=" + str(self.echo) + ", properties=" + str(self.properties) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setNextIncomingId(self, nextIncomingId):
        self.nextIncomingId = nextIncomingId

    def getNextIncomingId(self):
        return self.nextIncomingId

    def setIncomingWindow(self, incomingWindow):
        self.incomingWindow = incomingWindow

    def getIncomingWindow(self):
        return self.incomingWindow

    def setNextOutgoingId(self, nextOutgoingId):
        self.nextOutgoingId = nextOutgoingId

    def getNextOutgoingId(self):
        return self.nextOutgoingId

    def setOutgoingWindow(self, outgoingWindow):
        self.outgoingWindow = outgoingWindow

    def getOutgoingWindow(self):
        return self.outgoingWindow

    def setHandle(self, handle):
        self.handle = handle

    def getHandle(self):
        return self.handle

    def setDeliveryCount(self, deliveryCount):
        self.deliveryCount = deliveryCount

    def getDeliveryCount(self):
        return self.deliveryCount

    def setLinkCredit(self, linkCredit):
        self.linkCredit = linkCredit

    def getLinkCredit(self):
        return self.linkCredit

    def setAvaliable(self, avaliable):
        self.avaliable = avaliable

    def getAvaliable(self):
        return self.avaliable

    def setDrain(self, drain):
        self.drain = drain

    def getDrain(self):
        return self.drain

    def setEcho(self, echo):
        self.echo = echo

    def getEcho(self):
        return self.echo

    def setProperties(self, properties):
        self.properties = properties

    def getProperties(self):
        return self.properties



