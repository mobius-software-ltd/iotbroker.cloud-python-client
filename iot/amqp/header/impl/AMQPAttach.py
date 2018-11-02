from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.avps.ReceiveCode import *
from venv.iot.amqp.avps.RoleCode import *
from venv.iot.amqp.avps.SendCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.terminus.AMQPSource import *
from venv.iot.amqp.terminus.AMQPTarget import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.wrappers.AMQPSymbol import *

class AMQPAttach(AMQPHeader):
    def __init__(self,code,doff,type,channel,name,handle,role,sndSettleMode,rcvSettleMode,source,target,unsettled,incompleteUnsettled,initialDeliveryCount,maxMessageSize,offeredCapabilities,desiredCapabilities,properties):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.ATTACH
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

        self.name = name
        self.handle = handle
        self.role = role
        self.sndSettleMode = sndSettleMode
        self.rcvSettleMode = rcvSettleMode
        self.source = source
        self.target = target
        self.unsettled = unsettled
        self.incompleteUnsettled = incompleteUnsettled
        self.initialDeliveryCount = initialDeliveryCount
        self.maxMessageSize = maxMessageSize
        self.offeredCapabilities = offeredCapabilities
        self.desiredCapabilities = desiredCapabilities
        self.properties = properties

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.name is None:
            raise ValueError("Attach header's name can't be null")
        list.addElement(0, AMQPWrapper.wrapString(self.name))
        if self.handle is None:
            raise ValueError("Attach header's handle can't be null")
        list.addElement(1, AMQPWrapper.wrap(self.handle))
        if self.role is None:
            raise ValueError("Attach header's role can't be null")
        if isinstance(self.role,RoleCode):
            list.addElement(2, AMQPWrapper.wrap(self.role.value))
        if self.sndSettleMode is not None and isinstance(self.sndSettleMode,SendCode):
            list.addElement(3, AMQPWrapper.wrap(self.sndSettleMode.value))
        if self.rcvSettleMode is not None and isinstance(self.rcvSettleMode,ReceiveCode):
            list.addElement(4, AMQPWrapper.wrap(self.rcvSettleMode.value))
        if self.source is not None and isinstance(self.source,AMQPSource):
            list.addElement(5,self.source.toArgumentsList())
        if self.target is not None and isinstance(self.target,AMQPTarget):
            list.addElement(6,self.target.toArgumentsList())
        if self.unsettled is not None and len(self.unsettled) > 0:
            list.addElement(7, AMQPWrapper.wrapMap(self.unsettled))
        if self.incompleteUnsettled is not None:
            list.addElement(8,AMQPWrapper.wrap(self.incompleteUnsettled))
        if self.initialDeliveryCount is not None:
            list.addElement(9,AMQPWrapper.wrap(self.initialDeliveryCount))
        elif self.role == RoleCode.SENDER:
            raise ValueError("Sender's attach header must contain a non-null initial-delivery-count value")
        if self.maxMessageSize is not None:
            list.addElement(10,AMQPWrapper.wrap(self.maxMessageSize))
        if self.offeredCapabilities is not None and len(self.offeredCapabilities) > 0:
            list.addElement(11, AMQPWrapper.wrapArray(self.offeredCapabilities))
        if self.desiredCapabilities is not None and len(self.desiredCapabilities) > 0:
            list.addElement(12, AMQPWrapper.wrapArray(self.desiredCapabilities))
        if self.properties is not None and len(self.properties) > 0:
            list.addElement(13, AMQPWrapper.wrapMap(self.properties))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size < 3:
                raise ValueError('Received malformed Attach header: mandatory fields name, handle and role must not be null')
            if size > 14:
                raise ValueError('Received malformed Attach header. Invalid number of arguments: ' + str(size))

            if size > 0:
                element = list.getList()[0]
                if element is not None:
                    self.name = AMQPUnwrapper.unwrapString(element)
                else:
                    raise ValueError("Received malformed Attach header: name can't be null")
            if size > 1:
                element = list.getList()[1]
                if element is not None:
                    self.handle = AMQPUnwrapper.unwrapUInt(element)
                else:
                    raise ValueError("Received malformed Attach header: handle can't be null")
            if size > 2:
                element = list.getList()[2]
                if element is not None:
                    self.role = RoleCode(AMQPUnwrapper.unwrapBool(element))
                else:
                    raise ValueError("Received malformed Attach header: role can't be null")
            if size > 3:
                element = list.getList()[3]
                if element is not None:
                    self.sndSettleMode = SendCode(AMQPUnwrapper.unwrapUByte(element))
            if size > 4:
                element = list.getList()[4]
                if element is not None:
                    self.rcvSettleMode = ReceiveCode(AMQPUnwrapper.unwrapUByte(element))
            if size > 5:
                element = list.getList()[5]
                if element is not None and isinstance(element,TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError('Expected type SOURCE - received: ' + str(element.getCode()))
                    self.source = AMQPSource(None,None,None,None,None,None,None,None,None,None,None)
                    self.source.fromArgumentsList(element)
            if size > 6:
                element = list.getList()[6]
                if element is not None and isinstance(element, TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0, AMQPType.LIST_8, AMQPType.LIST_32):
                        raise ValueError('Expected type TARGET - received: ' + str(element.getCode()))
                    self.target = AMQPTarget(None, None, None, None, None, None, None)
                    self.target.fromArgumentsList(element)
            if size > 7:
                element = list.getList()[7]
                if element is not None:
                    self.unsettled = AMQPUnwrapper.unwrapMap(element)
            if size > 8:
                element = list.getList()[8]
                if element is not None:
                    self.incompleteUnsettled = AMQPUnwrapper.unwrapBool(element)
            if size > 9:
                element = list.getList()[9]
                if element is not None:
                    self.initialDeliveryCount = AMQPUnwrapper.unwrapUInt(element)
                elif self.role == RoleCode.SENDER:
                    raise ValueError('Received an attach header with a null initial-delivery-count')
            if size > 10:
                element = list.getList()[10]
                if element is not None:
                    self.maxMessageSize = AMQPUnwrapper.unwrapULong(element)
            if size > 11:
                element = list.getList()[11]
                if element is not None:
                    self.offeredCapabilities = AMQPUnwrapper.unwrapArray(element)
            if size > 12:
                element = list.getList()[12]
                if element is not None:
                    self.desiredCapabilities = AMQPUnwrapper.unwrapArray(element)
            if size > 13:
                element = list.getList()[12]
                if element is not None:
                    self.properties = AMQPUnwrapper.unwrapMap(element)

    def toString(self):
        return "AMQPAttach [name=" + str(self.name) + ", handle=" + str(self.handle) + ", role=" + str(self.role) + ", sndSettleMode=" + str(self.sndSettleMode) + ", rcvSettleMode=" + str(self.rcvSettleMode) + ", source=" + str(self.source) + ", target=" + str(self.target) + ", unsettled=" + str(self.unsettled) + ", incompleteUnsettled=" + str(self.incompleteUnsettled) + ", initialDeliveryCount=" + str(self.initialDeliveryCount) + ", maxMessageSize=" + str(self.maxMessageSize) + ", offeredCapabilities=" + str(self.offeredCapabilities) + ", desiredCapabilities=" + str(self.desiredCapabilities) + ", properties=" + str(self.properties) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setHandle(self, handle):
        self.handle = handle

    def getHandle(self):
        return self.handle

    def setRole(self, role):
        self.role = role

    def getRole(self):
        return self.role

    def setSndSettleMode(self, sndSettleMode):
        self.sndSettleMode = sndSettleMode

    def getSndSettleMode(self):
        return self.sndSettleMode

    def setRcvSettleMode(self, rcvSettleMode):
        self.rcvSettleMode = rcvSettleMode

    def getRcvSettleMode(self):
        return self.rcvSettleMode

    def setSource(self, source):
        self.source = source

    def getSource(self):
        return self.source

    def setTarget(self, target):
        self.target = target

    def getTarget(self):
        return self.target

    def setUnsettled(self, unsettled):
        self.unsettled = unsettled

    def getUnsettled(self):
        return self.unsettled

    def setIncompleteUnsettled(self, incompleteUnsettled):
        self.incompleteUnsettled = incompleteUnsettled

    def getIncompleteUnsettled(self):
        return self.incompleteUnsettled

    def setInitialDeliveryCount(self, initialDeliveryCount):
        self.initialDeliveryCount = initialDeliveryCount

    def getInitialDeliveryCount(self):
        return self.initialDeliveryCount

    def setMaxMessageSize(self, maxMessageSize):
        self.maxMessageSize = maxMessageSize

    def getMaxMessageSize(self):
        return self.maxMessageSize

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




