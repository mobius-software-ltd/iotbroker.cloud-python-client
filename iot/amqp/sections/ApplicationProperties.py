from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *

class ApplicationProperties(AMQPSection):
    def __init__(self, properties):
        self.properties = properties

    def getValue(self):
        map = TLVMap(None, None)

        if self.properties is not None and len(self.properties) > 0:
            map = AMQPWrapper.wrapMap(self.properties)

        constructor = DescribedConstructor(map.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x74))
        map.setConstructor(constructor)
        return map

    def fill(self, map):
        if map is not None:
            self.annotations = AMQPUnwrapper.unwrapMap(map)

    def getCode(self):
        return SectionCode.APPLICATION_PROPERTIES

    def toString(self):
        return 'ApplicationProperties [properties=' + str(self.properties) + ']'

    def getProperties(self):
        return self.properties

    def setProperties(self, properties):
        self.properties = properties

