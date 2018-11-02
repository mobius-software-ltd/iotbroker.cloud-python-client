from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *

class AMQPSequence(AMQPSection):
    def __init__(self, sequence):
        self.sequence = sequence

    def getValue(self):
        list = TLVList(None, None)

        if self.sequence is not None and len(self.sequence) > 0:
            list = AMQPWrapper.wrapList(self.sequence)

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x76))
        list.setConstructor(constructor)
        return list

    def fill(self, list):
        if list is not None:
            self.sequence = AMQPUnwrapper.unwrapList(list)

    def getCode(self):
        return SectionCode.SEQUENCE

    def toString(self):
        return 'AMQPSequence [sequence=' + str(self.sequence) + ']'

    def getSequence(self):
        return self.sequence

    def setSequence(self, sequence):
        self.sequence = sequence

