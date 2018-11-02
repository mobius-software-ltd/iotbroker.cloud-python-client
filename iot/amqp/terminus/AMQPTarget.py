from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.DistributionMode import *
from venv.iot.amqp.avps.TerminusDurability import *
from venv.iot.amqp.avps.TerminusExpiryPolicy import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.Parsable import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.wrappers.AMQPSymbol import *
from venv.iot.amqp.tlv.impl.AMQPOutcome import *

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

        if self.address is not None:
            list.addElement(0, AMQPWrapper.wrap(self.address))
        if self.durable is not None and isinstance(self.durable,TerminusDurability):
            list.addElement(1, AMQPWrapper.wrap(self.durable.value))
        if self.expiryPeriod is not None and isinstance(self.expiryPeriod, TerminusExpiryPolicy):
            list.addElement(2, AMQPWrapper.wrap(AMQPSymbol(self.expiryPeriod.value)))
        if self.timeout is not None:
            list.addElement(3, AMQPWrapper.wrap(self.timeout))
        if self.dynamic is not None:
            list.addElement(4, AMQPWrapper.wrap(self.dynamic))

        if self.dynamicNodeProperties is not None and isinstance(self.dynamicNodeProperties,dict):
            if self.dynamic is not None:
                if self.dynamic:
                    list.addElement(5, AMQPWrapper.wrapMap(self.dynamicNodeProperties))
                else:
                    raise ValueError("Target's dynamic-node-properties can't be specified when dynamic flag is false")
            else:
                raise ValueError("STarget's dynamic-node-properties can't be specified when dynamic flag is not set")

        if self.capabilities is not None and len(self.capabilities) > 0:
            list.addElement(6, AMQPWrapper.wrapArray(self.capabilities))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x29))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None:
                    self.address = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 1 :
                element = list.getList()[1]
                if element is not None:
                    self.durable = TerminusDurability(AMQPUnwrapper.unwrapInt(element))
            if len(list.getList()) > 2 :
                element = list.getList()[2]
                if element is not None:
                    self.expiryPeriod = TerminusExpiryPolicy(AMQPUnwrapper.unwrapSymbol(element))
            if len(list.getList()) > 3 :
                element = list.getList()[3]
                if element is not None:
                    self.timeout = AMQPUnwrapper.unwrapUInt(element)
            if len(list.getList()) > 4 :
                element = list.getList()[4]
                if element is not None:
                    self.dynamic = AMQPUnwrapper.unwrapBool(element)
            if len(list.getList()) > 5 :
                element = list.getList()[5]
                if element is not None:
                    if self.dynamic is not None:
                        self.dynamicNodeProperties = AMQPUnwrapper.unwrapMap(element)
                    else:
                        raise ValueError("Received malformed Target: dynamic-node-properties can't be specified when dynamic flag is false")
                else:
                    raise ValueError("Received malformed Target: dynamic-node-properties can't be specified when dynamic flag is not set")
            if len(list.getList()) > 6:
                element = list.getList()[6]
                if element is not None:
                    self.capabilities = AMQPUnwrapper.unwrapArray(element)

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
