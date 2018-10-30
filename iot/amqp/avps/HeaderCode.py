from enum import Enum

class HeaderCode(Enum):
    OPEN        = 0x10
    BEGIN       = 0x11
    ATTACH      = 0x12
    FLOW        = 0x13
    TRANSFER    = 0x14
    DISPOSITION = 0x15
    DETACH      = 0x16
    END         = 0x17
    CLOSE       = 0x18
    MECHANISMS  = 0x40
    INIT        = 0x41
    CHALLENGE   = 0x42
    RESPONSE    = 0x43
    OUTCOME     = 0x44
    PING        = 0xff
    PROTO       = 0xfe
