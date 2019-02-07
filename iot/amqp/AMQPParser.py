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
from iot.amqp.avps.SectionCode import *
from iot.amqp.avps.HeaderCode import *
from iot.amqp.header.api.AMQPHeader import *
from iot.amqp.header.api.HeaderFactory import *
from iot.amqp.header.impl.AMQPPing import *
from iot.amqp.header.impl.AMQPProtoHeader import *
from iot.amqp.header.impl.AMQPPing import *
from iot.amqp.header.impl.AMQPTransfer import *
from iot.amqp.sections.AMQPSection import *
from iot.amqp.tlv.impl.TLVList import *
from iot.classes.NumericUtil import NumericUtil as util

class AMQPParser(object):
    def __init__(self):
        self.index = 0

    def next(self, data, index):
        length = util.getInt(data[self.index:self.index + 4]) & 0xffffffff
        #print('Parser.next length= ' + str(length) + ' index= ' + str(index))
        self.index = index + 4
        if length == 1095586128:
            protocolId = util.getByte(data, self.index)
            self.index += 1
            versionMajor = util.getByte(data, self.index)
            self.index += 1
            versionMinor = util.getByte(data, self.index)
            self.index += 1
            versionRevision = util.getByte(data, self.index)
            self.index += 1
            if (protocolId == 0 or protocolId == 3) and versionMajor == 1 and versionMinor == 0 and versionRevision == 0:
                self.index = 0
                return data[index: 8]

        self.index = 0
        return data[index:length]

    def encode(self, header):
        buf = None

        if isinstance(header,AMQPProtoHeader):
            buf = bytearray()
            buf = util.addString(buf,'AMQP')
            buf = util.addByte(buf,header.getProtocolId())
            buf = util.addByte(buf, header.getVersionMajor())
            buf = util.addByte(buf, header.getVersionMinor())
            buf = util.addByte(buf, header.getVersionRevision())
            return buf

        if isinstance(header,AMQPPing):
            buf = bytearray()
            buf = util.addInt(buf,8)
            buf = util.addByte(buf,header.getDoff())
            buf = util.addByte(buf, header.getType())
            buf = util.addShort(buf, header.getChannel())
            return buf

        length = 8
        if isinstance(header,AMQPHeader):
            arguments = header.toArgumentsList()
            length += arguments.getLength()

        sections = None

        if header.getCode() == HeaderCode.TRANSFER and isinstance(header,AMQPTransfer):
            sections = header.getSections()
            if sections is not None and isinstance(sections,dict):
                for section in sections.values():
                    if isinstance(section, AMQPSection):
                        length += section.getValue().getLength()

        buf = bytearray()
        buf = util.addInt(buf,length)
        buf = util.addByte(buf,header.getDoff())
        buf = util.addByte(buf, header.getType())
        buf = util.addShort(buf, header.getChannel())

        if isinstance(arguments,TLVList):
            buf += arguments.getBytes()

        if sections is not None and isinstance(sections,dict):
            for section in sections.values():
                if isinstance(section, AMQPSection):
                    value = section.getValue()
                    if isinstance(value, TLVAmqp):
                        buf += value.getBytes()

        self.index = 0
        return buf

    def decode(self, data):
        #print('index= ' + str(self.index))
        length = util.getInt(data[self.index:self.index+4]) & 0xffffffff
        self.index += 4
        doff = util.getByte(data,self.index) & 0xff
        self.index += 1
        type = util.getByte(data,self.index) & 0xff
        self.index += 1
        channel = util.getShort(data[self.index:self.index+2]) & 0xffff
        self.index += 2

        if length == 8 and doff == 2 and (type == 0 or type == 1) and channel == 0:
            if self.index >= len(data):
                self.index = 0
                return AMQPPing()
            else:
                raise ValueError("Received malformed ping-header with invalid length")

        if length == 1095586128 and (doff == 3 or doff == 0) and type == 1 and channel == 0:
            if self.index >= len(data):
                self.index = 0
                return AMQPProtoHeader(doff)
            else:
                raise ValueError("Received malformed protocol-header with invalid length")

        header = None
        headerFactory = HeaderFactory(self.index)
        if type == 0:
            header = headerFactory.getAMQP(data)
        elif type == 1:
            header = headerFactory.getSASL(data)
        else:
            raise ValueError("Received malformed header with invalid type: " + type)

        self.index = headerFactory.getIndex()

        if isinstance(header, AMQPHeader):
            header.setDoff(doff)
            header.setType(type)
            header.setChannel(channel)

        if header.getCode() == HeaderCode.TRANSFER:
            if isinstance(header,AMQPTransfer):
                header.setSections({})
            while self.index < len(data):
                headerFactory.setIndex(self.index)
                section = headerFactory.getSection(data)
                header.sections[section.getCode()] = section
                self.index = headerFactory.getIndex()

        self.index = 0
        return header
