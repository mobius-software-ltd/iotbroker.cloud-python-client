from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.tlv.impl.TLVList import *


class AMQPPing(AMQPHeader):
    def __init__(self):
        self.code = HeaderCode.PING
        self.doff = 2
        self.type = 0
        self.channel = 0

    def toArgumentsList(self):
        return None

    def fromArgumentsList(self, list):
        pass

    def toString(self):
        return "AMQPPing"
