from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVNull import *

class AMQPClose(AMQPHeader):
    def __init__(self,code,doff,type,channel,error):
        self.code = code
        self.doff = doff
        self.type = type
        self.channel = channel
        self.error = error

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.error is not None and isinstance(self.error,AMQPError):
            list.addElement(0, self.error.toArgumentsList())
        else:
            list.addElement(0, TLVNull())

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size > 0:
                element = list.getList()[0]
                if element is not None and isinstance(element,TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError("Expected type 'ERROR' - received: " + str(element.getCode()))
                    self.error = AMQPError(None,None,None)
                    self.error.fromArgumentsList(element)

    def toString(self):
        return "AMQPClose [error=" + str(self.error) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setError(self, error):
        self.error = error

    def getError(self):
        return self.error