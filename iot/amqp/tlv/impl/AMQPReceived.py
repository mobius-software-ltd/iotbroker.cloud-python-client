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

class AMQPReceived(Parsable):
    def __init__(self, sectionNumber, sectionOffset):
        self.sectionNumber = sectionNumber
        self.sectionOffset = sectionOffset

    def toArgumentsList(self):
        list = TLVList(None,None)
        if self.sectionNumber is not None:
            list.addElement(0, AMQPWrapper.wrap(self.sectionNumber))
        if self.sectionOffset is not None:
            list.addElement(1, AMQPWrapper.wrap(self.sectionOffset))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x23))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None:
                    self.sectionNumber = AMQPUnwrapper.unwrapUInt(element)
            if len(list.getList()) > 1 :
                element = list.getList()[1]
                if element is not None:
                    self.sectionOffset = AMQPUnwrapper.unwrapULong(element)

    def toString(self):
        return 'AMQPReceived [sectionNumber='+ str(self.sectionNumber) + ', sectionOffset=' + str(self.sectionOffset) + ']'

    def getSectionNumber(self):
        return self.sectionNumber

    def setSectionNumber(self, sectionNumber):
        self.sectionNumber = sectionNumber

    def getSectionOffset(self):
        return self.sectionOffset

    def setSectionOffset(self, sectionOffset):
        self.sectionOffset = sectionOffset