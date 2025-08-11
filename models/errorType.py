from enum import Enum


class ErrorType(Enum):
    NOT_ERROR = 1
    ERR_UNKNOW = 2
    ERR_PROXY_CONNECTION_FAILED = 3
    ERR_TIMED_OUT = 4
    ERR_ABORTED = 5
