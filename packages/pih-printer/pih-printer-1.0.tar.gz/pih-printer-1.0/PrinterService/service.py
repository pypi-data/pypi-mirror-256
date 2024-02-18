import ipih
from pih import A

from pih.rpc import RPC

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:
    
    from PrinterService.const import SD, MODULES

    if A.U.for_service(SD, MODULES):
        
        from PrinterService.const import PrinterCommands
        from pih import PIHThread, PIHThreadPoolExecutor
        from pih.tools import while_not_do, ne, ParameterList
        from PrinterService.api import PrinterApi as Api, Printer
        from pih.collections import PrinterADInformation, Result, PrinterReport
        
        from concurrent import futures
        from typing import Any

        class DH:
            printer_report_list: list[PrinterReport] | None = None
            action_at_work: bool = False

        def update_printers_report() -> None:
            if not DH.action_at_work:
                DH.action_at_work = True
                printer_ad_information_list: Result[list[PrinterADInformation]] = (
                    A.R_PR.all().data
                )
                printer_ad_information_map: dict[str, PrinterADInformation] = {
                    printer_ad_information.portName: printer_ad_information
                    for printer_ad_information in printer_ad_information_list
                }
                printer_length: int = len(printer_ad_information_list)
                with PIHThreadPoolExecutor(max_workers=printer_length) as executor:
                    future_to_printer = {
                        executor.submit(
                            A.ER.wrap(Api.get_printer_report_for_command),
                            printer_ad_information,
                            PrinterCommands.REPORT,
                        ): printer_ad_information
                        for printer_ad_information in printer_ad_information_list
                    }
                    printer_list: list[Printer] = []
                    for future_printer in futures.as_completed(future_to_printer):
                        printer_list.append(future_printer.result())
                    DH.printer_report_list = A.D.map(
                        lambda printer: A.D.fill_data_from_source(
                            PrinterReport(
                                adminDescription=printer_ad_information_map[
                                    printer.ip
                                ].adminDescription
                            ),
                            printer,
                            skip_not_none=True,
                        ),
                        printer_list,
                    )
                DH.action_at_work = False

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:
            if sc == SC.heart_beat:
                if (RPC.SESSION.life_time.total_seconds() / 60) % A.S.get(
                    A.CT_S.PRINTER_REPORT_PERIOD_IN_MINUTES
                ) == 0:
                    update_printers_report()
                return
            if sc == SC.printers_report:
                while_not_do(lambda: ne(DH.printer_report_list), sleep_time=5)
                return Result(None, DH.printer_report_list)
            if sc == SC.printer_snmp_call:
                printer_name: str = pl.next()
                printer_name = printer_name.lower()
                return Result(
                    None,
                    Api.call_snmp(
                        A.R.get_first_item(
                            A.R.filter(
                                lambda item: item.name.lower() == printer_name,
                                A.R_PR.all(),
                            )
                        ),
                        pl.next(),
                    ),
                )

        def service_starts_handler() -> None:
            A.SRV_A.subscribe_on(SC.heart_beat, name="Printer report")
            PIHThread(update_printers_report)

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
