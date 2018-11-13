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
from venv.iot.amqp.avps.ErrorCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.Parsable import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.wrappers.AMQPSymbol import *

class AMQPError(Parsable):
    def __init__(self, condition, description, info):
        self.condition = condition
        self.description = description
        self.info = info

    def toArgumentsList(self):
        wrapper = AMQPWrapper()
        list = TLVList(None,None)
        if self.condition is not None and isinstance(self.condition, ErrorCode):
            list.addElement(0, wrapper.wrap(AMQPSymbol(self.condition)))
        if self.description is not None:
            list.addElement(1, wrapper.wrap(self.description))
        if self.info is not None:
            list.addElement(2, wrapper.wrap(self.info))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x1D))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        unwrapper = AMQPUnwrapper()
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None:
                    self.condition = ErrorCode(unwrapper.unwrapSymbol(element).getValue())
                    print('AMQPError ERROR OCCURED condition= ' + str(ErrorCode(unwrapper.unwrapSymbol(element).getValue())))
            if len(list.getList()) > 1 :
                element = list.getList()[1]
                if element is not None:
                    self.description = unwrapper.unwrapString(element)
            if len(list.getList()) > 2 :
                element = list.getList()[2]
                if element is not None:
                    self.info = unwrapper.unwrapMap(element)

    def toString(self):
        return 'AMQPError [condition='+ str(self.condition) + ', description=' + str(self.description) + ', info=' + str(self.info) + ']'

    def getCondition(self):
        return self.condition

    def setCondition(self, condition):
        self.condition = condition

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getInfo(self):
        return self.info

    def setInfo(self, info):
        self.info = info