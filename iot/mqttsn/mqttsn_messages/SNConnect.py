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
from iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class SNConnect(object):
    def __init__(self, willPresent, cleanSession, duration, clientID):
        self.willPresent = willPresent
        self.cleanSession = cleanSession
        self.duration = duration
        self.clientID = clientID
        self.protocolID = 1

    def getLength(self):
        if self.clientID is None or len(self.clientID) == 0:
            raise ValueError('SNConnect.getLength() must contain a valid clientID')
        length = 6 + len(self.clientID)
        return length

    def getType(self):
        return MQTTSN_messageType.SN_CONNECT.value[0]

    def getWillPresent(self):
        return self.willPresent

    def setWillPresent(self, willPresent):
        self.willPresent = willPresent

    def getCleanSession(self):
        return self.cleanSession

    def setCleanSession(self, cleanSession):
        self.cleanSession = cleanSession

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration

    def getClientID(self):
        return self.clientID

    def setClientID(self, clientID):
        self.clientID = clientID

    def getProtocolID(self):
        return self.protocolID