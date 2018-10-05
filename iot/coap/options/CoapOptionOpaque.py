from venv.iot.coap.options.CoapOptionValue import  *

class CoapOptionOpaque(CoapOptionValue):
    def __init__(self, type, length, value):
        self.type = type
        self.length = length
        self.value = value