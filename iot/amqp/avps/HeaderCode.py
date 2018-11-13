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

class HeaderCode(Enum):
    OPEN        = 0x10  #16
    BEGIN       = 0x11  #17
    ATTACH      = 0x12  #18
    FLOW        = 0x13  #19
    TRANSFER    = 0x14  #20
    DISPOSITION = 0x15  #21
    DETACH      = 0x16  #22
    END         = 0x17  #23
    CLOSE       = 0x18  #24
    MECHANISMS  = 0x40  #64
    INIT        = 0x41  #65
    CHALLENGE   = 0x42  #66
    RESPONSE    = 0x43  #67
    OUTCOME     = 0x44  #68
    PING        = 0xff  #255
    PROTO       = 0xfe  #254