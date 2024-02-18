import requests
import queue
import threading
import traceback
import sys
import atexit

class manager:
    _base_url = ""
    _auth_token = ""
    _q = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        self._base_url = ""
        self._auth_token = ""
        self._additional_info = {}
        self._q = queue.Queue()
        self._threading_event = threading.Event()
        self._threading_event.clear()
        self._thread = None
        self._initialize_hook()
        self._start_process_queue()

    @staticmethod
    def set_creds(base_url:str, auth_token:str):
        manager()._set_creds(base_url, auth_token)

    def _set_creds(self, base_url:str, auth_token:str):
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self._base_url = base_url
        self._auth_token = auth_token

    @staticmethod
    def set_additional_info(info:dict):
        manager()._set_additional_info(info)

    def _set_additional_info(self, info:dict):
        if not isinstance(info, dict):
            print("additional info should be dict")
            return
        self._additional_info = info

    def _initialize_hook(self):
        def custom_excepthook(type, value, traceback_data):
            msg_str = str(type)+" "+str(value)
            tb_str = ''.join(traceback.format_tb(traceback_data))
            self._queue_trace(msg_str, tb_str)
        sys.excepthook = custom_excepthook

    def _queue_trace(self, message:str, stacktrace:str):
        self._q.put_nowait([message, stacktrace])

    def _submit_trace(self, message:str, stacktrace:str):
        try:
            url = f"{self._base_url}/api/agent/crash_log"
            if not message:
                message = ""
            if not stacktrace:
                stacktrace = ""
            payload = {
                "message": message,
                "stack_trace": stacktrace,
                "other_info": self._additional_info
            }
            response = requests.post(url, json=payload, headers={
                "Authorization": f"Bearer {self._auth_token}"
            })
            if response.status_code != 200:
                raise Exception("request failed to submit")
        except Exception as e:
            print("failed to submit trace > "+e)

    def _start_process_queue(self):
        def _process(ins):
            while True:
                if not ins._q.empty():
                    l = ins._q.get()
                    ins._submit_trace(l[0], l[1])
                else:
                    if self._threading_event.is_set():
                        break
        self._thread = threading.Thread(target=_process, args=(self,), daemon=True)
        self._thread.start()

    def exit_thread(self):
        if self._thread is None:
            return
        self._threading_event.set()
        if self._thread.is_alive():
            try:
                self._thread.join()
            except:
                pass

    @staticmethod
    def log_exception(e:Exception):
        msg = str(e)
        trace = ''.join(traceback.format_tb(e.__traceback__))
        if len(trace) == 0:
            trace = traceback.format_exc()

        manager()._queue_trace(msg, trace)

@atexit.register
def signal_lokoguard_crashlytics_threads_to_exit():
    manager().exit_thread()