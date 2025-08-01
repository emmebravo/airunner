import os
from typing import List, Type, Optional, Dict, Any

from sqlalchemy.orm import joinedload

from PySide6.QtWidgets import QApplication

from airunner.components.application.data import ShortcutKeys, table_to_class
from airunner.components.art.data.active_grid_settings import (
    ActiveGridSettings,
)
from airunner.components.art.data.ai_models import AIModels
from airunner.components.art.data.brush_settings import BrushSettings
from airunner.components.art.data.controlnet_model import ControlnetModel
from airunner.components.art.data.controlnet_settings import ControlnetSettings
from airunner.components.art.data.drawingpad_settings import DrawingPadSettings
from airunner.components.art.data.embedding import Embedding
from airunner.components.art.data.generator_settings import GeneratorSettings
from airunner.components.art.data.grid_settings import GridSettings
from airunner.components.art.data.image_filter_value import ImageFilterValue
from airunner.components.art.data.image_to_image_settings import (
    ImageToImageSettings,
)
from airunner.components.art.data.lora import Lora
from airunner.components.art.data.memory_settings import MemorySettings
from airunner.components.art.data.metadata_settings import MetadataSettings
from airunner.components.art.data.outpaint_settings import OutpaintSettings
from airunner.components.art.data.saved_prompt import SavedPrompt
from airunner.components.art.data.schedulers import Schedulers
from airunner.components.llm.data.chatbot import Chatbot
from airunner.components.llm.data.llm_generator_settings import (
    LLMGeneratorSettings,
)
from airunner.components.llm.data.prompt_template import PromptTemplate
from airunner.components.llm.data.target_files import TargetFiles
from airunner.components.models.data.pipeline_model import PipelineModel
from airunner.components.settings.data.application_settings import (
    ApplicationSettings,
)
from airunner.components.settings.data.font_setting import FontSetting
from airunner.components.settings.data.language_settings import (
    LanguageSettings,
)
from airunner.components.llm.data.rag_settings import RAGSettings
from airunner.components.settings.data.path_settings import PathSettings
from airunner.components.settings.data.sound_settings import SoundSettings
from airunner.components.settings.data.voice_settings import VoiceSettings
from airunner.components.stt.data.stt_settings import STTSettings
from airunner.components.stt.data.whisper_settings import WhisperSettings
from airunner.components.tts.data.models.espeak_settings import EspeakSettings
from airunner.components.tts.data.models.openvoice_settings import (
    OpenVoiceSettings,
)
from airunner.components.tts.data.models.speech_t5_settings import (
    SpeechT5Settings,
)
from airunner.components.user.data.user import User
from airunner.enums import ModelService, TTSModel
from airunner.utils.image import convert_binary_to_image
from airunner.components.data.session_manager import session_scope
from airunner.components.llm.utils import get_chatbot
from airunner.utils.settings import get_qsettings
from airunner.utils.application.get_logger import get_logger
from airunner.settings import AIRUNNER_LOG_LEVEL

from airunner.components.settings.data.window_settings import WindowSettings


class SettingsMixinSharedInstance:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SettingsMixinSharedInstance, cls).__new__(
                cls, *args, **kwargs
            )
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.logger = get_logger("AI Runner", AIRUNNER_LOG_LEVEL)

        self._initialized = True
        self.chatbot: Optional[Chatbot] = None


