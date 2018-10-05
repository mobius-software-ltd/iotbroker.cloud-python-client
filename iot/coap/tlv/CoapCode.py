from enum import Enum

class CoapCode(Enum):
    GET                         = 1
    POST                        = 2
    PUT                         = 3
    DELETE                      = 4
    CREATED                     = 201
    DELETED                     = 202
    VALID                       = 203
    CHANGED                     = 204
    BAR_DEQUEST                 = 400
    UNAUTHORIZED                = 401
    BAD_OPTION                  = 402
    FORBIDDEN                   = 403
    NOT_FOUND                   = 404
    METHOD_NOT_ALLOWED          = 405
    NOT_ACCEPTABLE              = 406
    PRECONDITION_FAILED         = 407
    REQUEST_ENTITY_TOO_LARGE    = 412
    UNSUPPORTED_CONTENT_FORMAT  = 415
    INTERNAL_SERVER_ERROR       = 500
    NOT_IMPLEMENTED             = 501
    BAD_GATEWAY                 = 502
    SERVICE_UNAVAILABLE         = 503
    GATEWAY_TIMEOUT             = 504
    PROXYING_NOT_SUPPORTED      = 505