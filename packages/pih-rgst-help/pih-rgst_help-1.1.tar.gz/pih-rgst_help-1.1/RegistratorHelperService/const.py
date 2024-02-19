import ipih

from pih import A
from pih.collections.service import ServiceDescription


NAME: str = "RegistratorHelper"

HOST = A.CT_H.BACKUP_WORKER


MODULES: tuple[str, ...] = (
    A.PTH_FCD_DIST.NAME(A.CT_SR.MOBILE_HELPER.standalone_name),  # type: ignore
)

VERSION: str = "1.1"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Registrator mobile helper service",
    host=HOST.NAME,
    version=VERSION,
    standalone_name="rgst_help",
)
