
import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription


NAME: str = "FileWatchdog"

HOST = Hosts.BACKUP_WORKER

MODULES: tuple[str, ...] = ("watchdog",)

VERSION: str = "1.0"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="FileWatchdog service",
    host=HOST.NAME,
    commands=(
        "listen_for_new_files",
    ),
    version = VERSION,
    use_standalone=True,
    standalone_name="file"
)