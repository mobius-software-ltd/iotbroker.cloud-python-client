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
from venv.iot.mqttsn.mqttsn_classes.Radius import *

class Controls():
    def __init__(self, radius):
        self.radius = Radius(radius)

    def getRadius(self):
        return self.radius

    def setRadius(self, radius):
        self.radius = radius

    def encode(self):
        ctrByte = 0
        ctrByte |= self.radius
        return ctrByte

    def decode(self, ctrByte):
        if(ctrByte > 3 or ctrByte <0):
            raise ValueError('Invalid Encapsulated message control encoding: ' + ctrByte)
        return Controls(ctrByte)