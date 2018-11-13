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
from venv.iot.amqp.tlv.impl.TLVNull import *

class AMQPOpen(AMQPHeader):
    def __init__(self,code,doff,type,channel,containerId,hostname,maxFrameSize,channelMax,idleTimeout,outgoingLocales,incomingLocales,offeredCapabilities,desiredCapabilities,properties):
        if code is None:
            self.code = HeaderCode.OPEN
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

        self.containerId = containerId
        self.hostname = hostname
        self.maxFrameSize = maxFrameSize
        self.channelMax = channelMax
        self.idleTimeout = idleTimeout
        self.outgoingLocales = outgoingLocales
        self.incomingLocales = incomingLocales
        self.offeredCapabilities = offeredCapabilities
        self.desiredCapabilities = desiredCapabilities
        self.properties = properties

    def toArgumentsList(self):
        list = TLVList(None,None)
        wrapper = AMQPWrapper()
        if self.containerId is None:
            raise ValueError("Detach header's container id can't be null")
        list.addElement(0, wrapper.wrap(self.containerId))
        if self.hostname is not None:
            list.addElement(1, wrapper.wrap(self.hostname))
        if self.maxFrameSize is not None:
            list.addElement(2, wrapper.wrap(self.maxFrameSize))
        if self.channelMax is not None:
            list.addElement(3, wrapper.wrap(self.channelMax))
        if self.idleTimeout is not None:
            list.addElement(4, wrapper.wrap(self.idleTimeout))
        if self.outgoingLocales is not None and len(self.outgoingLocales) > 0:
            list.addElement(5, wrapper.wrapArray(self.outgoingLocales))
        if self.incomingLocales is not None and len(self.incomingLocales) > 0:
            list.addElement(6, wrapper.wrapArray(self.incomingLocales))
        if self.offeredCapabilities is not None and len(self.offeredCapabilities) > 0:
            list.addElement(7, wrapper.wrapArray(self.offeredCapabilities))
        if self.desiredCapabilities is not None and len(self.desiredCapabilities) > 0:
            list.addElement(8, wrapper.wrapArray(self.desiredCapabilities))
        if self.properties is not None and len(self.properties) > 0:
            list.addElement(9, wrapper.wrapMap(self.properties))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        #print('AMQPOpen list.values= ' + str(list.values))
        return list

    def fromArgumentsList(self, list):
        unwrapper = AMQPUnwrapper()
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size  == 0:
                raise ValueError("Received malformed Open header: container id can't be null")
            if size > 10:
                raise ValueError("Received malformed Open header. Invalid number of arguments: " + str(size))

            element = list.getList()[0]

            if element is None:
                raise ValueError("Received malformed Open header: container id can't be null")
            self.containerId = unwrapper.unwrapString(element)

            if size > 1:
                element = list.getList()[1]
                if element is not None and not element.isNull():
                    self.hostname = unwrapper.unwrapString(element)
            if size > 2:
                element = list.getList()[2]
                if element is not None and not element.isNull():
                    self.maxFrameSize = unwrapper.unwrapUInt(element) 
            if size > 3:
                element = list.getList()[3]
                if element is not None and not element.isNull():
                    self.channelMax = unwrapper.unwrapUShort(element)
            if size > 4:
                element = list.getList()[4]
                if element is not None and not element.isNull():
                    self.idleTimeout = unwrapper.unwrapUInt(element)
            if size > 5:
                element = list.getList()[5]
                if element is not None and not element.isNull():
                    self.outgoingLocales = unwrapper.unwrapArray(element)
            if size > 6:
                element = list.getList()[6]
                if element is not None and not element.isNull():
                    self.incomingLocales = unwrapper.unwrapArray(element)
            if size > 7:
                element = list.getList()[7]
                if element is not None and not element.isNull():
                    self.offeredCapabilities = unwrapper.unwrapArray(element)
            if size > 8:
                element = list.getList()[8]
                if element is not None and not element.isNull():
                    self.desiredCapabilities = unwrapper.unwrapArray(element)
            if size > 9:
                element = list.getList()[9]
                if element is not None and not element.isNull():
                    self.properties = unwrapper.unwrapMap(element)

    def toString(self):
        return "AMQPOpen [containerId=" + str(self.containerId) + ", hostname=" + str(self.hostname) + ", maxFrameSize=" + str(self.maxFrameSize) + ", channelMax=" + str(self.channelMax) + ", idleTimeout=" + str(self.idleTimeout) + ", outgoingLocales=" + str(self.outgoingLocales) + ", incomingLocales=" + str(self.incomingLocales) + ", offeredCapabilities=" + str(self.offeredCapabilities) + ", desiredCapabilities=" + str(self.desiredCapabilities) + ", properties=" + str(self.properties) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setContainerId(self, containerId):
        self.containerId = containerId

    def getContainerId(self):
        return self.containerId

    def setHostname(self, hostname):
        self.hostname = hostname

    def getHostname(self):
        return self.hostname

    def setMaxFrameSize(self, maxFrameSize):
        self.maxFrameSize = maxFrameSize

    def getMaxFrameSize(self):
        return self.maxFrameSize

    def setChannelMax(self, channelMax):
        self.channelMax = channelMax

    def getChannelMax(self):
        return self.channelMax

    def setIdleTimeout(self, idleTimeout):
        self.idleTimeout = idleTimeout

    def getIdleTimeout(self):
        return self.idleTimeout

    def setOutgoingLocales(self, outgoingLocales):
        self.outgoingLocales = outgoingLocales

    def getOutgoingLocales(self):
        return self.outgoingLocales

    def setIncomingLocales(self, incomingLocales):
        self.incomingLocales = incomingLocales

    def getIncomingLocales(self):
        return self.incomingLocales

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