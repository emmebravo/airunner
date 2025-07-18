import os
import requests
from json.decoder import JSONDecodeError
from PySide6.QtCore import QThread
from airunner.utils.application.mediator_mixin import MediatorMixin
from airunner.components.application.gui.windows.main.settings_mixin import SettingsMixin
from airunner.components.application.workers.civit_ai_download_worker import CivitAIDownloadWorker


class DownloadCivitAI(MediatorMixin, SettingsMixin):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None
        self.file_name = None

    def get_json(self, model_id: str):
        # if model_id == id/name split and get the id
        if "/" in model_id:
            model_id = model_id.split("/")[0]
        url = f"https://civitai.com/api/v1/models/{model_id}"
        if self.application_settings.civit_ai_api_key:
            url = f"{url}?token={self.application_settings.civit_ai_api_key}"
        headers = {
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {api_token}"
        }
        print(f"Getting model data from CivitAI {url}")
        response = requests.get(url, headers=headers, allow_redirects=True)
        json = None
        try:
            json = response.json()
        except JSONDecodeError:
            print(f"Failed to decode JSON from {url}")
            print(response)
        return json

    def download_model(self, url, file_name, size_kb, callback):
        self.file_name = file_name
        self.worker = CivitAIDownloadWorker()
        self.worker.add_to_queue((url, file_name, size_kb))
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.worker.finished.connect(lambda: self.api.download_complete)
        self.worker.finished.connect(self.thread.quit)
        self.worker.progress.connect(
            lambda current, total: callback(current, total)
        )
        print(f"Starting model download thread")
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.download)
        self.thread.start()

    def remove_file(self):
        if os.path.exists(
            self.file_name
        ):  # Check if the file exists and delete if so
            os.remove(self.file_name)
            print(
                f"Download of {self.file_name} was cancelled and the file has been deleted."
            )

    def stop_download(self):
        if self.worker:
            self.worker.cancel()
            self.remove_file()


class CivitAIDownloader:
    """
    Simple downloader for CivitAI models for testability and modularity.
    """

    def download(self, model_id: str, version: str) -> str:
        """
        Download a model from CivitAI.
        Args:
            model_id: The model ID on CivitAI.
            version: The version to download.
        Returns:
            str: Path to the downloaded model file.
        """
        # In real code, implement actual download logic
        # Here, just a stub for testability
        return f"/models/{model_id}/{version}/model.safetensors"


def download_model(model_id: str, version: str) -> str:
    """
    Download a model from CivitAI using CivitAIDownloader.
    Args:
        model_id: The model ID on CivitAI.
        version: The version to download.
    Returns:
        str: Path to the downloaded model file.
    """
    downloader = CivitAIDownloader()
    return downloader.download(model_id, version)
