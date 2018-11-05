from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *

class SASLChallenge(AMQPHeader):
    def __init__(self,code,doff,type,channel,challenge):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.CHALLENGE
        if doff is not None:
            self.doff = doff
        else:
            self.doff = 2
        if type is not None:
            self.type = type
        else:
            self.type = 1
        if channel is not None:
            self.channel = channel
        else:
            self.channel = 0
        self.challenge = challenge


    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.challenge == None:
            raise ValueError("SASL-Challenge header's challenge can't be null")
        list.addElement(0,AMQPWrapper.wrap(self.challenge))

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x42))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size == 0:
                raise ValueError("Received malformedSASL-Challenge header: challenge can't be null")
            if size > 1:
                raise ValueError('Received malformed SASL-Challenge header. Invalid number of arguments: ' + str(size))
            if size > 0:
                element = list.getList()[0]
                if element is None:
                    raise ValueError("Received malformed SASL-Challenge header: challenge can't be null")
                self.challenge = AMQPUnwrapper.unwrapBinary(element)


    def toString(self):
        return "SASLChallenge [challenge=" + str(self.challenge) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setChallenge(self, challenge):
        self.challenge = challenge

    def getChallenge(self):
        return self.challenge
