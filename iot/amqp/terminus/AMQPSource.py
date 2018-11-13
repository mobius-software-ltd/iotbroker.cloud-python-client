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
from venv.iot.amqp.avps.DistributionMode import *
from venv.iot.amqp.avps.TerminusDurability import *
from venv.iot.amqp.avps.TerminusExpiryPolicy import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.HeaderFactoryOutcome import *
from venv.iot.amqp.header.api.Parsable import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.wrappers.AMQPSymbol import *
from venv.iot.amqp.tlv.impl.AMQPOutcome import *

class AMQPSource(Parsable):
    def __init__(self,address,durable,expiryPeriod,timeout,dynamic,dynamicNodeProperties,distributionMode,filter,defaultOutcome,outcomes,capabilities):
        self.address = address
        self.durable = durable
        self.expiryPeriod = expiryPeriod
        self.timeout = timeout
        self.dynamic = dynamic
        self.dynamicNodeProperties = dynamicNodeProperties
        self.distributionMode = distributionMode
        self.filter = filter
        self.defaultOutcome = defaultOutcome
        self.outcomes = outcomes
        self.capabilities = capabilities
        self.index = 0

    def toArgumentsList(self):
        list = TLVList(None,None)
        wrapper = AMQPWrapper()
        if self.address is not None:
            list.addElement(0, wrapper.wrap(self.address))
        if self.durable is not None:
            list.addElement(1, wrapper.wrap(self.durable))
        if self.expiryPeriod is not None:
            list.addElement(2, wrapper.wrap(AMQPSymbol(self.expiryPeriod.value)))
        if self.timeout is not None:
            list.addElement(3, wrapper.wrap(self.timeout))
        if self.dynamic is not None:
            list.addElement(4, wrapper.wrap(self.dynamic))
        if self.dynamicNodeProperties is not None and isinstance(self.dynamicNodeProperties,dict):
            if self.dynamic is not None:
                if self.dynamic:
                    list.addElement(5, wrapper.wrapMap(self.dynamicNodeProperties))
                else:
                    raise ValueError("Source's dynamic-node-properties can't be specified when dynamic flag is false")
            else:
                raise ValueError("Source's dynamic-node-properties can't be specified when dynamic flag is not set")

        if self.distributionMode is not None and isinstance(self.distributionMode,DistributionMode):
            list.addElement(6, wrapper.wrap(AMQPSymbol(self.distributionMode.value)))
        if self.filter is not None and isinstance(self.filter, dict):
            list.addElement(7, wrapper.wrapMap(self.filter))
        if self.defaultOutcome is not None and isinstance(self.defaultOutcome,AMQPOutcome):
            list.addElement(8, self.defaultOutcome.toArgumentsList())
        if self.outcomes is not None and len(self.outcomes) > 0:
            list.addElement(9, wrapper.wrapArray(self.outcomes))
        if self.capabilities is not None and len(self.capabilities) > 0:
            list.addElement(10, wrapper.wrapArray(self.capabilities))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x28))
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
                        if self.dynamic:
                            self.dynamicNodeProperties = unwrapper.unwrapMap(element)
                        else:
                            raise ValueError("Received malformed Source: dynamic-node-properties can't be specified when dynamic flag is false")
                    else:
                        raise ValueError("Received malformed Source: dynamic-node-properties can't be specified when dynamic flag is not set")

            if len(list.getList()) > 6 :
                element = list.getList()[6]
                if element is not None and not element.isNull():
                    self.distributionMode = DistributionMode(unwrapper.unwrapSymbol(element))
            if len(list.getList()) > 7:
                element = list.getList()[7]
                if element is not None and not element.isNull():
                    self.filter = unwrapper.unwrapMap(element)

            if len(list.getList()) > 8:
                element = list.getList()[8]
                if element is not None and not element.isNull() and isinstance(element,TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError('Expected type OUTCOME - received: ' + element.getCode())


                self.defaultOutcome = HeaderFactoryOutcome.getOutcome(element)
                self.defaultOutcome.fromArgumentsList(element)

            if len(list.getList()) > 9:
                element = list.getList()[9]
                if element is not None and not element.isNull():
                    self.outcomes = unwrapper.unwrapArray(element)
            if len(list.getList()) > 10:
                element = list.getList()[10]
                if element is not None and not element.isNull():
                    self.capabilities = unwrapper.unwrapArray(element)

    def toString(self):
        return 'AMQPSource [address=' + str(self.address) + ', durable=' + str(self.durable) + ', expiryPeriod=' + str(self.expiryPeriod) + ', timeout=' + str(self.timeout) + ', dynamic=' + str(self.dynamic) + ', dynamicNodeProperties=' + str(self.dynamicNodeProperties) + ', distributionMode=' + str(self.distributionMode) + ', filter=' + str(self.filter) + ', defaultOutcome=' + str(self.defaultOutcome) + ', outcomes=' + str(self.outcomes) + ', capabilities=' + str(self.capabilities) + ']'

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

    def getDistributionMode(self):
        return self.distributionMode

    def setDistributionMode(self, distributionMode):
        self.distributionMode = distributionMode

    def getFilter(self):
        return self.filter

    def setFilter(self, filter):
        self.filter = filter

    def getDefaultOutcome(self):
        return self.defaultOutcome

    def setDefaultOutcome(self, defaultOutcome):
        self.defaultOutcome = defaultOutcome

    def getOutcomes(self):
        return self.outcomes

    def setOutcomes(self, outcomes):
        self.outcomes = outcomes

    def getCapabilities(self):
        return self.capabilities

    def setCapabilities(self, capabilities):
        self.capabilities = capabilities
