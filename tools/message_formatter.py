from typing import Dict

MESSAGE = "message"
STATUS = "status"
EXTRA_INFO = "extra_info"


def message_formatter(message, status, extra_info=None) -> Dict[str, str]:
    if extra_info is None:
        extra_info = {}

    return {STATUS: status, MESSAGE: message, EXTRA_INFO: extra_info}
