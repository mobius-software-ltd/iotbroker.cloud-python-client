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
class MQConnect(object):
    def __init__(self,username,password,clientID,cleanSession,keepAlive,will):
        self.username = username
        self.password = password
        self.clientID = clientID
        self.cleanSession = cleanSession
        self.keepAlive = keepAlive
        self.will = will
        self.protocolLevel = 4

    def getLength(self):
        length = 10
        length = length + len(self.clientID) + 2
        if self.will is not None:
            length = length + self.will.getLength()

        if self.username is not None:
            length = length + len(self.username) + 2

        if self.password is not None:
            length = length + len(self.password) + 2

        return int(length)

    def getType(self):
        return 1

    def getProtocol(self):
        return 1

    def setProtocolLevel(self, level):
        self.protocolLevel = level

    def willValid(self):
        if self.will.getLength()==0:
            return False
        return True

    def getLengthWill(self):
        return self.will.getLength

    def getKeepAlive(self):
        return self.keepAlive