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
from iot.amqp.sections.AMQPSection import *
from iot.amqp.header.api.AMQPWrapper import *
from iot.amqp.header.api.AMQPUnwrapper import *
from iot.amqp.constructor.DescribedConstructor import *
from iot.amqp.avps.SectionCode import *

class ApplicationProperties(AMQPSection):
    def __init__(self, properties):
        self.properties = properties

    def getValue(self):
        map = TLVMap(None, None)

        if self.properties is not None and len(self.properties) > 0:
            map = AMQPWrapper.wrapMap(self.properties)

        constructor = DescribedConstructor(map.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x74))
        map.setConstructor(constructor)
        return map

    def fill(self, map):
        if map is not None:
            self.annotations = AMQPUnwrapper.unwrapMap(map)

    def getCode(self):
        return SectionCode.APPLICATION_PROPERTIES

    def toString(self):
        return 'ApplicationProperties [properties=' + str(self.properties) + ']'

    def getProperties(self):
        return self.properties

    def setProperties(self, properties):
        self.properties = properties

