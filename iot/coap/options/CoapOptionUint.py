from venv.iot.coap.options.CoapOptionValue import  *

class CoapOptionString(CoapOptionValue):
    def __init__(self, type, length, value):
        self.type = type
        self.length = length
        self.value = value

    def getIntegerValue(self):
        return (int(self.value) & 0x00FFFFFFFF)