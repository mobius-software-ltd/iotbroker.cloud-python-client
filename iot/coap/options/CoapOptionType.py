from enum import Enum

class CoapOptionType(Enum):
    IF_MATCH        = 1
    URI_HOST        = 3
    ETAG            = 4
    IF_NONE_MATCH   = 5
    OBSERVE         = 6
    URI_PORT        = 7
    LOCATION_PATH   = 8
    URI_PATH        = 11
    CONTENT_FORMAT  = 12
    MAX_AGE         = 14
    URI_QUERY       = 15
    ACCEPT          = 17
    LOCATION_QUERY  = 20
    PROXY_URI       = 35
    PROXY_SCHEME    = 39
    SIZE1           = 60
    NODE_ID         = 2050