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
from iot.amqp.avps.DistributionMode import *
from iot.amqp.avps.TerminusDurability import *
from iot.amqp.avps.TerminusExpiryPolicy import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.header.api.Parsable import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.wrappers.AMQPSymbol import *
from iot.amqp.tlv.impl.AMQPOutcome import *

class AMQPTarget(Parsable):
    def __init__(self,address,durable,expiryPeriod,timeout,dynamic,dynamicNodeProperties,capabilities):
        self.address = address
        self.durable = durable
        self.expiryPeriod = expiryPeriod
        self.timeout = timeout
        self.dynamic = dynamic
        self.dynamicNodeProperties = dynamicNodeProperties
        self.capabilities = capabilities

    def toArgumentsList(self):
        list = TLVList(None,None)
        wrapper = AMQPWrapper()
        if self.address is not None:
            list.addElement(0, wrapper.wrap(self.address))

        if self.durable is not None:
            list.addElement(1, wrapper.wrap(self.durable))
        if self.expiryPeriod is not None:
            list.addElement(2, wrapper.wrap(self.expiryPeriod))
        if self.timeout is not None:
            result = wrapper.wrap(self.timeout)
            list.addElement(3, result)
        if self.dynamic is not None:
            list.addElement(4, wrapper.wrap(self.dynamic))
        if self.dynamicNodeProperties is not None:
            if self.dynamic is not None:
                if self.dynamic:
                    list.addElement(5, wrapper.wrapMap(self.dynamicNodeProperties))
                else:
                    raise ValueError("Target's dynamic-node-properties can't be specified when dynamic flag is false")
            else:
                raise ValueError("STarget's dynamic-node-properties can't be specified when dynamic flag is not set")

        if self.capabilities is not None and len(self.capabilities) > 0:
            list.addElement(6, wrapper.wrapArray(self.capabilities))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x29))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        unwrapper = AMQPUnwrapper()
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None and not element.isNull():
                    self.address = unwrapper.unwrapString(element)
            if len(list.getList()) > 1 :
                element = list.getList()[1]
                if element is not None and not element.isNull():
                    self.durable = TerminusDurability(unwrapper.unwrapUInt(element))
            if len(list.getList()) > 2 :
                element = list.getList()[2]
                if element is not None and not element.isNull():
                    self.expiryPeriod = TerminusExpiryPolicy(unwrapper.unwrapSymbol(element))
            if len(list.getList()) > 3 :
                element = list.getList()[3]
                if element is not None and not element.isNull():
                    self.timeout = unwrapper.unwrapUInt(element)
            if len(list.getList()) > 4 :
                element = list.getList()[4]
                if element is not None and not element.isNull():
                    self.dynamic = unwrapper.unwrapBool(element)
            if len(list.getList()) > 5 :
                element = list.getList()[5]
                if element is not None and not element.isNull():
                    if self.dynamic is not None:
                        self.dynamicNodeProperties = unwrapper.unwrapMap(element)
                    else:
                        raise ValueError("Received malformed Target: dynamic-node-properties can't be specified when dynamic flag is false")
                else:
                    raise ValueError("Received malformed Target: dynamic-node-properties can't be specified when dynamic flag is not set")
            if len(list.getList()) > 6:
                element = list.getList()[6]
                if element is not None and not element.isNull():
                    self.capabilities = unwrapper.unwrapArray(element)

    def toString(self):
        return 'AMQPTarget [address=' + str(self.address) + ', durable=' + str(self.durable) + ', expiryPeriod=' + str(self.expiryPeriod) + ', timeout=' + str(self.timeout) + ', dynamic=' + str(self.dynamic) + ', dynamicNodeProperties=' + str(self.dynamicNodeProperties) + ', capabilities=' + str(self.capabilities) + ']'

    def getAddress(self):
        return self.address

    def setAddress(self, address):
        self.address = address

    def getDurable(self):
        return self.durable

    def setDurable(self, durable):
        self.durable = durable

    def getExpiryPeriod(self):
        return self.expiryPeriod

    def setExpiryPeriod(self, expiryPeriod):
        self.expiryPeriod = expiryPeriod

    def getTimeout(self):
        return self.timeout

    def setTimeout(self, timeout):
        self.timeout = timeout

    def getDynamic(self):
        return self.dynamic

    def setDynamic(self, dynamic):
        self.dynamic = dynamic

    def getDynamicNodeProperties(self):
        return self.dynamicNodeProperties

    def setDynamicNodeProperties(self, dynamicNodeProperties):
        self.dynamicNodeProperties = dynamicNodeProperties

    def getCapabilities(self):
        return self.capabilities

    def setCapabilities(self, capabilities):
        self.capabilities = capabilities
