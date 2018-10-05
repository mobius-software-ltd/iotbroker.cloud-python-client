from enum import Enum

class ReturnCode(Enum):
    ACCEPTED = 0,
    CONGESTION = 1,
    INVALID_TOPIC_ID = 2,
    NOT_SUPPORTED = 3