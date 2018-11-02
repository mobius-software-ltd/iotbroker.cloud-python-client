from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *

class AMQPValue(AMQPSection):
    def __init__(self, value):
        self.value = value

    def getValue(self):
        val = None
        if self.value is not None:
            val = AMQPWrapper.wrap(self.value)
        else:
            val = TLVNull()

        if val is not None:
            constructor = DescribedConstructor(val.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x77))
            val.setConstructor(constructor)
        return val

    def fill(self, value):
        if value is not None:
            self.value = AMQPUnwrapper.unwrap(value)

    def getCode(self):
        return SectionCode.VALUE

    def toString(self):
        return 'AMQPValue [value=' + str(self.value) + ']'

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

