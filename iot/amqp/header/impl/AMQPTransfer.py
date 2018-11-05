from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.avps.ReceiveCode import *
from venv.iot.amqp.avps.SectionCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.HeaderFactory import *
from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.AMQPState import *
from venv.iot.amqp.wrappers.AMQPMessageFormat import *

class AMQPTransfer(AMQPHeader):
    def __init__(self,code,doff,type,channel,handle,deliveryId,deliveryTag,messageFormat,settled,more,rcvSettleMode,state,resume,aborted,batchable,sections):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.TRANSFER
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

        self.handle = handle
        self.deliveryId = deliveryId
        self.deliveryTag = deliveryTag
        self.messageFormat = messageFormat
        self.settled = settled
        self.more = more
        self.rcvSettleMode = rcvSettleMode
        self.state = state
        self.resume = resume
        self.aborted = aborted
        self.batchable = batchable
        self.sections = sections

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.handle == None:
            raise ValueError("Transfer header's handle can't be null")
        list.addElement(0,AMQPWrapper.wrap(self.handle))
        if self.deliveryId is not None:
            list.addElement(1, AMQPWrapper.wrap(self.deliveryId))
        if self.deliveryTag is not None:
            list.addElement(2, AMQPWrapper.wrap(self.deliveryTag))
        if self.messageFormat is not None and isinstance(self.messageFormat,AMQPMessageFormat):
            list.addElement(3, AMQPWrapper.wrap(self.messageFormat.encode()))
        if self.settled is not None:
            list.addElement(4, AMQPWrapper.wrap(self.settled))
        if self.more is not None:
            list.addElement(5, AMQPWrapper.wrap(self.more))
        if self.rcvSettleMode is not None and isinstance(self.rcvSettleMode,ReceiveCode):
            list.addElement(6, AMQPWrapper.wrap(self.rcvSettleMode.value))
        if self.state is not None and isinstance(self.state, AMQPState):
            list.addElement(7, AMQPWrapper.wrap(self.state.toArgumentsList()))
        if self.resume is not None:
            list.addElement(8, AMQPWrapper.wrap(self.resume))
        if self.aborted is not None:
            list.addElement(9, AMQPWrapper.wrap(self.aborted))
        if self.batchable is not None:
            list.addElement(10, AMQPWrapper.wrap(self.batchable))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size == 0:
                raise ValueError("Received malformed Transfer header: handle can't be null")
            if size > 11:
                raise ValueError('Received malformed Transfer header. Invalid number of arguments: ' + str(size))
            if size > 0:
                element = list.getList()[0]
                if element is None:
                    raise ValueError("Received malformed Transfer header: handle can't be null")
                self.handle = AMQPUnwrapper.unwrapUInt(element)
            if size > 1:
                element = list.getList()[1]
                if element is not None:
                    self.deliveryId = AMQPUnwrapper.unwrapUInt(element)
            if size > 2:
                element = list.getList()[2]
                if element is not None:
                    self.deliveryTag = AMQPUnwrapper.unwrapBinary(element)
            if size > 3:
                element = list.getList()[3]
                if element is not None:
                    self.messageFormat = AMQPMessageFormat(AMQPUnwrapper.unwrapUInt(element))
            if size > 4:
                element = list.getList()[4]
                if element is not None:
                    self.settled = AMQPUnwrapper.unwrapBool(element)
            if size > 5:
                element = list.getList()[5]
                if element is not None:
                    self.more = AMQPUnwrapper.unwrapBool(element)
            if size > 6:
                element = list.getList()[6]
                if element is not None:
                    self.rcvSettleMode = ReceiveCode(AMQPUnwrapper.unwrapUByte(element))
            if size > 7:
                element = list.getList()[7]
                if element is not None and isinstance(element,TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError("Expected type 'STATE' - received: " + str(element.getCode()))
                    self.state = HeaderFactory.getState(element)
                    self.state.fromArgumentsList(element)
            if size > 8:
                element = list.getList()[8]
                if element is not None:
                    self.resume = AMQPUnwrapper.unwrapBool(element)
            if size > 9:
                element = list.getList()[9]
                if element is not None:
                    self.aborted = AMQPUnwrapper.unwrapBool(element)
            if size > 10:
                element = list.getList()[10]
                if element is not None:
                    self.batchable = AMQPUnwrapper.unwrapBool(element)

    def toString(self):
        return "AMQPTransfer [handle=" + str(self.handle) + ", deliveryId=" + str(self.deliveryId) + ", deliveryTag=" + str(self.deliveryTag) + ", messageFormat=" + str(self.messageFormat) + ", settled=" + str(self.settled) + ", more=" + str(self.more) + ", rcvSettleMode=" + str(self.rcvSettleMode) + ", state=" + str(self.state) + ", resume=" + str(self.resume) + ", aborted=" + str(self.aborted) + ", batchable=" + str(self.batchable) + ", sections=" + str(self.sections) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setHandle(self, handle):
        self.handle = handle

    def getHandle(self):
        return self.handle

    def setDeliveryId(self, deliveryId):
        self.deliveryId = deliveryId

    def getDeliveryId(self):
        return self.deliveryId

    def setDeliveryTag(self, deliveryTag):
        self.deliveryTag = deliveryTag

    def getDeliveryTag(self):
        return self.deliveryTag

    def setMessageFormat(self, messageFormat):
        self.messageFormat = messageFormat

    def getMessageFormat(self):
        return self.messageFormat

    def setSettled(self, settled):
        self.settled = settled

    def getSettled(self):
        return self.settled

    def setMore(self, more):
        self.more = more

    def getMore(self):
        return self.more

    def setRcvSettleMode(self, rcvSettleMode):
        self.rcvSettleMode = rcvSettleMode

    def getRcvSettleMode(self):
        return self.rcvSettleMode

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setResume(self, resume):
        self.resume = resume

    def getResume(self):
        return self.resume

    def setAborted(self, aborted):
        self.aborted = aborted

    def getAborted(self):
        return self.aborted

    def setBatchable(self, batchable):
        self.batchable = batchable

    def getBatchable(self):
        return self.batchable

    def setSections(self, sections):
        self.sections = sections

    def getSections(self):
        return self.sections

    def getHeader(self):
        if self.sections is not None:
            return self.sections(SectionCode.HEADER)
        else:
            return None

    def getDeliveryAnnotations(self):
        if self.sections is not None:
            return self.sections(SectionCode.DELIVERY_ANNOTATIONS)
        else:
            return None

    def getMessageAnnotations(self):
        if self.sections is not None:
            return self.sections(SectionCode.MESSAGE_ANNOTATIONS)
        else:
            return None

    def getProperties(self):
        if self.sections is not None:
            return self.sections(SectionCode.PROPERTIES)
        else:
            return None

    def getApplicationProperties(self):
        if self.sections is not None:
            return self.sections(SectionCode.APPLICATION_PROPERTIES)
        else:
            return None

    def getData(self):
        if self.sections is not None:
            return self.sections(SectionCode.DATA)
        else:
            return None

    def getSequence(self):
        if self.sections is not None:
            return self.sections(SectionCode.SEQUENCE)
        else:
            return None

    def getValue(self):
        if self.sections is not None:
            return self.sections(SectionCode.VALUE)
        else:
            return None

    def getFooter(self):
        if self.sections is not None:
            return self.sections(SectionCode.FOOTER)
        else:
            return None