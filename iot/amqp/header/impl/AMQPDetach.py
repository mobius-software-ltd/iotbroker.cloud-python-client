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

class AMQPDetach(AMQPHeader):
    def __init__(self,code,doff,type,channel,handle,closed,error):
        self.code = code
        self.doff = doff
        self.type = type
        self.channel = channel
        self.handle = handle
        self.closed = closed
        self.error = error

    def toArgumentsList(self):
        list = TLVList(None,None)

        if self.handle is None:
            raise ValueError("Detach header's handle can't be null")
        list.addElement(0, AMQPWrapper.wrap(self.handle))
        if self.closed is not None:
            list.addElement(1, AMQPWrapper.wrap(self.closed))
        if self.error is not None and isinstance(self.error,AMQPError):
            list.addElement(2, self.error.toArgumentsList())

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            size = len(list.getList())
            if size  == 0:
                raise ValueError("Received malformed Detach header: handle can't be null")
            if size > 3:
                raise ValueError("Received malformed Detach header. Invalid number of arguments: " + str(size))
            if size > 0:
                element = list.getList()[0]
                if element is None:
                    raise ValueError("Received malformed Detach header: handle can't be null")
                self.handle = AMQPUnwrapper.unwrapUInt(element)
            if size > 1:
                element = list.getList()[1]
                if element is not None:
                    self.closed = AMQPUnwrapper.unwrapBool(element)
            if size > 2:
                element = list.getList()[2]
                if element is not None and isinstance(element,TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError("Expected type 'ERROR' - received: " + str(element.getCode()))
                    self.error = AMQPError(None, None, None)
                    self.error.fromArgumentsList(element)


    def toString(self):
        return "AMQPDetach [handle=" + str(self.handle) + ", closed=" + str(self.closed) + ", error=" + str(self.error) + ", code=" + str(self.code) + ", doff=" + str(self.doff) + ", type=" + str(self.type) + ", channel=" + str(self.channel) + "]"

    def setHandle(self, handle):
        self.handle = handle

    def getHandle(self):
        return self.handle

    def setClosed(self, closed):
        self.closed = closed

    def getClosed(self):
        return self.closed

    def setError(self, error):
        self.error = error

    def getError(self):
        return self.error