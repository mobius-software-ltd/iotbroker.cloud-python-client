from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.avps.SectionCode import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.HeaderFactory import *
from venv.iot.amqp.header.impl.AMQPPing import *
from venv.iot.amqp.header.impl.AMQPProtoHeader import *
from venv.iot.amqp.header.impl.AMQPPing import *
from venv.iot.amqp.header.impl.AMQPTransfer import *
from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.classes.NumericUtil import NumericUtil as util

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
            length += arguments.size

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
        return buf

    def decode(self, data):
        length = util.getInt(data) & 0xffffffff
        self.index += 4
        doff = util.getByte(data) & 0xff
        self.index += 1
        type = util.getByte(data) & 0xff
        self.index += 1
        channel = util.getShort(data) & 0xffff
        self.index += 2

        


