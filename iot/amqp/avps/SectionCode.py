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
from enum import Enum

class SectionCode(Enum):
    HEADER                  = 0x70
    DELIVERY_ANNOTATIONS    = 0x71
    MESSAGE_ANNOTATIONS     = 0x72
    PROPERTIES              = 0x73
    APPLICATION_PROPERTIES  = 0x74
    DATA                    = 0x75
    SEQUENCE                = 0x76
    VALUE                   = 0x77
    FOOTER                  = 0x78
