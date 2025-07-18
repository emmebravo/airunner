__all__ = [
    "WhisperModelManager",
]


def __getattr__(name):
    if name == "WhisperModelManager":
        from airunner.components.stt.managers.whisper_model_manager import WhisperModelManager

        return WhisperModelManager
    raise AttributeError(f"module {__name__} has no attribute {name}")