class SettingsMixin:
    _chatbot: Optional[Chatbot] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app = QApplication.instance()
        if app:
            self.api = getattr(app, "api", None)

    @property
    def user_web_dir(self) -> str:
        """Return the user web directory."""
        return os.path.join(
            os.path.expanduser(self.path_settings.base_path), "web"
        )

    @property
    def session_manager(self):
        return self.settings_mixin_shared_instance.session_manager

    @property
    def settings_mixin_shared_instance(self):
        return SettingsMixinSharedInstance()

    @property
    def logger(self):
        return self.settings_mixin_shared_instance.logger

    @property
    def stt_settings(self) -> STTSettings:
        return self.load_settings_from_db(STTSettings)

    @property
    def application_settings(self) -> ApplicationSettings:
        return self.load_settings_from_db(ApplicationSettings)

    @property
    def language_settings(self) -> LanguageSettings:
        return self.load_settings_from_db(LanguageSettings)

    @property
    def sound_settings(self) -> SoundSettings:
        return self.load_settings_from_db(SoundSettings)

    @property
    def whisper_settings(self) -> WhisperSettings:
        return self.load_settings_from_db(WhisperSettings)

    @property
    def browser_settings(self) -> Dict[str, Any]:
        settings = get_qsettings()
        settings.beginGroup("browser")
        browser_settings = {
            "private_browsing": settings.value(
                "private_browsing", False, type=bool
            ),
            "browser_type": settings.value(
                "browser_type", "default", type=str
            ),
            "browser_os": settings.value("browser_os", "default", type=str),
            "random_user_agent": settings.value(
                "random_user_agent", False, type=bool
            ),
            "plaintext_display": settings.value(
                "plaintext_display", False, type=bool
            ),
            "summarize_display": settings.value(
                "summarize_display", False, type=bool
            ),
        }
        settings.endGroup()
        return browser_settings

    def update_browser_settings(self, **kwargs):
        settings = get_qsettings()
        settings.beginGroup("browser")
        for key, value in kwargs.items():
            settings.setValue(key, value)
        settings.endGroup()
        settings.sync()
        self.__settings_updated(
            setting_name="browser", column_name=None, val=None
        )

    @property
    def window_settings(self) -> WindowSettings:
        settings = get_qsettings()
        settings.beginGroup("window_settings")
        window_settings = WindowSettings(
            is_maximized=settings.value("is_maximized", False, type=bool),
            is_fullscreen=settings.value("is_fullscreen", False, type=bool),
            width=settings.value("width", 800, type=int),
            height=settings.value("height", 600, type=int),
            x_pos=settings.value("x_pos", 0, type=int),
            y_pos=settings.value("y_pos", 0, type=int),
            active_main_tab_index=settings.value(
                "active_main_tab_index", 0, type=int
            ),
        )
        settings.endGroup()
        return window_settings

    @window_settings.setter
    def window_settings(self, settings_dict: Dict[str, Any]):
        """Update window settings in QSettings."""
        settings = get_qsettings()
        settings.beginGroup("window_settings")
        for key, value in settings_dict.items():
            if key in ["is_maximized", "is_fullscreen"]:
                value = bool(value)
            else:
                value = int(value)
            settings.setValue(key, value)
        settings.endGroup()
        settings.sync()
        self.__settings_updated(
            setting_name="window_settings", column_name=None, val=None
        )

    @property
    def rag_settings(self) -> RAGSettings:
        rag_settings = RAGSettings.objects.first()
        if rag_settings is None:
            RAGSettings.objects.create(
                enabled=False,
                model_service=ModelService.LOCAL.value,
                model_path="",
            )
            rag_settings = RAGSettings.objects.first()
        return rag_settings

    @property
    def llm_generator_settings(self) -> LLMGeneratorSettings:
        """Return the LLMGeneratorSettings instance from the database, creating it if necessary.
        No longer manages current_chatbot; current chatbot is determined via Chatbot.objects.filter_by(current=True).
        """
        return self.load_settings_from_db(LLMGeneratorSettings)

    @property
    def generator_settings(self) -> GeneratorSettings:
        return self.load_settings_from_db(
            GeneratorSettings, eager_load=["aimodel"]
        )

    @property
    def controlnet_settings(self) -> ControlnetSettings:
        return self.load_settings_from_db(ControlnetSettings)

    @property
    def image_to_image_settings(self) -> ImageToImageSettings:
        return self.load_settings_from_db(ImageToImageSettings)

    @property
    def outpaint_settings(self) -> OutpaintSettings:
        return self.load_settings_from_db(OutpaintSettings)

    @property
    def drawing_pad_settings(self) -> DrawingPadSettings:
        return self.load_settings_from_db(DrawingPadSettings)

    @property
    def brush_settings(self) -> BrushSettings:
        return self.load_settings_from_db(BrushSettings)

    @property
    def grid_settings(self) -> GridSettings:
        return self.load_settings_from_db(GridSettings)

    @property
    def active_grid_settings(self) -> ActiveGridSettings:
        return self.load_settings_from_db(ActiveGridSettings)

    @property
    def path_settings(self) -> PathSettings:
        return self.load_settings_from_db(PathSettings)

    @property
    def memory_settings(self) -> MemorySettings:
        return self.load_settings_from_db(MemorySettings)

    @property
    def chatbots(self) -> List[Type[Chatbot]]:
        return self.load_chatbots()

    @property
    def ai_models(self) -> List[Type[AIModels]]:
        return self.load_ai_models()

    @property
    def schedulers(self) -> List[Type[Schedulers]]:
        return self.load_schedulers()

    @property
    def shortcut_keys(self) -> List[Type[ShortcutKeys]]:
        return self.load_shortcut_keys()

    @property
    def chatbot_voice_settings(self) -> VoiceSettings:
        if self.chatbot.voice_id is None:
            voice_settings = VoiceSettings.objects.first()
            if voice_settings is None:
                settings = self._get_settings_for_voice_settings(
                    TTSModel.ESPEAK
                )
                voice_settings = VoiceSettings.objects.create(
                    name="Default Voice",
                    model_type=TTSModel.ESPEAK.value,
                    settings_id=settings.id,
                )
            Chatbot.objects.update(
                self.chatbot.id,
                voice_id=voice_settings.id,
            )
            self.chatbot.voice_id = voice_settings.id

        voice_settings = VoiceSettings.objects.get(pk=self.chatbot.voice_id)

        if voice_settings is None:
            raise ValueError(
                "Chatbot voice settings not found. Please check the database."
            )

        return voice_settings

    @property
    def chatbot_voice_model_type(self) -> TTSModel:
        return TTSModel(self.chatbot_voice_settings.model_type)

    @property
    def speech_t5_settings(self) -> SpeechT5Settings:
        settings = SpeechT5Settings.objects.first()
        if settings is None:
            settings = SpeechT5Settings.objects.create()
        return SpeechT5Settings.objects.first()

    @property
    def espeak_settings(self) -> Optional[object]:
        settings = EspeakSettings.objects.first()
        if settings is None:
            settings = EspeakSettings.objects.create()
        return EspeakSettings.objects.first()

    @property
    def openvoice_settings(self) -> OpenVoiceSettings:
        settings = OpenVoiceSettings.objects.first()
        if settings is None:
            settings = OpenVoiceSettings.objects.create()
        return OpenVoiceSettings.objects.first()

    @property
    def metadata_settings(self) -> MetadataSettings:
        return self.load_settings_from_db(MetadataSettings)

    @property
    def prompt_templates(self) -> List[Type[PromptTemplate]]:
        return self.load_prompt_templates()

    @property
    def controlnet_models(self):
        return self.load_controlnet_models()

    @property
    def saved_prompts(self) -> List[Type[SavedPrompt]]:
        return self.load_saved_prompts()

    @property
    def font_settings(self) -> List[Type[FontSetting]]:
        return self.load_font_settings()

    @property
    def pipelines(self) -> List[Type[PipelineModel]]:
        return self.load_pipelines()

    @property
    def drawing_pad_image(self):
        base_64_image = self.drawing_pad_settings.image
        image = convert_binary_to_image(base_64_image)
        if image is not None:
            image = image.convert("RGB")
        return image

    @property
    def drawing_pad_mask(self):
        base_64_image = self.drawing_pad_settings.mask
        image = convert_binary_to_image(base_64_image)
        if image is not None:
            image = image.convert("RGB")
        return image

    @property
    def img2img_image(self):
        base_64_image = self.image_to_image_settings.image
        image = convert_binary_to_image(base_64_image)
        if image is not None:
            image = image.convert("RGB")
        return image

    @property
    def controlnet_image(self):
        base_64_image = self.controlnet_settings.image
        image = convert_binary_to_image(base_64_image)
        if image is not None:
            image = image.convert("RGB")
        return image

    @property
    def controlnet_generated_image(self):
        base_64_image = self.controlnet_settings.imported_image_base64
        image = convert_binary_to_image(base_64_image)
        if image is not None:
            image = image.convert("RGB")
        return image

    @property
    def outpaint_mask(self):
        base_64_image = self.drawing_pad_settings.mask
        image = convert_binary_to_image(base_64_image)
        if image is not None:
            image = image.convert("RGB")
        return image

    @property
    def outpaint_image(self):
        base_64_image = self.outpaint_settings.image
        image = convert_binary_to_image(base_64_image)
        if image is not None:
            image = image.convert("RGB")
        return image

    @property
    def image_filter_values(self) -> Optional[List[ImageFilterValue]]:
        return ImageFilterValue.objects.all()

    @property
    def chatbot(self) -> Optional[Chatbot]:
        return get_chatbot()

    def _get_settings_for_voice_settings(self, model_type: TTSModel):
        if model_type is TTSModel.SPEECHT5:
            return self.speech_t5_settings
        elif model_type is TTSModel.OPENVOICE:
            return self.openvoice_settings
        else:
            return self.espeak_settings

    @property
    def user(self) -> Type[User]:
        user = User.objects.first()
        if user is None:
            user = User()
            user.username = "User"
            user.save()
            user = User.objects.first()
        return user

    @staticmethod
    def add_chatbot_document_to_chatbot(chatbot, file_path):
        document = TargetFiles.objects.filter_by_first(
            chatbot_id=chatbot.id, file_path=file_path
        )
        if document is None:
            document = TargetFiles(file_path=file_path, chatbot_id=chatbot.id)
        TargetFiles.objects.merge(document)

    def update_application_settings(self, column_name, val):
        self.update_setting(ApplicationSettings, column_name, val)

    def update_espeak_settings(self, column_name, val):
        self.update_setting(EspeakSettings, column_name, val)

    def update_speech_t5_settings(self, column_name, val):
        self.update_setting(SpeechT5Settings, column_name, val)

    def update_controlnet_settings(self, column_name, val):
        self.update_setting(ControlnetSettings, column_name, val)

    def update_brush_settings(self, column_name, val):
        self.update_setting(BrushSettings, column_name, val)

    def update_image_to_image_settings(self, column_name, val):
        self.update_setting(ImageToImageSettings, column_name, val)

    def update_outpaint_settings(self, column_name, val):
        self.update_setting(OutpaintSettings, column_name, val)

    def update_drawing_pad_settings(self, column_name, val):
        self.update_setting(DrawingPadSettings, column_name, val)

    def update_grid_settings(self, column_name, val):
        self.update_setting(GridSettings, column_name, val)

    def update_active_grid_settings(self, column_name, val):
        self.update_setting(ActiveGridSettings, column_name, val)

    def update_path_settings(self, column_name, val):
        self.update_setting(PathSettings, column_name, val)

    def update_memory_settings(self, column_name, val):
        self.update_setting(MemorySettings, column_name, val)

    def update_metadata_settings(self, column_name, val):
        self.update_setting(MetadataSettings, column_name, val)

    def update_llm_generator_settings(self, column_name: str, val):
        self.update_setting(LLMGeneratorSettings, column_name, val)

    def update_whisper_settings(self, column_name, val):
        self.update_setting(WhisperSettings, column_name, val)

    def update_ai_models(self, models: List[AIModels]):
        for model in models:
            self.update_ai_model(model)
        self.__settings_updated()

    def update_ai_model(self, model: AIModels):
        ai_model = AIModels.objects.filter_by_first(
            name=model.name,
            path=model.path,
            branch=model.branch,
            version=model.version,
            category=model.category,
            pipeline_action=model.pipeline_action,
            enabled=model.enabled,
            model_type=model.model_type,
            is_default=model.is_default,
        )
        if ai_model:
            for key in model.__dict__.keys():
                if key != "_sa_instance_state":
                    setattr(ai_model, key, getattr(model, key))
            ai_model.save()
        else:
            model.save()
        self.__settings_updated()

    def update_generator_settings(self, column_name, val):
        generator_settings = self.generator_settings
        setattr(generator_settings, column_name, val)
        generator_settings.save()
        self.__settings_updated(
            setting_name=GeneratorSettings.__tablename__,
            column_name=column_name,
            val=val,
        )

    def update_controlnet_image_settings(self, column_name, val):
        controlnet_settings = self.controlnet_settings
        setattr(controlnet_settings, column_name, val)
        self.update_controlnet_settings(column_name, val)

    def update_setting_by_table_name(self, table_name, column_name, val):
        model_class_ = table_to_class.get(table_name)
        if model_class_ is None:
            self.logger.error(f"Model class for {table_name} not found")
            return
        setting = model_class_.objects.order_by(model_class_.id.desc()).first()
        if setting:
            model_class_.objects.update(setting.id, **{column_name: val})
            self.__settings_updated(table_name, column_name, val)
        else:
            self.logger.error("Failed to update settings: No setting found")

    @staticmethod
    def load_schedulers() -> List[Schedulers]:
        return Schedulers.objects.all()

    @staticmethod
    def load_settings_from_db(
        model_class_, eager_load: Optional[List[str]] = None
    ) -> Type:
        settings_instance = None
        try:
            with session_scope() as session:
                query = session.query(model_class_)
                if eager_load:
                    for relation in eager_load:
                        try:
                            relation_attr = getattr(
                                model_class_, relation, None
                            )
                            if relation_attr is not None:
                                query = query.options(
                                    joinedload(relation_attr)
                                )
                        except Exception as e:
                            # Use a local logger instance to avoid issues with shared state during initialization
                            local_logger = get_logger(
                                "AI Runner SettingsMixin", AIRUNNER_LOG_LEVEL
                            )
                            local_logger.warning(
                                f"Could not eager load {relation} for {model_class_.__name__}: {e}"
                            )

                settings_instance = query.first()

                if settings_instance is None:
                    local_logger = get_logger(
                        "AI Runner SettingsMixin", AIRUNNER_LOG_LEVEL
                    )
                    local_logger.info(
                        f"No settings found for {model_class_.__name__}, creating new entry."
                    )
                    settings_instance = model_class_()
                    session.add(settings_instance)
                    session.commit()
                    if settings_instance.id is not None:
                        query_after_create = session.query(model_class_)
                        if eager_load:
                            for relation in eager_load:
                                try:
                                    relation_attr = getattr(
                                        model_class_, relation, None
                                    )
                                    if relation_attr is not None:
                                        query_after_create = (
                                            query_after_create.options(
                                                joinedload(relation_attr)
                                            )
                                        )
                                except Exception:
                                    pass
                        settings_instance = query_after_create.filter(
                            model_class_.id == settings_instance.id
                        ).first()
                    else:
                        local_logger.error(
                            f"Failed to get ID for new {model_class_.__name__} instance after commit."
                        )
                        settings_instance = None

                if settings_instance:
                    session.expunge(settings_instance)

                return settings_instance

        except Exception as e:
            local_logger = get_logger(
                "AI Runner SettingsMixin", AIRUNNER_LOG_LEVEL
            )
            local_logger.error(
                f"Error loading settings for {model_class_.__name__}: {e}. Attempting to return a new transient default instance.",
                exc_info=True,
            )
            try:
                return model_class_()
            except Exception as e_create_fallback:
                local_logger.critical(
                    f"CRITICAL: Failed to create even a fallback default instance for {model_class_.__name__} "
                    f"during error handling for the original error ({e}). Fallback creation error: {e_create_fallback}",
                    exc_info=True,
                )
                raise RuntimeError(
                    f"Fatal error in settings: Could not instantiate default for {model_class_.__name__} after initial load failed. Original error: {e}"
                ) from e_create_fallback

        return settings_instance

    def update_setting(self, model_class_, name, value):
        if model_class_.objects.first() is None:
            model_class_.objects.create()

        setting = model_class_.objects.order_by(model_class_.id.desc()).first()
        if setting:
            model_class_.objects.update(setting.id, **{name: value})
            self.__settings_updated(model_class_.__tablename__, name, value)
        else:
            self.logger.error("Failed to update settings: No setting found")

    @staticmethod
    def reset_settings():
        """
        Reset all settings to their default values by deleting all
        settings from the database. When applications are
        accessed again, they will be recreated.
        """
        settings_models = [
            ApplicationSettings,
            ActiveGridSettings,
            ControlnetSettings,
            ImageToImageSettings,
            OutpaintSettings,
            DrawingPadSettings,
            MetadataSettings,
            GeneratorSettings,
            LLMGeneratorSettings,
            SpeechT5Settings,
            EspeakSettings,
            STTSettings,
            BrushSettings,
            GridSettings,
            PathSettings,
            MemorySettings,
        ]
        for cls in settings_models:
            cls.objects.delete_all()

    @staticmethod
    def get_saved_prompt_by_id(prompt_id) -> Type[SavedPrompt]:
        return SavedPrompt.objects.filter_by_first(id=prompt_id)

    def update_saved_prompt(self, saved_prompt: SavedPrompt):
        new_saved_prompt = SavedPrompt.objects.filter_by_first(
            id=saved_prompt.id
        )
        if new_saved_prompt:
            for key in saved_prompt.__dict__.keys():
                if key != "_sa_instance_state":
                    setattr(new_saved_prompt, key, getattr(saved_prompt, key))
            new_saved_prompt.save()
        else:
            saved_prompt.save()
        self.__settings_updated()

    @staticmethod
    def create_saved_prompt(data: dict):
        new_saved_prompt = SavedPrompt(**data)
        new_saved_prompt.save()

    @staticmethod
    def load_saved_prompts() -> List[Type[SavedPrompt]]:
        return SavedPrompt.objects.all()

    @staticmethod
    def load_font_settings() -> List[Type[FontSetting]]:
        return FontSetting.objects.all()

    @staticmethod
    def get_font_setting_by_name(name) -> Type[FontSetting]:
        return FontSetting.objects.filter_by_first(name=name)

    def update_font_setting(self, font_setting: FontSetting):
        new_font_setting = FontSetting.objects.filter_by_first(
            name=font_setting.name
        )
        if new_font_setting:
            for key in font_setting.__dict__.keys():
                if key != "_sa_instance_state":
                    setattr(new_font_setting, key, getattr(font_setting, key))
            new_font_setting.save()
        else:
            font_setting.save()
        self.__settings_updated()

    @staticmethod
    def load_ai_models() -> List[Type[AIModels]]:
        return AIModels.objects.all()

    @staticmethod
    def load_chatbots() -> List[Type[Chatbot]]:
        return Chatbot.objects.all()

    @staticmethod
    def delete_chatbot_by_name(chatbot_name):
        Chatbot.objects.delete_by(name=chatbot_name)

    @staticmethod
    def create_chatbot(chatbot_name) -> Chatbot:
        # Check for existing chatbot with this name before creating
        from airunner.components.llm.data.chatbot import Chatbot

        try:
            existing = Chatbot.objects.filter_by_first(name=chatbot_name)
            if existing:
                return existing
        except Exception:
            pass  # If query fails, proceed to create new one

        try:
            new_chatbot = Chatbot(name=chatbot_name)
            new_chatbot.save()
            return new_chatbot
        except Exception:
            # If save fails, try to get existing one again
            try:
                return (
                    Chatbot.objects.filter_by_first(name=chatbot_name)
                    or Chatbot.objects.first()
                )
            except Exception:
                # Create a minimal fallback chatbot in memory
                return Chatbot(name=chatbot_name, botname="Fallback")

    def reset_path_settings(self):
        PathSettings.objects.delete_all()
        self.set_default_values(PathSettings)

    @staticmethod
    def set_default_values(model_name_):
        with session_scope() as session:
            default_values = {}
            for column in model_name_.__table__.columns:
                if column.default is not None:
                    default_values[column.name] = column.default.arg
            session.execute(model_name_.__table__.insert(), [default_values])
            session.commit()

    @staticmethod
    def load_lora() -> List[Type[Lora]]:
        return Lora.objects.all()

    @staticmethod
    def get_lora_by_name(name):
        return Lora.objects.filter_by_first(name=name)

    @staticmethod
    def add_lora(lora: Lora):
        lora.save()

    @staticmethod
    def delete_lora(lora: Lora):
        loras = Lora.objects.filter_by(name=lora.name)
        for lora in loras:
            lora.delete()

    def update_lora(self, lora: Lora):
        new_lora = Lora.objects.filter_by_first(name=lora.name)
        if new_lora:
            for key in lora.__dict__.keys():
                if key != "_sa_instance_state":
                    setattr(new_lora, key, getattr(lora, key))
            new_lora.save()
        else:
            lora.save()
        self.__settings_updated()

    def update_loras(self, loras: List[Lora]):
        for lora in loras:
            new_lora = Lora.objects.filter_by_first(name=lora.name)
            if new_lora:
                for key in lora.__dict__.keys():
                    if key != "_sa_instance_state":
                        setattr(new_lora, key, getattr(lora, key))
                new_lora.save()
            else:
                lora.save()
        self.__settings_updated()

    @staticmethod
    def create_lora(lora: Lora):
        lora.save()

    @staticmethod
    def delete_lora_by_name(lora_name, version):
        loras = Lora.objects.filter_by(name=lora_name, version=version)
        for lora in loras:
            lora.delete()

    @staticmethod
    def delete_embedding(embedding: Embedding):
        Embedding.objects.delete_by(
            name=embedding.name,
            path=embedding.path,
            branch=embedding.branch,
            version=embedding.version,
            category=embedding.category,
            pipeline_action=embedding.pipeline_action,
            enabled=embedding.enabled,
            model_type=embedding.model_type,
            is_default=embedding.is_default,
        )

    def update_embeddings(self, embeddings: List[Embedding]):
        for embedding in embeddings:
            new_embedding = Embedding.objects.filter_by_first(
                name=embedding.name,
                path=embedding.path,
                branch=embedding.branch,
                version=embedding.version,
                category=embedding.category,
                pipeline_action=embedding.pipeline_action,
                enabled=embedding.enabled,
                model_type=embedding.model_type,
                is_default=embedding.is_default,
            )
            if new_embedding:
                for key in embedding.__dict__.keys():
                    if key != "_sa_instance_state":
                        setattr(new_embedding, key, getattr(embedding, key))
                new_embedding.save()
            else:
                embedding.save()
        self.__settings_updated()

    @staticmethod
    def get_embedding_by_name(name):
        return Embedding.objects.filter_by_first(name=name)

    @staticmethod
    def add_embedding(embedding: Embedding):
        embedding.save()

    @staticmethod
    def load_prompt_templates() -> List[Type[PromptTemplate]]:
        return PromptTemplate.objects.all()

    @staticmethod
    def get_prompt_template_by_name(name) -> Type[PromptTemplate]:
        return PromptTemplate.objects.filter_by_first(template_name=name)

    @staticmethod
    def load_controlnet_models() -> List[Type[ControlnetModel]]:
        return ControlnetModel.objects.all()

    @staticmethod
    def controlnet_model_by_name(name) -> Type[ControlnetModel]:
        return ControlnetModel.objects.filter_by_first(name=name)

    @staticmethod
    def load_pipelines() -> List[Type[PipelineModel]]:
        return PipelineModel.objects.all()

    @staticmethod
    def load_shortcut_keys() -> List[Type[ShortcutKeys]]:
        return ShortcutKeys.objects.all()

    def get_chatbot_by_id(self, chatbot_id) -> Chatbot:
        if not self.settings_mixin_shared_instance.chatbot:
            try:
                # Use string names for eager loading relationships
                chatbot = Chatbot.objects.get(
                    pk=chatbot_id,
                    eager_load=[
                        "target_files",
                        "target_directories",
                    ],
                )
                if chatbot is None:
                    chatbot = self.create_chatbot("Default")
                self.settings_mixin_shared_instance.chatbot = chatbot
            except Exception as e:
                self.logger.error(f"Error getting chatbot by id: {e}")
                chatbot = self.create_chatbot("Default")
                self.settings_mixin_shared_instance.chatbot = chatbot
        return self.settings_mixin_shared_instance.chatbot

    def __settings_updated(
        self, setting_name=None, column_name=None, val=None
    ):
        if hasattr(self, "api") and self.api:
            self.api.application_settings_changed(
                setting_name=setting_name,
                column_name=column_name,
                val=val,
            )
        elif hasattr(self, "application_settings_changed"):
            self.application_settings_changed(
                setting_name=setting_name,
                column_name=column_name,
                val=val,
            )
