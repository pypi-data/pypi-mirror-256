import ipih

from pih.tools import nn
from pih import A, PIHThread
from FileWatchdogService.const import SD, MODULES

from dataclasses import dataclass

# version 0.4

SC = A.CT_SC

@dataclass
class HostInfo:
    name: str | None = None
    accessible: bool | None = None

ISOLATED: bool = False

def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD, MODULES):

        from pih.tools import ParameterList, ne
        
        from typing import Any
        from time import sleep
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler, FileSystemEvent


        path_list: list[str] = []
        host_info_map: dict[str, HostInfo] = {}
        observer_map: dict[str, Observer] = {}

        def on_new_file(file_path: str) -> None:
            A.PTH.save_timestamp_for_directory_info(file_path)
            A.E.new_file_detected(file_path)

        class Handler(FileSystemEventHandler):
            def on_created(self, event: FileSystemEvent):
                if not event.is_directory:
                    on_new_file(A.PTH.path(event.src_path))

            def on_deleted(self, event: FileSystemEvent):
                pass

            def on_moved(self, event: FileSystemEvent):
                pass

        def update_observer(path: str, create: bool, stop: bool) -> None:
            observer: Observer | None = None
            if stop and path in observer_map:
                observer = observer_map[path]
                observer.stop()
            if create:
                observer = Observer()
                observer_map[path] = observer
                observer.schedule(Handler(), path)
                observer.start()

        def service_starts_handler() -> None:
            A.SRV_A.subscribe_on(SC.send_event)
            PIHThread(file_observer_action)

        def detect_new_files(path: str) -> None:
            new_file_path_list: list[str] = A.PTH.get_file_list_by_directory_info(path)
            if ne(new_file_path_list):
                for new_file_path in new_file_path_list:
                    on_new_file(new_file_path)

        
        def file_observer_action() -> None:
            while True:
                for host in host_info_map:
                    before_accessable: bool | None = host_info_map[host].accessible
                    after_accessable: bool = A.C_R.accessibility_by_smb_port(
                        host, count=1, check_all=False
                    )
                    host_info_map[host].accessible = after_accessable
                    if nn(before_accessable):
                        for path in path_list:
                            if A.PTH.get_host(path).lower() == host:
                                if not before_accessable and after_accessable:
                                    update_observer(path, True, False)
                                if before_accessable and not after_accessable:
                                    update_observer(path, False, True)
                sleep(5)
        

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:
            if sc == SC.listen_for_new_files:
                path: str = A.PTH.path(pl.next())
                if path not in path_list:
                    path_list.append(path)
                host: str = A.PTH.get_host(path).lower()
                host_info_map[host] = HostInfo(host)
                update_observer(path, True, True)
                detect_new_files(path)

        A.SRV_A.serve(SD, service_call_handler, service_starts_handler, isolate=ISOLATED, as_standalone=as_standalone)
        
if __name__ == "__main__":
    start()
