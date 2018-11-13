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

class AMQPType(Enum):
    SOURCE          = 0x28
    TARGET          = 0x29
    ERROR           = 0x1D
    NULL            = 0x40
    BOOLEAN         = 0x56
    BOOLEAN_TRUE    = 0x41
    BOOLEAN_FALSE   = 0x42
    UBYTE           = 0x50
    USHORT          = 0x60
    UINT            = 0x70
    SMALL_UINT      = 0x52
    UINT_0          = 0x43
    ULONG           = 0x80
    SMALL_ULONG     = 0x53
    ULONG_0         = 0x44
    BYTE            = 0x51
    SHORT           = 0x61
    INT             = 0x71
    SMALL_INT       = 0x54
    LONG            = 0x81
    SMALL_LONG      = 0x55
    FLOAT           = 0x72
    DOUBLE          = 0x82
    DECIMAL_32      = 0x74
    DECIMAL_64      = 0x84
    DECIMAL_128     = 0x94
    CHAR            = 0x73
    TIMESTAMP       = 0x83
    UUID            = 0x98
    BINARY_8        = 0xA0
    BINARY_32       = 0xB0
    STRING_8        = 0xA1
    STRING_32       = 0xB1
    SYMBOL_8        = 0xA3
    SYMBOL_32       = 0xB3
    LIST_0          = 0x45
    LIST_8          = 0xC0
    LIST_32         = 0xD0
    MAP_8           = 0xC1
    MAP_32          = 0xD1
    ARRAY_8         = 0xE0
    ARRAY_32        = 0xF0
