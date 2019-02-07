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
from iot.amqp.avps.HeaderCode import *
from iot.amqp.header.api.AMQPHeader import *
from iot.amqp.tlv.impl.TLVList import *
from iot.classes.NumericUtil import NumericUtil as util

class AMQPProtoHeader(AMQPHeader):
    def __init__(self,protocolId):
        self.protocol = 'AMQP'
        self.code = HeaderCode.PROTO
        self.doff = 2
        self.type = 0
        self.channel = 0
        self.protocolId = protocolId
        self.versionMajor = 1
        self.versionMinor = 0
        self.versionRevision = 0

    def getBytes(self):
        data = bytearray()
        data = util.addString(data,self.protocol)
        data = util.addByte(self.protocolId)
        data = util.addByte(self.versionMajor)
        data = util.addByte(self.versionMinor)
        data = util.addByte(self.versionRevision)
        return data

    def toArgumentsList(self):
        return None

    def fromArgumentsList(self, list):
        pass

    def toString(self):
        return "AMQPProtoHeader [protocol=" + str(self.protocol) + ", protocolId=" + str(self.protocolId) + ", versionMajor=" + str(self.versionMajor) + ", versionMinor=" + str(self.versionMinor) + ", versionRevision=" + str(self.versionRevision) + "]"

    def getProtocol(self):
        return self.protocol

    def getProtocolId(self):
        return self.protocolId

    def getVersionMajor(self):
        return self.versionMajor

    def getVersionMinor(self):
        return self.versionMinor

    def getVersionRevision(self):
        return self.versionRevision

