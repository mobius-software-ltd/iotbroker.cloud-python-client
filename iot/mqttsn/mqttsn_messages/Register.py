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
from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class Register(object):
    def __init__(self, topicID, packetID, topicName):
        self.topicID = topicID
        self.packetID = packetID
        self.topicName = topicName

    def getLength(self):
        if self.topicName is None or len(self.topicName) == 0:
            raise ValueError('Register.getLength() must contain a valid topic name')
        length = 6 + len(self.topicName)
        if len(self.topicName) > 249:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_REGISTER.value[0]

    def getTopicID(self):
        return self.topicID

    def setTopicID(self, topicID):
        self.topicID = topicID

    def getPacketID(self):
        return self.packetID

    def setPacketID(self, packetID):
        self.packetID = packetID

    def getTopicName(self):
        return self.topicName

    def setTopicName(self, topicName):
        self.topicName = topicName