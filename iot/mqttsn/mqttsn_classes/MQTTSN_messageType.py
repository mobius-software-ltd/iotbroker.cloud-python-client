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

class MQTTSN_messageType(Enum):
    SN_ADVERTISE = 0,                    #0x00
    SN_SEARCHGW = 1,                     #0x01
    SN_GWINFO = 2,                       #0x02
    SN_CONNECT = 4,                      #0x04
    SN_CONNACK = 5,                      #0x05
    SN_WILL_TOPIC_REQ = 6,               #0x06
    SN_WILL_TOPIC = 7,                   #0x07
    SN_WILL_MSG_REQ = 8,                 #0x08
    SN_WILL_MSG = 9,                     #0x09
    SN_REGISTER = 10,                    #0x0A
    SN_REGACK = 11,                      #0x0B
    SN_PUBLISH = 12,                     #0x0C
    SN_PUBACK = 13,                      #0x0D
    SN_PUBCOMP = 14,                     #0x0E
    SN_PUBREC = 15,                      #0x0F
    SN_PUBREL = 16,                      #0x10
    SN_SUBSCRIBE = 18,                   #0x12
    SN_SUBACK = 19,                      #0x13
    SN_UNSUBSCRIBE = 20,                 #0x14
    SN_UNSUBACK = 21,                    #0x15
    SN_PINGREQ = 22,                     #0x16
    SN_PINGRESP = 23,                    #0x17
    SN_DISCONNECT = 24,                  #0x18
    SN_WILL_TOPIC_UPD = 26,              #0x1A
    SN_WILL_TOPIC_RESP = 27,             #0x1B
    SN_WILL_MSG_UPD = 28,                #0x1C
    SN_WILL_MSG_RESP = 29,               #0x1D
    SN_ENCAPSULATED = 254               #0xFE
