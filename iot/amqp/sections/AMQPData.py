from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *

class AMQPData(AMQPSection):
    def __init__(self, data):
        self.data = data

    def getValue(self):
        bin = None
        if self.data is not None:
            bin = AMQPWrapper.wrap(self.data)
        else:
            bin = TLVNull()
        constructor = DescribedConstructor(bin.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x75))
        bin.setConstructor(constructor)
        return bin

    def fill(self, value):
        if value is not None:
            self.data = AMQPUnwrapper.unwrapBinary(value)

    def getCode(self):
        return SectionCode.DATA

    def toString(self):
        return 'AMQPData [data=' + str(self.data) + ']'

    def getData(self):
        return self.data

    def setValue(self, data):
        self.data = data

