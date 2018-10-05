from enum import Enum

class Flag(Enum):
    DUPLICATE = 128,
    QOS_LEVEL_ONE = 96,
    QOS_2 = 64,
    QOS_1 = 32,
    RETAIN = 16,
    WILL = 8,
    CLEAN_SESSION = 4,
    RESERVED_TOPIC = 3,
    SHORT_TOPIC = 2,
    ID_TOPIC = 1,
    UNKNOWN = 0
