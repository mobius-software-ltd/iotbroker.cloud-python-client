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
from iot.amqp.constructor.SimpleConstructor import *
from iot.amqp.avps.AMQPType import *
import abc

class TLVAmqp(metaclass=abc.ABCMeta):
    def __init__(self, constructor):
        self.constructor = constructor

    @abc.abstractmethod
    def getConstructor(self):
        return self.constructor

    @abc.abstractmethod
    def setConstructor(self, arg):
        self.constructor = arg

    @abc.abstractmethod
    def getCode(self):
        if isinstance(self.constructor, SimpleConstructor):
            return self.constructor.getCode()

    @abc.abstractmethod
    def setCode(self, arg):
        if isinstance(self.constructor, SimpleConstructor):
            self.constructor.setCode(arg)

    @abc.abstractmethod
    def getBytes(self):
        pass

    @abc.abstractmethod
    def getLength(self):
        pass

    @abc.abstractmethod
    def getValue(self):
        pass

    @abc.abstractmethod
    def isNull(self):
        if isinstance(self.constructor, SimpleConstructor):
            if self.constructor.getCode() == AMQPType.NULL:
                return True
            else:
                return False
