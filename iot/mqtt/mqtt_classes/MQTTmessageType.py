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

class MQTTmessageType(Enum):
    MQ_CONNECT = 1,
    MQ_CONNACK = 2,
    MQ_PUBLISH = 3,
    MQ_PUBACK = 4,
    MQ_PUBREC = 5,
    MQ_PUBREL = 6,
    MQ_PUBCOMP = 7,
    MQ_SUBSCRIBE = 8,
    MQ_SUBACK = 9,
    MQ_UNSUBSCRIBE = 10,
    MQ_UNSUBACK = 11,
    MQ_PINGREQ = 12,
    MQ_PINGRESP = 13,
    MQ_DISCONNECT = 14