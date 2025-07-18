import os
from typing import Dict
import requests
from PySide6.QtCore import Signal
from airunner.enums import SignalCode
from airunner.components.application.workers.worker import Worker
from airunner.settings import DEFAULT_HF_ENDPOINT


class DownloadWorker(Worker):
    progress = Signal(int, int)  # current, total
    finished = Signal(dict)
    failed = Signal(Exception)
    running = False
    is_cancelled = False

    @staticmethod
    def get_size(url: str):
        try:
            response = requests.head(url, allow_redirects=True)
            size_kb = int(response.headers.get("content-length", 0))
            return size_kb
        except OverflowError:
            print(f"OverflowError when getting size for {url}")
            raise

    def cancel(self):
        self.is_cancelled = True

    def handle_message(self, data: Dict):
        self.running = True
        path = data.get("requested_path", "")
        file_name = data.get("requested_file_name", "")
        file_path = data.get("requested_file_path", "")
        callback = data.get("requested_callback", None)

        if path == "" and file_name == "" and file_path == "":
            callback()
            return
        url = f"{DEFAULT_HF_ENDPOINT}/{path}/resolve/main/{file_name}?download=true".replace(
            " ", ""
        )
        self.emit_signal(SignalCode.CLEAR_DOWNLOAD_STATUS_BAR)
        self.emit_signal(
            SignalCode.SET_DOWNLOAD_STATUS_LABEL,
            {"message": f"Downloading {file_name}"},
        )

        file_name = os.path.join(file_path, file_name)
        file_name = os.path.expanduser(file_name)
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
            except FileExistsError:
                pass

        if os.path.exists(file_name):
            self.emit_signal(
                SignalCode.UPDATE_DOWNLOAD_LOG,
                {"message": f"File already exists, skipping download"},
            )
            self.emit_signal(
                SignalCode.DOWNLOAD_PROGRESS, {"current": 0, "total": 0}
            )
            self.api.download_complete(file_name)
            return

        size_kb = self.get_size(url)
        self.emit_signal(
            SignalCode.UPDATE_DOWNLOAD_LOG,
            {
                "message": f"Downloading {url} of size {size_kb} KB to {file_name}"
            },
        )

        try:
            headers = {}
            with requests.get(
                url, headers=headers, stream=True, allow_redirects=True
            ) as r:
                r.raise_for_status()
                dir_name = os.path.dirname(file_name)

                if dir_name != "" and not os.path.exists(dir_name):
                    try:
                        os.makedirs(dir_name, exist_ok=True)
                    except FileExistsError:
                        pass

                with open(file_name, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if self.is_cancelled:
                            break
                        try:
                            f.write(chunk)
                        except OverflowError:
                            print(f"OverflowError when writing to {file_name}")
                            raise
                        self.emit_signal(
                            SignalCode.DOWNLOAD_PROGRESS,
                            {"current": f.tell(), "total": size_kb},
                        )
                    self.emit_signal(
                        SignalCode.UPDATE_DOWNLOAD_LOG,
                        {"message": f"finished with download of {file_name}"},
                    )
                    # Also emit the DOWNLOAD_COMPLETE signal to update the progress bar
                    self.api.download_complete(file_name)
                    self.finished.emit({})
        except Exception as e:
            print(f"Failed to download {url}")
            print(e)
            self.failed.emit(e)
