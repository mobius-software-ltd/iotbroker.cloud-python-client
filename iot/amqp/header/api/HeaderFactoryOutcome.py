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
from venv.iot.amqp.avps.StateCode import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.AMQPAccepted import *
from venv.iot.amqp.tlv.impl.AMQPModified import *
from venv.iot.amqp.tlv.impl.AMQPReceived import *
from venv.iot.amqp.tlv.impl.AMQPRejected import *
from venv.iot.amqp.tlv.impl.AMQPReleased import *

class HeaderFactoryOutcome(object):

    def getOutcome(list):
        outcome = None
        if isinstance(list, TLVList):
            byteCode = list.getConstructor().getDescriptorCode()
            code = StateCode(byteCode)
            if code == StateCode.ACCEPTED:
                outcome = AMQPAccepted()
            elif code == StateCode.MODIFIED:
                outcome = AMQPModified(None ,None ,None)
            elif code == StateCode.REJECTED:
                outcome = AMQPRejected(None)
            elif code == StateCode.RELEASED:
                outcome = AMQPReleased()
            else:
                raise ValueError('Received header with unrecognized outcome code')
        return outcome

    def getState(list):
        state = None
        if isinstance(list, TLVList):
            byteCode = list.getConstructor().getDescriptorCode()
            code = StateCode(byteCode)
            if code == StateCode.ACCEPTED:
                state = AMQPAccepted()
            elif code == StateCode.MODIFIED:
                state = AMQPModified(None,None,None)
            elif code == StateCode.RECEIVED:
                state = AMQPReceived(None,None)
            elif code == StateCode.REJECTED:
                state = AMQPRejected(None)
            elif code == StateCode.RELEASED:
                state = AMQPReleased()
            else:
                raise ValueError('Received header with unrecognized state code')
        return state