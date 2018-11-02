from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.ErrorCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.Parsable import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.AMQPError import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVFixed import *

class AMQPRejected(Parsable):
    def __init__(self, error):
        self.error = error

    def toArgumentsList(self):
        list = TLVList(None,None)
        if self.error is not None and isinstance(self.error, AMQPError):
            list.addElement(0, self.error.toArgumentsList())

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x25))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None and isinstance(element, TLVAmqp):
                    code = element.getCode()
                    if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                        raise ValueError('Expected type Error received ' + str(element.getCode()))
                    self.error = AMQPError(None, None, None)
                    self.error.fromArgumentsList(element)

    def toString(self):
        return 'AMQPRejected [error='+ str(self.error) + ']'

    def getError(self):
        return self.error

    def setError(self, error):
        self.error = error