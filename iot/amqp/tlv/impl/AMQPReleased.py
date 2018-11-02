from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.Parsable import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVFixed import *

class AMQPReleased(Parsable):
    def __init__(self):
        pass

    def toArgumentsList(self):
        list = TLVList(None,None)
        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x26))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        pass

    def toString(self):
        return 'AMQPReleased []'

    def getError(self):
        return self.error

    def setError(self, error):
        self.error = error