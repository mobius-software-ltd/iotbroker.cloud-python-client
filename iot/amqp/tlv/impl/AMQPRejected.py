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
from iot.amqp.avps.ErrorCode import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.header.api.Parsable import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.AMQPError import *
from iot.amqp.tlv.impl.TLVList import *
from iot.amqp.tlv.impl.TLVFixed import *

class AMQPRejected(Parsable):
    def __init__(self, error):
        self.error = error

    def toArgumentsList(self):
        list = TLVList(None,None)
        if self.error is not None and isinstance(self.error, AMQPError):
            list.addElement(0, self.error.toArgumentsList())

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x25))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None and isinstance(element, TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError('Expected type Error received ' + str(element.getCode()))
                    self.error = AMQPError(None, None, None)
                    self.error.fromArgumentsList(element)

    def toString(self):
        return 'AMQPRejected [error='+ str(self.error) + ']'

    def getError(self):
        return self.error

    def setError(self, error):
        self.error = error