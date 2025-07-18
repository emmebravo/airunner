# Main Window Tab Persistence

## Purpose

The main window now persists the active tab across application restarts. When the user changes tabs, the active tab index is stored in application settings. On startup, the last active tab is restored automatically.

## Implementation
- The active tab index is stored in `QSettings` under the `window_settings` group with the key `active_main_tab_index`.
- On tab change, the index is updated in settings.
- On startup, the main window reads this value and restores the corresponding tab (if valid).

## Usage
No user action is required. The last active tab will be restored automatically when the application is launched again.

---

# ModelLoadBalancer

## Purpose

`ModelLoadBalancer` orchestrates the loading and unloading of AI models (LLM, TTS, STT, SD) to optimize VRAM usage and enable seamless switching between art (image generation) and non-art (text, speech) modes in AI Runner.

## Key Features
- Tracks which models are loaded/unloaded.
- Delegates actual load/unload to the appropriate worker manager(s).
- Remembers which non-art models were loaded before switching to art mode, and restores them after.
- Can be extended to use VRAM stats and model size for smarter balancing.

## API
- `switch_to_art_mode()`: Unloads all non-art models (LLM, TTS, STT) and loads Stable Diffusion.
- `switch_to_non_art_mode()`: Reloads previously unloaded non-art models.
- `get_loaded_models()`: Returns a list of currently loaded models.
- `vram_stats(device)`: Returns VRAM stats for a given device.

## Usage

Instantiate with a `WorkerManager`:

```python
from airunner.components.application.gui.windows.main.model_load_balancer import
    ModelLoadBalancer

balancer = ModelLoadBalancer(worker_manager, logger=logger)
```

Switch to art mode (for image generation):
```python
balancer.switch_to_art_mode()
```

Switch back to non-art mode (for LLM, TTS, STT):
```python
balancer.switch_to_non_art_mode()
```

## Extending
- To add smarter VRAM/model size balancing, extend `switch_to_art_mode` and `switch_to_non_art_mode` to use `vram_stats` and model size info.
- For more granular control, add methods for individual model types.

## Tests
See `tests/model_load_balancer/test_model_load_balancer.py` for TDD and usage examples.
