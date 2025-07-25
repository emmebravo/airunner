import enum
from enum import Enum, auto
from PySide6.QtCore import QLocale
import os


class WorkerState(Enum):
    RUNNING = 100
    PAUSED = 200
    HALTED = 300


class QueueType(Enum):
    GET_LAST_ITEM = 100
    GET_NEXT_ITEM = 200
    NONE = 300


class HandlerType(Enum):
    TRANSFORMER = 100
    DIFFUSER = 200


class FilterType(Enum):
    PIXEL_ART = "pixelart"


class ModelAction(Enum):
    NONE = auto()
    LOAD = auto()
    UNLOAD = auto()
    CLEAR = auto()
    APPLY_TO_PIPE = auto()
    GENERATE = auto()


class SignalCode(Enum):
    RUN_SCRIPT = "run_script_signal"
    BROWSER_NAVIGATE_SIGNAL = "browser_navigate_signal"
    UPATE_LOCALE = "update_locale_signal"
    RETRANSLATE_UI_SIGNAL = "retranslate_ui_signal"
    SD_UPDATE_BATCH_IMAGES_SIGNAL = "sd_update_batch_images_signal"
    SD_UPDATE_LOOSE_IMAGES_SIGNAL = "sd_update_loose_images_signal"
    CANVAS_UPDATE_IMAGE_POSITIONS = "canvas_update_image_positions"
    WIDGET_ELEMENT_CHANGED_SIGNAL = "widget_element_changed_signal"
    REFRESH_STYLESHEET_SIGNAL = "refresh_stylesheet_signal"
    NAVIGATE_TO_URL = "navigate_to_url"
    RAG_RELOAD_INDEX_SIGNAL = "rag_reload_index_signal"
    ENABLE_BRUSH_TOOL_SIGNAL = "enable_brush_tool_signal"
    ENABLE_ERASER_TOOL_SIGNAL = "enable_eraser_tool_signal"
    ENABLE_MOVE_TOOL_SIGNAL = "enable_move_tool_signal"
    INTERRUPT_PROCESS_SIGNAL = "interrupt_process_signal"
    INTERRUPT_IMAGE_GENERATION_SIGNAL = "interrupt_image_generation_signal"
    AI_MODELS_SAVE_OR_UPDATE_SIGNAL = "ai_models_save_or_update_signal"
    AI_MODEL_DELETE_SIGNAL = "ai_model_delete_signal"  # No listeners
    AI_MODELS_CREATE_SIGNAL = "ai_models_create_signal"
    APPLICATION_MAIN_WINDOW_LOADED_SIGNAL = "main_window_loaded_signal"
    APPLICATION_SETTINGS_LOADED_SIGNAL = (
        "settings_loaded_signal"  # No listeners
    )
    STATUS_MESSAGE_SIGNAL = "status_message_signal"
    APPLICATION_CLEAR_STATUS_MESSAGE_SIGNAL = "clear_status_message_signal"
    APPLICATION_RESET_SETTINGS_SIGNAL = "reset_settings_signal"
    APPLICATION_RESET_PATHS_SIGNAL = "reset_paths_signal"
    APPLICATION_STOP_SD_PROGRESS_BAR_SIGNAL = (
        "stop_image_generator_progress_bar_signal"
    )
    APPLICATION_SETTINGS_CHANGED_SIGNAL = "application_settings_changed_signal"
    APPLICATION_STATUS_INFO_SIGNAL = "status_info_signal"
    APPLICATION_STATUS_ERROR_SIGNAL = "status_error_signal"
    APPLICATION_TOOL_CHANGED_SIGNAL = "tool_changed_signal"
    APPLICATION_ACTIVE_GRID_AREA_UPDATED = "active_grid_area_updated"
    GENERATE_MASK = "generate_mask"
    MASK_GENERATOR_WORKER_RESPONSE_SIGNAL = (
        "mask_generator_worker_response_signal"
    )
    AUDIO_CAPTURE_WORKER_RESPONSE_SIGNAL = "AudioCaptureWorker_response_signal"
    AUDIO_PROCESSOR_RESPONSE_SIGNAL = "audio_processor_response_signal"
    PRESET_IMAGE_GENERATOR_DISPLAY_ITEM_MENU_SIGNAL = (
        "preset_image_generator_display_menu_signal"  # No listeners
    )
    PRESET_IMAGE_GENERATOR_ACTIVATE_BRUSH_SIGNAL = (
        "activate_brush"  # No listeners
    )
    CANVAS_LOAD_IMAGE_FROM_PATH_SIGNAL = "load_image_from_path_signal"
    SCENE_DO_DRAW_SIGNAL = "scene_do_draw_signal"
    CANVAS_CLEAR_LINES_SIGNAL = "canvas_clear_lines_signal"  # No listeners
    CANVAS_UPDATE_CURSOR = "canvas_update_cursor"
    CANVAS_ZOOM_LEVEL_CHANGED = "zoom_level_changed"
    CANVAS_CLEAR = "clear_canvas"
    CANVAS_PASTE_IMAGE_SIGNAL = "canvas_paste_image_signal"
    CANVAS_COPY_IMAGE_SIGNAL = "canvas_copy_image_signal"
    CANVAS_CUT_IMAGE_SIGNAL = "canvas_cut_image_signal"
    CANVAS_ROTATE_90_CLOCKWISE_SIGNAL = "canvas_rotate_90_clockwise_signal"
    CANVAS_ROTATE_90_COUNTER_CLOCKWISE_SIGNAL = (
        "canvas_rotate_90_counter_clockwise_signal"
    )
    CANVAS_PREVIEW_FILTER_SIGNAL = "canvas_preview_filter_signal"
    CANVAS_CANCEL_FILTER_SIGNAL = "canvas_cancel_filter_signal"
    CANVAS_APPLY_FILTER_SIGNAL = "canvas_apply_filter_signal"
    CANVAS_EXPORT_IMAGE_SIGNAL = "canvas_export_image_signal"
    CANVAS_IMPORT_IMAGE_SIGNAL = "canvas_import_image_signal"
    EMBEDDING_UPDATE_SIGNAL = "update_embedding_signal"
    EMBEDDING_DELETE_MISSING_SIGNAL = "delete_missing_embeddings_signal"
    EMBEDDING_GET_ALL_RESULTS_SIGNAL = "get_all_embeddings_results"
    ENGINE_RESPONSE_WORKER_RESPONSE_SIGNAL = (
        "EngineResponseWorker_response_signal"
    )
    GENERATOR_FORM_UPDATE_VALUES_SIGNAL = "generator_form_update_values"
    GENERATE_IMAGE_FROM_IMAGE_SIGNAL = "generate_image_from_image"
    DO_GENERATE_IMAGE_FROM_IMAGE_SIGNAL = "do_generate_image_from_image"
    LAYER_UPDATE_CURRENT_SIGNAL = "update_current_layer_signal"
    LAYERS_SHOW_SIGNAL = "show_layers_signal"
    LAYER_OPACITY_CHANGED_SIGNAL = "layers_layer_opacity_changed_signal"
    LLM_IMAGE_PROMPT_GENERATED_SIGNAL = "llm_image_prompt_generated_signal"
    # TODO: combine clear history signals - we have two by mistake
    LLM_CLEAR_HISTORY_SIGNAL = "llm_clear_history_signal"
    LLM_TEXT_STREAMED_SIGNAL = "llm_text_streamed_signal"
    LLM_TEXT_GENERATE_REQUEST_SIGNAL = "llm_text_generate_request_signal"
    LLM_TOKEN_SIGNAL = "llm_token_signal"
    LORA_UPDATE_SIGNAL = "update_lora_signal"
    LORA_UPDATED_SIGNAL = "lora_updated_signal"
    LORA_DELETE_SIGNAL = "delete_lora_signal"
    EMBEDDING_UPDATED_SIGNAL = "embedding_updated_signal"
    EMBEDDING_DELETE_SIGNAL = "delete_embedding_signal"
    SET_CANVAS_COLOR_SIGNAL = "set_canvas_color_signal"
    UPDATE_SCENE_SIGNAL = "update_scene_signal"
    DOWNLOAD_COMPLETE = "scan_for_models"
    PATH_SET = "path_set"
    SD_PROGRESS_SIGNAL = "progress_signal"
    SD_CANCEL_SIGNAL = "sd_cancel_signal"
    SD_SAVE_PROMPT_SIGNAL = "save_stablediffusion_prompt_signal"
    SD_LOAD_PROMPT_SIGNAL = "load_saved_stablediffuion_prompt_signal"
    SD_GENERATE_IMAGE_SIGNAL = "generate_image_signal"
    SD_IMAGE_GENERATED_SIGNAL = "image_generated_signal"
    SD_NSFW_CONTENT_DETECTED_SIGNAL = "nsfw_content_detected_signal"
    HANDLE_LATENTS_SIGNAL = "handle_latents_signal"
    STT_START_CAPTURE_SIGNAL = "stt_start_capture"
    STT_STOP_CAPTURE_SIGNAL = "stt_stop_capture"
    UNBLOCK_TTS_GENERATOR_SIGNAL = "unblock_tts_generator_signal"
    TTS_GENERATOR_WORKER_ADD_TO_STREAM_SIGNAL = (
        "TTSGeneratorWorker_add_to_stream_signal"
    )
    TTS_QUEUE_SIGNAL = "tts_queue_signal"
    TTS_ENABLE_SIGNAL = "tts_enable_signal"
    TTS_DISABLE_SIGNAL = "tts_disable_signal"
    QUIT_APPLICATION = "quit"
    TOGGLE_FULLSCREEN_SIGNAL = "fullscreen_signal"
    TOGGLE_TTS_SIGNAL = "toggle_tts_signal"
    TOGGLE_SD_SIGNAL = "toggle_sd_signal"
    TOGGLE_LLM_SIGNAL = "toggle_llm_signal"
    START_AUTO_IMAGE_GENERATION_SIGNAL = "start_auto_image_generation_signal"
    STOP_AUTO_IMAGE_GENERATION_SIGNAL = "stop_auto_image_generation_signal"
    DO_GENERATE_SIGNAL = "do_generate_signal"
    BASH_EXECUTE_SIGNAL = "bash_execute_signal"
    WRITE_FILE = "write_file_signal"
    ADD_CHATBOT_MESSAGE_SIGNAL = "add_chatbot_message_signal"
    DOWNLOAD_PROGRESS = "download_progress"
    UPDATE_DOWNLOAD_LOG = "update_download_log"
    CLEAR_DOWNLOAD_STATUS_BAR = "clear_download_status_bar"
    SET_DOWNLOAD_STATUS_LABEL = "set_download_status_label"
    CHANGE_SCHEDULER_SIGNAL = "change_scheduler_signal"
    LOG_LOGGED_SIGNAL = "log_logged_signal"
    MODEL_STATUS_CHANGED_SIGNAL = "model_status_changed_signal"

    STT_LOAD_SIGNAL = "stt_load_signal"
    STT_UNLOAD_SIGNAL = "stt_unload_signal"
    LLM_LOAD_SIGNAL = "llm_load_signal"
    LLM_UNLOAD_SIGNAL = "llm_unload_signal"
    SD_LOAD_SIGNAL = "load_stablediffusion_signal"
    SD_UNLOAD_SIGNAL = "unload_stablediffusion_signal"
    SD_ART_MODEL_CHANGED = "reload_stablediffusion_signal"
    LLM_MODEL_CHANGED = "llm_model_changed_signal"
    RAG_LOAD_DOCUMENTS = "rag_load_documents_signal"
    CONTROLNET_LOAD_SIGNAL = "load_controlnet_signal"
    CONTROLNET_UNLOAD_SIGNAL = "unload_controlnet_signal"
    SAFETY_CHECKER_LOAD_SIGNAL = "SAFETY_CHECKER_LOAD_SIGNAL"
    SAFETY_CHECKER_UNLOAD_SIGNAL = "SAFETY_CHECKER_UNLOAD_SIGNAL"

    BRUSH_COLOR_CHANGED_SIGNAL = "brush_color_changed_signal"

    HISTORY_CLEAR_SIGNAL = "history_clear_signal"
    UNDO_SIGNAL = "undo_signal"
    REDO_SIGNAL = "redo_signal"
    QUEUE_LOAD_CONVERSATION = "queue_load_conversation_signal"
    LOAD_CONVERSATION = "load_conversation_signal"
    BOT_MOOD_UPDATED = "bot_mood_updated_signal"
    CHATBOT_CHANGED = "chatbot_changed_signal"
    CONVERSATION_DELETED = "conversation_deleted_signal"

    KEYBOARD_SHORTCUTS_UPDATED = "keyboard_shortcuts_updated_signal"
    LORA_STATUS_CHANGED = "lora_status_changed"
    EMBEDDING_STATUS_CHANGED = "embedding_status_changed"

    MASK_LAYER_TOGGLED = "mask_layer_toggled"
    MASK_UPDATED = "mask_updated"
    HISTORY_UPDATED = "history_updated"
    CANVAS_IMAGE_UPDATED_SIGNAL = "canvas_image_updated_signal"

    UNLOAD_NON_SD_MODELS = "unload_non_sd_models"
    LOAD_NON_SD_MODELS = "load_non_sd_models"

    SD_PIPELINE_LOADED_SIGNAL = "sd_pipeline_loaded_signal"
    MISSING_REQUIRED_MODELS = "missing_required_models"

    DELETE_MESSAGES_AFTER_ID = "delete_messages_after_id"
    TTS_MODEL_CHANGED = "tts_model_changed"

    TOGGLE_TOOL = "toggle_tool"
    TOGGLE_GRID = "toggle_grid"

    SECTION_CHANGED = "section_changed"

    WEB_BROWSER_PAGE_HTML = "web_browser_page_html"

    CLEAR_PROMPTS = "clear_prompts"

    WIDGET_ELEMENT_CHANGED = "widget_element_changed"
    SD_ADDITIONAL_PROMPT_DELETE_SIGNAL = "sd_additional_prompt_delete_signal"
    RECENTER_GRID_SIGNAL = "recenter_grid_signal"
    LLM_TEXT_STREAM_PROCESS_SIGNAL = "llm_text_stream_process_signal"
    SHOW_WINDOW_SIGNAL = "show_window_signal"
    SHOW_DYNAMIC_UI_FROM_STRING_SIGNAL = "show_dynamic_ui_from_string_signal"
    VOICE_SAVED = "voice_saved"
    PLAYBACK_DEVICE_CHANGED = "playback_device_changed"
    RECORDING_DEVICE_CHANGED = "recording_device_changed"
    NODE_EXECUTION_COMPLETED_SIGNAL = "node_execution_completed_signal"
    CLEAR_WORKFLOW_SIGNAL = "clear_workflow_signal"
    WORKFLOW_LOAD_SIGNAL = "workflow_load_signal"
    REGISTER_GRAPH_SIGNAL = "register_graph_signal"
    ENABLE_WORKFLOWS_TOGGLED = "enable_workflows_toggled"
    SEND_IMAGE_TO_CANVAS_SIGNAL = "send_image_to_canvas_signal"
    RUN_WORKFLOW_SIGNAL = "run_workflow_signal"
    STOP_WORKFLOW_SIGNAL = "stop_workflow_signal"
    WORKFLOW_EXECUTION_COMPLETED_SIGNAL = "workflow_execution_completed_signal"
    PAUSE_WORKFLOW_SIGNAL = "pause_workflow_signal"
    INPUT_IMAGE_SETTINGS_CHANGED = "input_image_settings_changed"

    # Video generation signals
    VIDEO_LOAD_SIGNAL = "video_load_signal"
    VIDEO_UNLOAD_SIGNAL = "video_unload_signal"
    VIDEO_GENERATE_SIGNAL = "video_generate_signal"
    VIDEO_GENERATED_SIGNAL = "video_generated_signal"
    INTERRUPT_VIDEO_GENERATION_SIGNAL = "interrupt_video_generation_signal"
    VIDEO_PROGRESS_SIGNAL = "video_progress_signal"
    VIDEO_FRAME_UPDATE_SIGNAL = "video_frame_update_signal"
    NODEGRAPH_ZOOM = "nodegraph_zoom"
    NODEGRAPH_PAN = "nodegraph_pan"
    LLM_MODEL_DOWNLOAD_PROGRESS = "llm_model_download_progress"
    MOOD_SUMMARY_UPDATE_STARTED = "mood_summary_update_started_signal"
    BROWSER_EXTRA_CONTEXT = "browser_extra_context_signal"
    WIDGET_COMMAND_SIGNAL = "widget_command_signal"

    # file explorer
    FILE_EXPLORER_OPEN_FILE = "open_file_signal"
    INDEX_DOCUMENT = "index_document_signal"
    DOCUMENT_INDEXED = "document_indexed_signal"


