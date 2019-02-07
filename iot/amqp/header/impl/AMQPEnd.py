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
from iot.amqp.avps.HeaderCode import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.header.api.AMQPHeader import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.tlv.api.TLVAmqp import *
from iot.amqp.tlv.impl.TLVFixed import *
from iot.amqp.tlv.impl.TLVList import *
from iot.amqp.tlv.impl.TLVNull import *
from iot.amqp.tlv.impl.AMQPError import *

class AMQPEnd(AMQPHeader):
    def __init__(self,code,doff,type,channel,error):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.END
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
        self.error = error

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.error is not None and isinstance(self.error,AMQPError):
            list.addElement(0, self.error.toArgumentsList())
        else:
            list.addElement(0, TLVNull())

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            #print('list.getList()= ' + str(list.getList()))
            if size > 0:
                element = list.getList()[0]
                if element is not None and isinstance(element,TLVAmqp) and isinstance(element,TLVNull) != True:
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError("Expected type 'ERROR' - received: " + str(element.getCode()))
                    self.error = AMQPError(None,None,None)
                    self.error.fromArgumentsList(element)

    def toString(self):
        return "AMQPEnd [error=" + str(self.error) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setError(self, error):
        self.error = error

    def getError(self):
        return self.error