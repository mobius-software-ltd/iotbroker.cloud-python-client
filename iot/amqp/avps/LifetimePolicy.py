from enum import Enum

class LifetimePolicy(Enum):
    DELETE_ON_CLOSE                 = 0x2b
    DELETE_ON_NO_LINKS              = 0x2c
    DELETE_ON_NO_MESSAGES           = 0x2d
    DELETE_ON_NO_LINKS_OR_MESSAGES  = 0x2e
