from enum import Enum

class QoSType(Enum):
    AT_MOST_ONCE = 0,
    AT_LEAST_ONCE = 1,
    EXACTLY_ONCE = 2,
    LEVEL_ONE = 3