from venv.iot.amqp.avps.SectionCode import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.HeaderFactory import *
from venv.iot.amqp.header.impl.AMQPPing import *
from venv.iot.amqp.header.impl.AMQPProtoHeader import *
from venv.iot.amqp.header.impl.AMQPPing import *
from venv.iot.amqp.header.impl.AMQPTransfer import *
from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.classes.NumericUtil import NumericUtil as util
import binascii

class AMQPParser(object):
    def __init__(self):
        self.index = 0

    def next(self, data, index):
        length = util.getInt(data)
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
                return data[index, 8]

        self.index = 0
        return data[index,length]

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
            for section in sections:
                if isinstance(section, AMQPSection):
                    length += len(section.getValue())

        buf = bytearray()
        buf = util.addInt(buf,length)
        buf = util.addByte(buf,header.getDoff())
        buf = util.addByte(buf, header.getType())
        buf = util.addShort(buf, header.getChannel())

        if isinstance(arguments,TLVList):
            buf += arguments.getBytes()

        if sections is not None:
            for section in sections:
                if isinstance(section, AMQPSection):
                    value = section.getValue()
                    if isinstance(value, TLVAmqp):
                        buf.append(value.getBytes())
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

        #print('length ==' + str(length) + ' doff ==' +str(doff) + ' type ==' + str(type) + ' channel =='  +str(channel))

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

        #print('length= ' + str(length) + ' len(data)=' + str(len(data)) + ' index=' + str(self.index))
        #if length != len(data) - self.index + 8:
         #   raise ValueError("Received malformed ping-header with invalid length")

        header = None
        headerFactory = HeaderFactory(self.index)
        if type == 0:
            header = headerFactory.getAMQP(data)
        elif type == 1:
            header = headerFactory.getSASL(data)
        else:
            raise ValueError("Received malformed header with invalid type: " + type)

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
                header.getSections()[section.getCode()] = section
                self.index = headerFactory.getIndex()

        self.index = 0
        return header
