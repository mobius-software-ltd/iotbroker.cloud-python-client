from enum import Enum

class CoapType(Enum):
    CONFIRMABLE         = 0
    NON_CONFIRMABLE     = 1
    ACKNOWLEDGEMENT     = 2
    RESET               = 3