import ipih

from pih.consts import UNKNOWN
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "PolibasePersonNotification"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "1.0"
   
SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Polibase Person Notification service",
    host=HOST.NAME,
    use_standalone=True,
    version=VERSION,
    standalone_name="plb_ntf",
    run_from_system_account=True,
    python_executable_path=UNKNOWN,
)