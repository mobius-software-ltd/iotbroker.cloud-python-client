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

class SASLInit(AMQPHeader):
    def __init__(self,code,doff,type,channel,mechanism,initialRespone,hostName):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.INIT
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
        self.mechanism = mechanism
        self.initialRespone = initialRespone
        self.hostName = hostName

    def toArgumentsList(self):
        list = TLVList(None,None)
        wrapper = AMQPWrapper()
        if self.mechanism == None:
            raise ValueError("SASL-Init header's mechanism can't be null")
        list.addElement(0,wrapper.wrap(self.mechanism))
        if self.initialRespone is not None:
            list.addElement(1,wrapper.wrap(self.initialRespone))
        if self.hostName is not None:
            list.addElement(2, wrapper.wrap(self.hostName))

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x41))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        unwrapper = AMQPUnwrapper()
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size == 0:
                raise ValueError("Received malformed SASL-Init header: mechanism can't be null")
            if size > 3:
                raise ValueError('Received malformed SASL-Init header. Invalid number of arguments: ' + str(size))
            if size > 0:
                element = list.getList()[0]
                if element is None or element.isNull():
                    raise ValueError("Received malformed SASL-Init header: mechanism can't be null")
                self.mechanism = unwrapper.unwrapSymbol(element)
            if size > 1:
                element = list.getList()[1]
                if element is not None and not element.isNull():
                    self.initialRespone = unwrapper.unwrapBinary(element)
            if size > 2:
                element = list.getList()[2]
                if element is not None and not element.isNull():
                    self.hostName = unwrapper.unwrapString(element)

    def toString(self):
        return "SASLInit [mechanism=" + str(self.mechanism) + ", initialResponse=" + str(self.initialResponse) + ", hostName=" + str(self.hostName) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setMechanism(self, mechanism):
        self.mechanism = mechanism

    def getMechanism(self):
        return self.mechanism

    def setInitialResponse(self, initialResponse):
        self.initialResponse = initialResponse

    def getInitialResponse(self):
        return self.initialResponse

    def setHostName(self, hostName):
        self.hostName = hostName

    def getHostName(self):
        return self.hostName
