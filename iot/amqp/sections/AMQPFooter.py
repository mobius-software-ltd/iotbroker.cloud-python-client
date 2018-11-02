from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *

class AMQPFooter(AMQPSection):
    def __init__(self, annotations):
        self.annotations = annotations

    def getValue(self):
        map  = TLVMap(None, None)

        if self.annotations is not None and len(self.annotations) > 0:
            map = AMQPWrapper.wrapMap(self.annotations)

        constructor = DescribedConstructor(map.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x78))
        map.setConstructor(constructor)
        return map

    def fill(self, map):
        if map is not None:
            self.annotations = AMQPUnwrapper.unwrapMap(map)

    def getCode(self):
        return SectionCode.FOOTER

    def toString(self):
        return 'AMQPFooter [annotations=' + str(self.annotations) + ']'

    def getAnnotations(self):
        return self.annotations