from enum import Enum

class StateCode(Enum):
    RECEIVED = 0x23
    ACCEPTED = 0x24
    REJECTED = 0x25
    RELEASED = 0x26
    MODIFIED = 0x27