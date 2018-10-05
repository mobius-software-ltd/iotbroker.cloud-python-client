from venv.iot.coap.options.CoapOptionValue import  *

class CoapOptionEmpty(CoapOptionValue):
    def __init__(self, type, length, value):
        self.type = type
        self.length = length
        self.value = value