class EngineResponseCode(Enum):
    NONE = 0
    STATUS = 100
    ERROR = 200
    WARNING = 300
    PROGRESS = 400
    IMAGE_GENERATED = 500
    CONTROLNET_IMAGE_GENERATED = 501
    MASK_IMAGE_GENERATED = 502
    EMBEDDING_LOAD_FAILED = 600
    TEXT_GENERATED = 700
    TEXT_STREAMED = 701
    CAPTION_GENERATED = 800
    ADD_TO_CONVERSATION = 900
    CLEAR_MEMORY = 1000
    NSFW_CONTENT_DETECTED = 1100
    INSUFFICIENT_GPU_MEMORY = 1200
    INTERRUPTED = 1300


class Scheduler(Enum):
    EULER_ANCESTRAL = "Euler a"
    EULER = "Euler"
    LMS = "LMS"
    HEUN = "Heun"
    DPM = "DPM"
    DPM2 = "DPM2"
    DPM_PP_2M = "DPM++ 2M"
    DPM2_K = "DPM2 Karras"
    DPM2_A_K = "DPM2 a Karras"
    DPM_PP_2M_K = "DPM++ 2M Karras"
    DPM_PP_2M_SDE_K = "DPM++ 2M SDE Karras"
    DDIM = "DDIM"
    UNIPC = "UniPC"
    DDPM = "DDPM"
    DEIS = "DEIS"
    DPM_2M_SDE_K = "DPM 2M SDE Karras"
    PLMS = "PLMS"
    # DDIMInverse = "DDIM Inverse"
    # IPNM = "IPNM"
    # REPAINT = "RePaint"
    # KVE = "Karras Variance exploding"
    # VESDE = "VE-SDE"
    # VPSDE = "VP-SDE"
    # VQDIFFUSION = "VQ Diffusion"


