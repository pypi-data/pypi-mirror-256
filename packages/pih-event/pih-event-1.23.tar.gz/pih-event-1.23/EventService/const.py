import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts

NAME: str = "Event"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "1.23"

CONFIG_LOCATION: str = "telegram_send_config"

MODULES: tuple[str, ...] = ("telegram-send",)

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Log and Event service",
    host=HOST.NAME,
    commands=("send_log_message", "send_event"),
    standalone_name="event",
    use_standalone=True,
    version=VERSION,
)
