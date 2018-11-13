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
from venv.iot.amqp.avps.RoleCode import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.HeaderFactoryOutcome import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVNull import *
from venv.iot.amqp.tlv.impl.AMQPState import *

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
        wrapper = AMQPWrapper()
        if self.role is None:
            raise ValueError("Disposition header's role can't be null")
        if isinstance(self.role, RoleCode):
            list.addElement(0, wrapper.wrap(self.role.value))
        if self.first is None:
            raise ValueError("Disposition header's first can't be null")
        list.addElement(1, wrapper.wrap(self.first))
        if self.last is not None:
            list.addElement(2, wrapper.wrap(self.last))
        if self.settled is not None:
            list.addElement(3, wrapper.wrap(self.settled))
        if self.state is not None:
            if isinstance(self.state, AMQPState):
                list.addElement(4, self.state.toArgumentsList())
        if self.batchable is not None and len(self.outgoingLocales) > 0:
            list.addElement(5, wrapper.wrap(self.batchable))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        unwrapper = AMQPUnwrapper()
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size  < 2:
                raise ValueError("Received malformed Disposition header: role and first can't be null")
            if size > 6:
                raise ValueError("Received malformed Disposition header. Invalid number of arguments: " + str(size))

            if size > 0:
                element = list.getList()[0]
                if element is None and not element.isNull():
                    raise ValueError("Received malformed Disposition header: role can't be null")
                self.role = unwrapper.unwrapBool(element)
            if size > 1:
                element = list.getList()[1]
                if element is None and not element.isNull():
                    raise ValueError("Received malformed Disposition header: first can't be null")
                self.first = unwrapper.unwrapUInt(element)
            if size > 2:
                element = list.getList()[2]
                if element is not None and not element.isNull():
                    self.last = unwrapper.unwrapUInt(element)
            if size > 3:
                element = list.getList()[3]
                if element is not None and not element.isNull():
                    self.settled = unwrapper.unwrapBool(element)
            if size > 4:
                element = list.getList()[4]
                if element is not None and not element.isNull() and isinstance(element,TLVAmqp):
                    code  = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError('Expected type STATE - received: ' + str(element.getCode()))
                    self.state = HeaderFactoryOutcome.getState(element)
                    self.state.fromArgumentsList(element)
            if size > 5:
                element = list.getList()[5]
                if element is not None and not element.isNull():
                    self.batchable = unwrapper.unwrapBool(element)

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