class Mode(Enum):
    IMAGE = "Image Generation"
    LANGUAGE_PROCESSOR = "Language Processing"
    MODEL_MANAGER = "Model Manager"


class LLMActionType(Enum):
    """
    The following action types are used by the LLM to process various user
    requests. The default action type is "APPLICATION_COMMAND". This is used when the user
    wants to interact with a chatbot. When this is combined with the
    use_tool_flter flag, the LLM will attempt to determine which action to take
    based on the user's words.
    """

    # DO_NOT_RESPOND = "DO NOTHING: Choose this action if none of the other actions apply to the user's request."
    NONE = "None"
    CHAT = "RESPOND: Choose this action if you want to respond to the user."
    GENERATE_IMAGE = (
        "GENERATE IMAGE: Choose this action if you want to generate an image."
    )
    APPLICATION_COMMAND = "APPLICATION_COMMAND"
    UPDATE_MOOD = "UPDATE_MOOD"
    QUIT_APPLICATION = "QUIT APPLICATION: If the users requests that you quit the application, choose this action."
    TOGGLE_FULLSCREEN = "TOGGLE FULLSCREEN: If the user requests to toggle fullscreen mode, choose this action."
    TOGGLE_TTS = (
        "TOGGLE TEXT-TO-SPEECH: If the user requests that you turn on or off or toggle text-to-speech, "
        "choose this action."
    )
    PERFORM_RAG_SEARCH = "SEARCH: If the user requests that you search for information, choose this action."
    SUMMARIZE = "SUMMARIZE"
    DO_NOTHING = (
        "DO NOTHING: If the user's request is unclear or you are unable to determine the user's intent, "
        "choose this action."
    )
    GET_WEATHER = "get_weather"
    STORE_DATA = "store_data"
    SEARCH = "search"
    DECISION = "decision"

    BROWSER = "browser"
    CODE = "code"
    WORKFLOW = "workflow"

    FILE_INTERACTION = "file_interaction"
    WORKFLOW_INTERACTION = "workflow_interaction"


