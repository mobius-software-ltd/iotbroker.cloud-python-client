from enum import Enum

class DynamicNodeProperty(Enum):
    SUPPORTED_DIST_MODES = "supported-dist-modes"
    DURABLE = "durable"
    AUTO_DELETE = "auto-delete"
    ALTERNATE_EXCHANGE = "alternate-exchange"
    EXCHANGE_TYPE = "exchange-type"
