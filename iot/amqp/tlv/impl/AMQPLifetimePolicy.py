from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.LifetimePolicy import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVFixed import *

class AMQPLifetimePolicy(object):
    def __init__(self, code):
        self.code = code

    def getList(self):
        list = TLVList(None, None)
        if isinstance(self.code, LifetimePolicy):
            constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, self.code.value))
            list.setConstructor(constructor)
        return list

    def fill(self,list):
        if list is not None and isinstance(list, TLVList):
            constructor = list.getConstructor()
            self.code = LifetimePolicy(constructor.getDescriptorCode() & 0xff).value

    def getCode(self):
        return self.code