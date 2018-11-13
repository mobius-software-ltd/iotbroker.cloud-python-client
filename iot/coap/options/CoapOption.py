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
class CoapOption(object):
    def __init__(self, type, length, value):
        self.type = type
        self.length = length
        self.value = value

    def equals(self, obj):
        if self == obj:
            return True
        return False

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value