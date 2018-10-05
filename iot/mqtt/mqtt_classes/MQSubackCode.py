from enum import Enum

class MQSubackCode(Enum):
    ACCEPTED_QOS0 = 0,
    ACCEPTED_QOS1 = 1,
    ACCEPTED_QOS2 = 2,
    FAILURE = 128