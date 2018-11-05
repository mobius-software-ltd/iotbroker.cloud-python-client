from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.classes.NumericUtil import NumericUtil as util

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

