from enum import Enum

class MQTTmessageType(Enum):
    MQ_CONNECT = 1,
    MQ_CONNACK = 2,
    MQ_PUBLISH = 3,
    MQ_PUBACK = 4,
    MQ_PUBREC = 5,
    MQ_PUBREL = 6,
    MQ_PUBCOMP = 7,
    MQ_SUBSCRIBE = 8,
    MQ_SUBACK = 9,
    MQ_UNSUBSCRIBE = 10,
    MQ_UNSUBACK = 11,
    MQ_PINGREQ = 12,
    MQ_PINGRESP = 13,
    MQ_DISCONNECT = 14