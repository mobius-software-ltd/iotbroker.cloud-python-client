from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.avps.SectionCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *


class SASLMechanisms(AMQPHeader):
    def __init__(self,code,doff,type,channel,mechanisms):

        if code is not None:
            self.code = code
        else:
            self.code = HeaderCode.MECHANISMS.value
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
        self.mechanisms = mechanisms

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.mechanisms == None:
            raise ValueError("At least one SASL Mechanism must be specified")
        wrapper = AMQPWrapper()
        list.addElement(0,wrapper.wrapArray(self.mechanisms))
        #print('SASLMechanismsm.toArgumentsList ' + str(list))
        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x40))
        list.setConstructor(constructor)
        #print('SASLMechanisms.toArgumentsList ' + str(list.getConstructor().getCode().value))
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size > 0:
                element = list.getList()[0]
                if element is None:
                    raise ValueError("Received malformed SASL-Init header: mechanism can't be null")
                unwrapper = AMQPUnwrapper()
                #print('fromArgumentsList element ' + str(element))
                self.mechanisms = unwrapper.unwrapArray(element)

    def toString(self):
        return "SASLMechanisms [mechanisms=" + str(self.mechanisms) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setMechanisms(self, mechanisms):
        self.mechanisms = mechanisms

    def getMechanisms(self):
        return self.mechanisms