class CanvasToolName(Enum):
    ACTIVE_GRID_AREA = "active_grid_area"
    BRUSH = "brush"
    ERASER = "eraser"
    SELECTION = "selection"
    GRID = "grid"
    TEXT = "text"
    NONE = "none"


class ImageGenerator(Enum):
    STABLEDIFFUSION = "stablediffusion"


class GeneratorSection(Enum):
    TXT2IMG = "txt2img"
    IMG2IMG = "img2img"
    INPAINT = "inpaint"
    OUTPAINT = "outpaint"


class StableDiffusionVersion(Enum):
    NONE = "None"
    SDXL1_0 = "SDXL 1.0"
    SDXL_TURBO = "SDXL Turbo"
    SDXL_LIGHTNING = "SDXL Lightning"
    SDXL_HYPER = "SDXL Hyper"
    SD1_5 = "SD 1.5"
    FLUX_S = "Flux S"


class Language(Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"


class CanvasType(Enum):
    BRUSH = "brush"
    IMAGE = "image"
    CONTROLNET = "controlnet"
    OUTPAINT = "outpaint"


class Controlnet(Enum):
    CANNY = "canny"


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"


class ModelStatus(Enum):
    UNLOADED = "Unloaded"
    LOADED = "Loaded"
    READY = "Ready"
    LOADING = "Loading"
    FAILED = "Failed"


class StatusColors(Enum):
    LOADED = "#00ff00"
    READY = "#00ffff"
    LOADING = "#ffff00"
    FAILED = "#ff0000"
    UNLOADED = "#c0c0c0"


class ModelType(Enum):
    LORA = "Lora"
    EMBEDDINGS = "Embeddings"
    SD = "SD Model"
    FLUX_MODEL = "Flux Model"
    SD_VAE = "SD VAE"
    SD_UNET = "SD UNet"
    SD_TOKENIZER = "SD Tokenizer"
    SD_TEXT_ENCODER = "SD Text Encoder"
    TTS = "TTS Model"
    TTS_PROCESSOR = "TTS Processor"
    TTS_FEATURE_EXTRACTOR = "TTS Feature Extractor"
    TTS_VOCODER = "TTS Vocoder"
    TTS_SPEAKER_EMBEDDINGS = "TTS Speaker Embeddings"
    TTS_TOKENIZER = "TTS Tokenizer"
    TTS_DATASET = "TTS Dataset"
    STT = "STT Model"
    STT_PROCESSOR = "STT Processor"
    STT_FEATURE_EXTRACTOR = "STT Feature Extractor"
    CONTROLNET = "SD Controlnet"
    CONTROLNET_PROCESSOR = "SD Controlnet Processor"
    SAFETY_CHECKER = "SD Safety Checker"
    FEATURE_EXTRACTOR = "SD Feature Extractor"
    SCHEDULER = "SD Scheduler"
    LLM = "LLM Model"
    LLM_TOKENIZER = "LLM Tokenizer"
    VIDEO = "Video Model"


class HandlerState(Enum):
    UNINITIALIZED = "Uninitialized"
    INITIALIZED = "Initialized"
    LOADING = "Loading"
    READY = "Ready"
    GENERATING = "Generating"
    PREPARING_TO_GENERATE = "Preparing to Generate"
    ERROR = "Error"


class TTSModel(Enum):
    ESPEAK = "Espeak"
    SPEECHT5 = "SpeechT5"
    OPENVOICE = "OpenVoice"


class ImagePreset(Enum):
    NONE = ""
    ILLUSTRATION = "Illustration"
    PHOTOGRAPH = "Photograph"
    PAINTING = "Painting"


class SpeechT5Voices(Enum):
    US_MALE = "US Male"
    US_MALE_2 = "US Male 2"
    US_FEMALE = "US Female"
    US_FEMALE_2 = "US Female 2"
    CANADIAN_MALE = "Canadian Male"
    SCOTTISH_MALE = "Scottish Male"
    INDIAN_MALE = "Indian Male"


class AvailableLanguage(enum.Enum):
    """
    Enum for available languages in OpenVoice.
    """

    AUTO = "Automatic"
    EN = "EN"
    ES = "ES"
    FR = "FR"
    ZH = "ZH"
    ZH_MIX_EN = "ZH_MIX_EN"
    JP = "JP"
    KR = "KR"
    SP = "SP"


LANGUAGE_DISPLAY_MAP = {
    AvailableLanguage.AUTO: "Automatic",
    AvailableLanguage.EN: "English",
    AvailableLanguage.ES: "Spanish",
    AvailableLanguage.FR: "French",
    AvailableLanguage.ZH: "Chinese",
    AvailableLanguage.ZH_MIX_EN: "Chinese (Mixed English)",
    AvailableLanguage.JP: "Japanese",
    AvailableLanguage.KR: "Korean",
    AvailableLanguage.SP: "Spanish",
}
LANGUAGE_TO_LOCALE_MAP = {
    AvailableLanguage.EN: QLocale.English,
    AvailableLanguage.ES: QLocale.Spanish,
    AvailableLanguage.FR: QLocale.French,
    AvailableLanguage.ZH: QLocale.Chinese,
    AvailableLanguage.ZH_MIX_EN: QLocale.Chinese,
    AvailableLanguage.JP: QLocale.Japanese,
    AvailableLanguage.KR: QLocale.Korean,
    AvailableLanguage.SP: QLocale.Spanish,
}
LOCALE_TO_LANGUAGE_MAP = {
    QLocale.English: AvailableLanguage.EN,
    QLocale.Spanish: AvailableLanguage.ES,
    QLocale.French: AvailableLanguage.FR,
    QLocale.Chinese: AvailableLanguage.ZH,
    QLocale.Japanese: AvailableLanguage.JP,
    QLocale.Korean: AvailableLanguage.KR,
}
AVAILABLE_LANGUAGES = {
    "gui_language": [
        AvailableLanguage.EN,
        AvailableLanguage.JP,
    ],
    "user_language": [
        lang
        for lang in AvailableLanguage
        if lang
        not in (
            AvailableLanguage.EN,
            AvailableLanguage.ZH_MIX_EN,
        )
    ],
    "bot_language": [
        lang
        for lang in AvailableLanguage
        if lang
        not in (
            AvailableLanguage.EN,
            AvailableLanguage.ZH_MIX_EN,
        )
    ],
}


class ModelService(enum.Enum):
    LOCAL = "local"
    HUGGINGFACE = "huggingface"
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"


class QualityEffects(enum.Enum):
    CUSTOM = "Custom"
    STANDARD = "Standard"
    LOW_RESOLUTION = "Low Resolution"
    HIGH_RESOLUTION = "High Resolution"
    SUPER_SAMPLE_X2 = "Super Sample x2"
    SUPER_SAMPLE_X4 = "Super Sample x4"
    SUPER_SAMPLE_X8 = "Super Sample x8"


class Quantize(enum.Enum):
    NONE = "None"
    EIGHT_BIT = "8-bit"
    FOUR_BIT = "4-bit"


def _get_available_templates():
    """
    Dynamically scan the styles directory for available themes and return a dict for Enum creation.
    """
    styles_dir = os.path.join(os.path.dirname(__file__), "gui", "styles")
    templates = {"SYSTEM_DEFAULT": "System Default"}
    if os.path.isdir(styles_dir):
        for entry in os.listdir(styles_dir):
            if entry.endswith("_theme") and os.path.isdir(
                os.path.join(styles_dir, entry)
            ):
                key = entry.replace("_theme", "").upper()
                display = entry.replace("_theme", "").capitalize()
                templates[key] = display
    return templates


TemplateName = enum.Enum("TemplateName", _get_available_templates())
