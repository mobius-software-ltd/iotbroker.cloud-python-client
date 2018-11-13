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
from venv.iot.coap.options.CoapOption import  *
from venv.iot.coap.options.CoapOptionType import  *
import struct

class OptionParser(object):
    def __init__(self):
        pass

    def encode(self, type, value):
        encoded = self.encodeWithType(type, value)
        option = CoapOption(type,len(encoded),encoded)
        return option

    def encodeWithType(self, type, value):
        encoded = bytearray()
        if isinstance(type, CoapOptionType):
            if type == CoapOptionType.URI_PORT or type == CoapOptionType.ACCEPT or type == CoapOptionType.CONTENT_FORMAT:
                encoded = addShort(encoded, value)
            if type == CoapOptionType.MAX_AGE or type == CoapOptionType.SIZE1 or type == CoapOptionType.OBSERVE:
                encoded = addInt(encoded, value)
            if type == CoapOptionType.IF_MATCH or type == CoapOptionType.ETAG or type == CoapOptionType.NODE_ID or type == CoapOptionType.URI_PATH or type == CoapOptionType.LOCATION_PATH or type == CoapOptionType.URI_QUERY or type == CoapOptionType.LOCATION_QUERY or type == CoapOptionType.URI_HOST or type == CoapOptionType.PROXY_SCHEME or type == CoapOptionType.PROXY_URI:
                encoded = addString(encoded, value)
            return encoded
        else:
            raise ValueError('Error.OptionParser.decode unsupported coap option type: ' + str(type))
        return encoded

    def decode(self, type, encoded):
        if isinstance(encoded, CoapOption):
            self.validateLength(type, encoded.getLength())
            return self.decodeWithType(type,encoded.getValue())
        else:
            raise ValueError('Error.OptionParser.decode encoded is not instance of CoapOption: ' + str(encoded))

    def decodeWithType(self, type, encoded):
        if isinstance(type, CoapOptionType):
            if type == CoapOptionType.URI_PORT or type == CoapOptionType.ACCEPT or type == CoapOptionType.CONTENT_FORMAT:
                return getShort(encoded)
            if type == CoapOptionType.MAX_AGE or type == CoapOptionType.SIZE1 or type == CoapOptionType.OBSERVE:
                return getInt(encoded)

            if type == CoapOptionType.IF_MATCH or type == CoapOptionType.ETAG or type == CoapOptionType.NODE_ID or type == CoapOptionType.URI_PATH or type == CoapOptionType.LOCATION_PATH or type == CoapOptionType.URI_QUERY or type == CoapOptionType.LOCATION_QUERY or type == CoapOptionType.URI_HOST or type == CoapOptionType.PROXY_SCHEME or type == CoapOptionType.PROXY_URI:
                return getString(encoded)

            if type == CoapOptionType.IF_NONE_MATCH:
                return bytearray()
        else:
            raise ValueError('Error.OptionParser.decode unsupported coap option type: ' + str(type))

    def validateLength(self, type, length):
        if isinstance(type, CoapOptionType):
            if type == CoapOptionType.URI_PORT or type == CoapOptionType.ACCEPT or type == CoapOptionType.CONTENT_FORMAT:
                if length > 2:
                    raise ValueError('Error.OptionParser.Invalid length 0-2: type = ' + str(type))
            if type == CoapOptionType.MAX_AGE or type == CoapOptionType.SIZE1 or type == CoapOptionType.OBSERVE:
                if length > 4:
                    raise ValueError('Error.OptionParser.Invalid length 0-4: type = ' + str(type))
            if type == CoapOptionType.IF_MATCH:
                if length > 8:
                    raise ValueError('Error.OptionParser.Invalid length 0-8: type = ' + str(type))
            if type == CoapOptionType.ETAG:
                if length > 8:
                    raise ValueError('Error.OptionParser.Invalid length 1-8: type = ' + str(type))
            if type == CoapOptionType.NODE_ID or type == CoapOptionType.URI_PATH or type == CoapOptionType.LOCATION_PATH or type == CoapOptionType.URI_QUERY or type == CoapOptionType.LOCATION_QUERY:
                if length > 255:
                    raise ValueError('Error.OptionParser.Invalid length 0-255: type = ' + str(type))
            if type == CoapOptionType.URI_HOST or type == CoapOptionType.PROXY_SCHEME:
                if length == 0 or length > 255:
                    raise ValueError('Error.OptionParser.Invalid length 1-255: type = ' + str(type))
            if type == CoapOptionType.PROXY_URI:
                if length == 0 or length > 1034:
                    raise ValueError('Error.OptionParser.Invalid length 1-1034: type = ' + str(type))
            if type == CoapOptionType.IF_NONE_MATCH:
                if length > 0:
                    raise ValueError('Error.OptionParser.Invalid length 0: type = ' + str(type))
        else:
            raise ValueError('Error.OptionParser.length unsupported coap option type: ' + str(type))

def addShort(data, short):
    dataStruct  = struct.pack('h', short)
    data += dataStruct[::-1]
    return data

def getShort(data):
    tuple = struct.unpack('h', data[::-1])
    return tuple[0]

def addInt(data, int):
    dataStruct  = struct.pack('i', int)
    data += dataStruct[::-1]
    return data

def getInt(data):
    tuple = struct.unpack('i', data[::-1])
    return tuple[0]

def addString(dataIn, text):
    data = dataIn
    for ch in text:
        ch = bytes(ch, encoding='utf_8')
        data += struct.pack('c', ch)
    return data

def getString(data):
    return data.decode('utf_8')