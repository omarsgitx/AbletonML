# AbletonML Project Structure

## Overview

AbletonML uses an **OSC and macro-based** architecture (migrated from Max for Live–only). Voice (F4 + speech) or text commands are parsed by natural language processing, mapped to actions, then executed via **OSC** (AbletonOSC) or **UI automation** (PyAutoGUI), with a simple Tk GUI for input and feedback.

## Components

### 1. App Layer
- **`app/simple_gui.py`** — Tk GUI: text input, Execute button, "Start Voice Assistant" toggle, console output, and project state panel.

### 2. Core (Python)

- **`core/osc_controller.py`** — The high-speed bridge to Ableton via the AbletonOSC Remote Script. Sends OSC over UDP (default port 11000) for set tempo, create track, and other OSC-capable actions.

- **`core/macro_controller.py`** — UI automation for searching and loading devices. Uses PyAutoGUI to open browser search (Cmd+F / Ctrl+F), type the device name, select the first result, and confirm. Used for add instrument/effect when OSC cannot do it.

- **`core/command_executor.py`** — Functional router for OSC vs. macro execution based on intent. Routes `add_instrument` and `add_effect` to the macro controller; `set_tempo`, `create_track`, `set_effect_param` to the OSC controller.

- **`core/voice_listener.py`** — Background engine for the F4 wake-key and speech-to-text transcription. Listens for the global F4 hotkey, activates the microphone, transcribes (e.g. Google Speech Recognition), then parses and executes via the command executor. Runs in a daemon thread so the GUI stays responsive.

- **`core/nlp.py`** — Natural language parsing (e.g. spaCy) of commands into intent and parameters.

- **`core/action_mapper.py`** — Maps parsed commands to a sequence of actions (set_tempo, create_track, add_instrument, add_effect, set_effect_param).

### 3. Backend (Optional)
- **`backend/`** — Flask/Socket.IO server and API for connecting an Electron or other frontend to the same core pipeline.

### 4. Electron (Optional)
- **`electron/`** — Electron app (main, renderer, styles) for an alternative GUI.

### 5. Max for Live (Legacy / Optional)
- **`max/`** — Max for Live bridge device; not required when using AbletonOSC and macros.

## Scripts & Tests

- **`full_system_check.py`** — Verifies OSC and macro paths without the microphone (set tempo via OSC, load "Reverb" via macro).
- **`test_osc.py`** — Sends sample OSC messages to AbletonOSC.
- **`test_simple_gui.py`** — GUI tests.

## Communication Flow

1. User types a command or presses **F4** and speaks.
2. (Voice) F4 → microphone → speech-to-text → same pipeline as text.
3. **NLP** parses the command; **action mapper** produces a list of actions.
4. **Command executor** routes each action: OSC for tempo/tracks, macro for add instrument/effect.
5. **OSC controller** sends UDP/OSC to AbletonOSC; **macro controller** sends keystrokes to Ableton’s UI.
6. GUI console and project state update.
