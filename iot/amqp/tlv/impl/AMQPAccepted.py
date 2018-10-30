from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.header.api.Parsable import *

class AMQPAccepted(Parsable):

    def toArgumentsList(self):
        list = TLVList(None,None);
        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x24))
        list.setConstructor(constructor);
        return list

    def fromArgumentsList(self, list):
        pass

    def toString(self):
        return 'AMQPAccepted []'