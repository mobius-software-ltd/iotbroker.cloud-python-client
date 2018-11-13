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
from venv.iot.coap.options.CoapOption import *

class CoapMessage(object):
    def __init__(self, version, type, code, packetID, token, options, payload):
        self.version = version
        self.type = type
        self.code = code
        self.packetID = packetID
        self.token = token
        self.options = options
        self.payload = payload

    def equals(self, obj):
        if self == obj:
            return True
        return False

    def getVersion(self):
        return self.version

    def setVersion(self, version):
        self.version = version

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getPacketID(self):
        return self.packetID

    def setPacketID(self, packetID):
        self.packetID = packetID

    def getToken(self):
        return self.token

    def setToken(self, token):
        self.token = token

    def getOptions(self):
        #if isinstance(CoapOption.type, int):
         #   return self.getOptionsDecode()
        #else:
        return sorted(self.options, key=lambda CoapOption: CoapOption.type.value)

    def getOptionsDecode(self):
        return self.options

    def setOptions(self, options):
        self.options = options

    def getPayload(self):
        return self.payload

    def setPayload(self, payload):
        self.payload = payload