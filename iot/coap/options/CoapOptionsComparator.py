from venv.iot.coap.options.CoapOption import  *

class CoapOptionComparator(object):
    def __init__(self):
        pass
    
    def compare(self, obj1, obj2):
        if isinstance(obj1, CoapOption) and isinstance(obj2, CoapOption):
            if obj1.getType() > obj2.getType():
                return 1
            elif obj1.getType() == obj2.getType():
                return 0
        return -1