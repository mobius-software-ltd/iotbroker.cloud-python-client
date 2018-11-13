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
from venv.iot.amqp.avps.HeaderCode import *
from enum import Enum

class SASLState(Enum):
    NONE                = 'NONE'
    MECHANISMS_SENT     = 'MECHANISMS_SENT'
    INIT_RECEIVED       = 'INIT_RECEIVED'
    CHALLENGE_SENT      = 'CHALLENGE_SENT'
    RESPONSE_RECEIVED   = 'RESPONSE_RECEIVED'
    NEGOTIATED          = 'NEGOTIATED'

    @classmethod
    def validate(self, code):
        if isinstance(code, HeaderCode):
            if code == HeaderCode.MECHANISMS:
                return self.NONE
            elif code == HeaderCode.INIT:
                return self.MECHANISMS_SENT
            elif code == HeaderCode.CHALLENGE:
                return self.INIT_RECEIVED
            elif code == HeaderCode.RESPONSE:
                return self.CHALLENGE_SENT
            elif code == HeaderCode.OUTCOME:
                return self.RESPONSE_RECEIVED
            else:
                return self.NEGOTIATED


