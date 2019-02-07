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
from iot.coap.tlv.CoapMessage import *
from iot.coap.tlv.CoapType import *
from iot.coap.tlv.CoapCode import *
from iot.coap.options.CoapOption import *

import struct

class CoapParser(object):
    def __init__(self):
        pass

    def encode(self, message):
        data = bytearray()
        if isinstance(message, CoapMessage):
            firstByte = 0
            firstByte += message.getVersion() << 6
            firstByte += message.getType().value << 4
            token = message.getToken()
            if token is not None and len(token) > 0:
                firstByte += len(token)
            data = addByte(data,firstByte)
            codeMsb = int(message.getCode().value / 100)
            codeLsb = message.getCode().value % 100
            codeByte = (codeMsb << 5) + codeLsb
            data = addByte(data, codeByte)
            data = addShort(data, message.getPacketID())

            if token is not None and len(token) > 0:
                data = addString(data, token)
            previousNumber = 0
            for option in message.getOptions():
                if isinstance(option, CoapOption):
                    delta = option.getType().value - previousNumber
                    nextByte = 0
                    extendedDelta = None
                    if delta < 13:
                        nextByte += delta << 4
                    else:
                        extendedDelta = delta
                        if delta < 0xFF:
                            nextByte = 13 << 4
                        else:
                            nextByte = 14 << 4
                    extendedLength = None
                    if option.getLength() < 13:
                        nextByte += option.getLength()
                    else:
                        extendedLength = option.getLength()
                        if option.getLength() < 0xFF:
                            nextByte += 13
                        else:
                            nextByte += 14
                    data = addByte(data, nextByte)
                    if extendedDelta is not None:
                        if extendedDelta < 0xFF:
                            data = addByte(data, extendedDelta - 13)
                        else:
                            data = addShort(data, extendedDelta - 269)
                    if extendedLength is not None:
                        if extendedLength < 0xFF:
                            data = addByte(data, extendedLength - 13)
                        else:
                            data = addShort(data, extendedLength - 269)
                    data += option.getValue()
                    previousNumber = option.getType().value
            data = addByte(data, 0xFF)

            if message.getPayload() is not None and len(message.getPayload()) > 0:
                data = addString(data, message.getPayload())

        return data

    def decode(self, data):
        index = 0
        firstByte = getByte(data, index)
        index += 1

        version = firstByte >> 6
        if version != 1:
            raise ValueError('Error.decode Invalid version: ' + str(version))

        typeValue = (firstByte >> 4) & 3
        type = CoapType(typeValue)

        tokenLength = firstByte & 0xF
        if tokenLength > 8:
            raise ValueError('Error.decode Invalid token length: ' + str(tokenLength))

        codeByte = getByte(data, index)
        index += 1
        codeValue = (codeByte >> 5) * 100
        codeValue += codeByte & 0x1F
        code = CoapCode(codeValue)
        if code is None:
            raise ValueError('Error.decode Unsupported code value: ' + str(codeValue))

        messageID = getShort(data[index:index + 2])
        index += 2

        token = None
        if tokenLength > 0:
            token = getString(data[index:index + tokenLength])
            index += tokenLength

        number = 0
        options = []
        while index < len(data):
            nextByte = getByte(data, index)
            index += 1

            if nextByte == 0xFF:
                break

            delta = (nextByte >> 4) & 15
            if delta == 13:
                delta = getByte(data, index)
                index += 1
                delta += 13
            elif delta == 14:
                delta = getShort(data[index:index+2])
                index += 2
                delta += 269
            elif delta > 14:
                raise ValueError('Error.decode Invalid option delta value: ' + str(delta))

            number += delta

            optionLength = nextByte & 15
            if optionLength == 13:
                optionLength = getByte(data, index)
                index += 1
                optionLength += 13
            elif optionLength == 14:
                delta = getShort(data[index:index + 2])
                index += 2
                delta += 269
            elif optionLength > 14:
                raise ValueError('Error.decode Invalid option length value: ' + str(optionLength))

            optionValue = None
            if optionLength > 0:
                optionValue = data[index:index+optionLength]
                index += optionLength

            options.append(CoapOption(number, optionLength, optionValue))

        payload = None
        if index < len(data):
            payload = getString(data[index:len(data)])

        message = CoapMessage(1,type,code,messageID,token,options,payload)
        return message

def addByte(data, byte):
    data.append(byte)
    return data

def getByte(data, index):
    tuple = struct.unpack('B', data[index: index+1])
    return tuple[0]

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