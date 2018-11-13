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

class ConnectionState(Enum):
    START       = 'START'
    HDR_CRV     = 'HDR_CRV'
    YDR_SENT    = 'YDR_SENT'
    HDR_EXCH    = 'HDR_EXCH'
    OPEN_PIPE   = 'OPEN_PIPE'
    OC_PIPE     = 'OC_PIPE'
    OPEN_RCVD   = 'OPEN_RCVD'
    OPEN_SENT   = 'OPEN_SENT'
    CLOSE_PIPE  = 'CLOSE_PIPE'
    OPENED      = 'OPENED'
    CLOSE_RCVD  = 'CLOSE_RCVD'
    CLOSE_SENT  = 'CLOSE_SENT'
    DISCARDING  = 'DISCARDING'
    END         = 'END'