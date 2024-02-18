import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts

from enum import StrEnum

NAME: str = "Printer"

HOST = Hosts.WS255

VERSION: str = "1.0"

MODULES: tuple[str, ...] = (
    "pyasn1==0.4.8",
    "pycryptodomex==3.15.0",
    "pysmi==0.3.4",
    "pysnmp",
)

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Printer service",
    host=HOST.NAME,
    commands=("printers_report", "printer_snmp_call"),
    use_standalone=True,
    standalone_name="printer",
    version=VERSION,
)


class PrinterCommands(StrEnum):
    REPORT = "report"
    STATUS = "status"