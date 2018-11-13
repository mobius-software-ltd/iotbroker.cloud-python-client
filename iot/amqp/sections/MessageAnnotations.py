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
from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *

class MessageAnnotations(AMQPSection):
    def __init__(self, annotations):
        self.annotations = annotations

    def getValue(self):
        map = TLVMap(None, None)

        if self.annotations is not None and len(self.annotations) > 0:
            map = AMQPWrapper.wrapMap(self.annotations)

        constructor = DescribedConstructor(map.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x72))
        map.setConstructor(constructor)
        return map

    def fill(self, map):
        if map is not None:
            self.annotations = AMQPUnwrapper.unwrapMap(map)

    def getCode(self):
        return SectionCode.MESSAGE_ANNOTATIONS

    def toString(self):
        return 'MessageAnnotations [annotations=' + str(self.annotations) + ']'

    def getAnnotations(self):
        return self.annotations

    def setAnnotations(self, annotations):
        self.annotations = annotations

