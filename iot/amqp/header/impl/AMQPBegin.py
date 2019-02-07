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
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.header.api.AMQPHeader import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.TLVFixed import *
from iot.amqp.tlv.impl.TLVList import *
from iot.amqp.wrappers.AMQPSymbol import *

class AMQPBegin(AMQPHeader):
    def __init__(self,code,doff,type,channel,remoteChannel,nextOutgoingId,incomingWindow,outgoingWindow,handleMax,offeredCapabilities,desiredCapabilities,properties):
        if code is None:
            self.code = HeaderCode.BEGIN
        else:
            self.code = code

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

        self.remoteChannel = remoteChannel
        self.nextOutgoingId = nextOutgoingId
        self.incomingWindow = incomingWindow
        self.outgoingWindow = outgoingWindow
        self.handleMax = handleMax
        self.offeredCapabilities = offeredCapabilities
        self.desiredCapabilities = desiredCapabilities
        self.properties = properties

    def toArgumentsList(self):
        list = TLVList(None,None)
        wrapper = AMQPWrapper()
        if self.remoteChannel is not None:
            list.addElement(0, wrapper.wrap(self.remoteChannel))
        if self.nextOutgoingId is None:
            raise ValueError("Begin header's next-outgoing-id can't be null")
        list.addElement(1, wrapper.wrap(self.nextOutgoingId))
        if self.incomingWindow is None:
            raise ValueError("Begin header's incoming-window can't be null")
        list.addElement(2, wrapper.wrap(self.incomingWindow))
        if self.outgoingWindow is None:
            raise ValueError("Begin header's outgoing-window can't be null")
        list.addElement(3, wrapper.wrap(self.outgoingWindow))
        if self.handleMax is not None:
            list.addElement(4, wrapper.wrap(self.handleMax))
        if self.offeredCapabilities is not None and len(self.offeredCapabilities) > 0:
            list.addElement(5, wrapper.wrapArray(self.offeredCapabilities))
        if self.desiredCapabilities is not None and len(self.desiredCapabilities) > 0:
            list.addElement(6, wrapper.wrapArray(self.desiredCapabilities))
        if self.properties is not None and len(self.properties) > 0:
            list.addElement(7, wrapper.wrapMap(self.properties))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        unwrapper = AMQPUnwrapper()
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size < 4:
                raise ValueError('Received malformed Begin header: mandatory fields next-outgoing-id, incoming-window and outgoing-window must not be null')
            if size > 8:
                raise ValueError('Received malformed Begin header. Invalid number of arguments: ' + str(size))
            if size > 0:
                element = list.getList()[0]
                if element is not None and not element.isNull():
                    self.remoteChannel = unwrapper.unwrapUShort(element)
            if size > 1:
                element = list.getList()[1]
                if element is not None and not element.isNull():
                    self.nextOutgoingId = unwrapper.unwrapUInt(element)
                else:
                    raise ValueError("Received malformed Begin header: next-outgoing-id can't be null")
            if size > 2:
                element = list.getList()[2]
                if element is not None and not element.isNull():
                    self.incomingWindow = unwrapper.unwrapUInt(element)
                else:
                    raise ValueError("Received malformed Begin header: incoming-window can't be null")
            if size > 3:
                element = list.getList()[3]
                if element is not None and not element.isNull():
                    self.outgoingWindow = unwrapper.unwrapUInt(element)
                else:
                    raise ValueError("Received malformed Begin header: outgoing-window can't be null")
            if size > 4:
                element = list.getList()[4]
                if element is not None and not element.isNull():
                    self.handleMax = unwrapper.unwrapUInt(element)
            if size > 5:
                element = list.getList()[5]
                if element is not None and not element.isNull():
                    self.offeredCapabilities = unwrapper.unwrapArray(element)
            if size > 6:
                element = list.getList()[6]
                if element is not None and not element.isNull():
                    self.desiredCapabilities = unwrapper.unwrapArray(element)
            if size > 7:
                element = list.getList()[7]
                if element is not None and not element.isNull():
                    self.properties = unwrapper.unwrapMap(element)

    def toString(self):
        return "AMQPBegin [remoteChannel=" + str(self.remoteChannel) + ", nextOutgoingId=" + str(self.nextOutgoingId) + ", incomingWindow=" + str(self.incomingWindow) + ", outgoingWindow=" + str(self.outgoingWindow) + ", handleMax=" + str(self.handleMax) + ", offeredCapabilities=" + str(self.offeredCapabilities) + ", desiredCapabilities=" + str(self.desiredCapabilities) + ", properties=" + str(self.properties) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setRemoteChannel(self, remoteChannel):
        self.remoteChannel = remoteChannel

    def getRemoteChannel(self):
        return self.remoteChannel

    def setNextOutgoingId(self, nextOutgoingId):
        self.nextOutgoingId = nextOutgoingId

    def getNextOutgoingId(self):
        return self.nextOutgoingId

    def setIncomingWindow(self, incomingWindow):
        self.incomingWindow = incomingWindow

    def getIncomingWindow(self):
        return self.incomingWindow

    def setOutgoingWindow(self, outgoingWindow):
        self.outgoingWindow = outgoingWindow

    def getOutgoingWindow(self):
        return self.outgoingWindow

    def setHandleMax(self, handleMax):
        self.handleMax = handleMax

    def getHandleMax(self):
        return self.handleMax

    def setOfferedCapabilities(self, offeredCapabilities):
        self.offeredCapabilities = offeredCapabilities

    def getOfferedCapabilities(self):
        return self.offeredCapabilities

    def setDesiredCapabilities(self, desiredCapabilities):
        self.desiredCapabilities = desiredCapabilities

    def getDesiredCapabilities(self):
        return self.desiredCapabilities

    def setProperties(self, properties):
        self.properties = properties

    def getProperties(self):
        return self.properties







