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
from iot.amqp.avps.LifetimePolicy import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.tlv.impl.TLVList import *
from iot.amqp.tlv.impl.TLVFixed import *

class AMQPLifetimePolicy(object):
    def __init__(self, code):
        self.code = code

    def getList(self):
        list = TLVList(None, None)
        if isinstance(self.code, LifetimePolicy):
            constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
            list.setConstructor(constructor)
        return list

    def fill(self,list):
        if list is not None and isinstance(list, TLVList):
            constructor = list.getConstructor()
            self.code = LifetimePolicy(constructor.getDescriptorCode() & 0xff).value

    def getCode(self):
        return self.code