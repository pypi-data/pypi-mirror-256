import ipih
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "Mail"
SECTION: str = "MailboxInfo"

HOST = Hosts.WS255

VERSION: str = "1.0"

TIMEOUT: int = 10
TRY_AGAIN_SLEEP_TIME: int = 1
TRY_AGAIN_COUNT: int = 5

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Mail service",
    host=HOST.NAME,
    commands=(
        "check_email_accessibility",
        "send_email",
        "get_email_information",
        "check_email_external",
    ),
    standalone_name="mail",
    use_standalone=True,
    version=VERSION,
)
