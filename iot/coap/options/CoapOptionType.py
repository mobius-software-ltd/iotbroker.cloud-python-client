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

class CoapOptionType(Enum):
    IF_MATCH        = 1
    URI_HOST        = 3
    ETAG            = 4
    IF_NONE_MATCH   = 5
    OBSERVE         = 6
    URI_PORT        = 7
    LOCATION_PATH   = 8
    URI_PATH        = 11
    CONTENT_FORMAT  = 12
    MAX_AGE         = 14
    URI_QUERY       = 15
    ACCEPT          = 17
    LOCATION_QUERY  = 20
    PROXY_URI       = 35
    PROXY_SCHEME    = 39
    SIZE1           = 60
    NODE_ID         = 2050