from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.avps.OutcomeCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *
import hashlib

class SASLResponse(AMQPHeader):
    def __init__(self,code,doff,type,channel,response):
        if code is not None:
            self.code = code
        else:
            self.code = HeaderCodeClear.OUTCOME
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
        self.response = response

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.response == None:
            raise ValueError("SASL-Response header's challenge can't be null")
        list.addElement(0,AMQPWrapper.wrap(self.response))

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x43))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size == 0:
                raise ValueError("Received malformed SASL-Response header: challenge can't be null")
            if size > 1:
                raise ValueError('Received malformed SASL-Response header. Invalid number of arguments: ' + str(size))

            if size > 0:
                element = list.getList()[0]
                if element is None:
                    raise ValueError("Received malformed SASL-Response header: challenge can't be null")
                self.response = AMQPUnwrapper.unwrapBinary(element)

    def toString(self):
        return "SASLResponse [response=" + str(self.response) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def getResponse(self):
        return self.response

    def calcCramMD5(self,challenge,user):
        data = bytearray()
        if challenge is not None and len(challenge) > 0:
            m = hashlib.md5()
            m.update(challenge)
            data = m.digest()
            hash = user + ' '
            for i in data:
                hex = chr(0xFF & i)
                if len(hex) == 1:
                    hex += '0'
                hash += hex
            return bytes(hash,'utf-8')
        else:
            return data

    def setCramMD5Response(self,challenge,user):
        if user is None:
            raise ValueError("CramMD5 response generator must be provided with a non-null username value")
        if challenge is None:
            raise ValueError("CramMD5 response generator must be provided with a non-null challenge value")
        self.response = self.calcCramMD5(challenge,user)
