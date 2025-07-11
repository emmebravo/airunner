from airunner.components.application.gui.widgets.base_widget import BaseWidget
from airunner.components.tts.gui.widgets.templates.speecht5_preferences_ui import (
    Ui_speecht5_preferences,
)
from airunner.components.tts.data.models.speech_t5_settings import SpeechT5Settings


class SpeechT5PreferencesWidget(BaseWidget):
    widget_class_ = Ui_speecht5_preferences

    def __init__(self, id: int, *args, **kwargs):
        self._id: int = id
        super().__init__(*args, **kwargs)
        if self.speech_t5_settings is None:
            SpeechT5PreferencesWidget.objects.create()

    def initialize_ui(self):
        self.ui.pitch.setProperty("table_item", self.speech_t5_settings)
        voice = None

        settings = SpeechT5Settings.objects.get(self._id)

        if settings is not None:
            voice = settings.voice

        if voice:
            self.ui.voice.setCurrentText(voice)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_settings()

    def initialize_form(self):
        settings = SpeechT5Settings.objects.get(self._id)
        if settings is not None:
            self.ui.pitch.init(current_value=settings.pitch / 100)

    def voice_changed(self, text):
        SpeechT5PreferencesWidget.objects.update(
            voice=text,
        )

    def load_settings(self):
        """Load the SpeechT5 settings into the widget."""
        # Populate the widget with settings (e.g., pitch, voice)
        pass
