from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.HeaderFactory import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVNull import *

class AMQPDisposition(AMQPHeader):
    def __init__(self,code,doff,type,channel,role,first,last,settled,state,batchable):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.DISPOSITION
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
        self.role = role
        self.first = first
        self.last = last
        self.settled = settled
        self.state = state
        self.batchable = batchable

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.role is None:
            raise ValueError("Disposition header's role can't be null")
        if isinstance(self.role, RoleCode):
            list.addElement(0, AMQPWrapper.wrap(self.role.value))
        if self.first is None:
            raise ValueError("Disposition header's first can't be null")
        list.addElement(1, AMQPWrapper.wrap(self.first))
        if self.last is not None:
            list.addElement(2, AMQPWrapper.wrap(self.last))
        if self.settled is not None:
            list.addElement(3, AMQPWrapper.wrap(self.settled))
        if self.state is not None:
            list.addElement(4, AMQPWrapper.wrap(self.state))
        if self.batchable is not None and len(self.outgoingLocales) > 0:
            list.addElement(5, AMQPWrapper.wrapArray(self.batchable))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size  < 2:
                raise ValueError("Received malformed Disposition header: role and first can't be null")
            if size > 6:
                raise ValueError("Received malformed Disposition header. Invalid number of arguments: " + str(size))

            if size > 0:
                element = list.getList()[0]
                if element is None:
                    raise ValueError("Received malformed Disposition header: role can't be null")
                self.role = AMQPUnwrapper.unwrapBool(element)
            if size > 1:
                element = list.getList()[1]
                if element is None:
                    raise ValueError("Received malformed Disposition header: first can't be null")
                self.first = AMQPUnwrapper.unwrapUInt(element)
            if size > 2:
                element = list.getList()[2]
                if element is not None:
                    self.last = AMQPUnwrapper.unwrapUInt(element)
            if size > 3:
                element = list.getList()[3]
                if element is not None:
                    self.settled = AMQPUnwrapper.unwrapBool(element)
            if size > 4:
                element = list.getList()[4]
                if element is not None and isinstance(element,TLVAmqp):
                    code  = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError('Expected type STATE - received: ' + str(element.getCode()))
                    self.state = HeaderFactory.getState(element)
                    self.state.fromArgumentsList(element)
            if size > 5:
                element = list.getList()[5]
                if element is not None:
                    self.batchable = AMQPUnwrapper.unwrapBool(element)

    def toString(self):
        return "AMQPDisposition [role=" + str(self.role) + ", first=" + str(self.first) + ", last=" + str(self.last) + ", settled=" + str(self.settled) + ", state=" + str(self.state) + ", batchable=" + str(self.batchable) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setRole(self, role):
        self.role = role

    def getRole(self):
        return self.role

    def setFirst(self, first):
        self.first = first

    def getFirst(self):
        return self.first

    def setLast(self, last):
        self.last = last

    def getLast(self):
        return self.last

    def setSettled(self, settled):
        self.settled = settled

    def getSettled(self):
        return self.settled

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setBatchable(self, batchable):
        self.batchable = batchable

    def getBatchable(self):
        return self.batchable