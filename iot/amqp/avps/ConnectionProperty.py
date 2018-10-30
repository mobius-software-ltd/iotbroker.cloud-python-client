from enum import Enum

class ConnectionProperty(Enum):
    PLATFORM            = "platform"
    PRODUCT             = "product"
    QPID_CLIENT_PID     = "qpid.client_pid"
    QPID_CLIENT_PPID    = "qpid.client_ppid"
    QPID_CLIENT_PROCESS = "qpid.client_process"
    VERSION             = "version"
