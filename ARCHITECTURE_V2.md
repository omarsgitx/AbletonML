# AbletonML v2: Architectural Pivot & Implementation Plan

## Project Goal
We are transitioning AbletonML from a prototype to a robust accessibility add-on for Ableton Live. The goal is to allow visually impaired or motor-impaired users to control Ableton completely via voice/natural language, without needing to drag-and-drop devices onto tracks.

## The Pivot: From Max for Live to Control Surface Script
**We are deprecating the Max for Live (M4L) approach.**
* **Old Architecture:** Electron Frontend -> Python Backend -> UDP -> Max for Live Device.
* **New Architecture:** Python Backend -> OSC (Open Sound Control) -> AbletonOSC (Remote Script).

**Why?**
1.  **Always On:** Remote scripts run automatically when Ableton starts.
2.  **Global Scope:** We need access to global commands (Save, Undo, Browser) that M4L handles poorly.
3.  **Zero Friction:** The user should not have to load a device to use accessibility features.

## Technical Stack & Dependencies

### 1. The Bridge: AbletonOSC
Instead of writing a Control Surface script from scratch, we will use [AbletonOSC](https://github.com/ideoforms/AbletonOSC).
* **Action:** We need to install the `AbletonOSC` remote script into Ableton's MIDI Remote Scripts folder.
* **Protocol:** Our Python backend will send OSC messages (e.g., `/live/song/create_midi_track`) to localhost on port 11000.

### 2. The Brain: Python Backend (Existing)
We will keep the `core/` logic but refactor the output layer.
* **Keep:** `core/nlp.py` (The logic that parses "add reverb" is still valid).
* **Refactor:** `core/max_controller.py` -> Rename to `core/osc_controller.py`.
* **New Dependency:** `python-osc` library for sending messages.

### 3. Voice & Input Layer (New)
* **Global Hotkey:** Use the `keyboard` library to listen for a wake key (e.g., F1 or Caps Lock) regardless of focus.
* **STT (Speech-to-Text):** Integrate `SpeechRecognition` or OpenAI Whisper locally to convert voice to text, which is then fed into `nlp.py`.

## Implementation Roadmap

### Phase 1: The Connection
1.  Install `python-osc`.
2.  Create a test script `test_osc.py` that sends a simple command (e.g., stop/start playback) to Ableton via AbletonOSC.
3.  Verify Ableton responds without any M4L device loaded.

### Phase 2: Refactoring the Backend
1.  Rename `max_controller.py` to `osc_controller.py`.
2.  Rewrite the `send_command` function to map our internal intent (e.g., `intent: create_track`) to the specific OSC address required by AbletonOSC (e.g., `/live/song/create_midi_track`).

### Phase 3: The "Ear"
1.  Create a `voice_listener.py` module.
2.  Implement a loop that waits for a specific hotkey press.
3.  On press, record audio -> transcribe to text -> send text to `nlp.py`.

## Instructions for AI Assistant (Cursor)
* Reference this file to understand the project scope.
* Do not suggest Max for Live solutions.
* Prioritize `python-osc` and `AbletonOSC` syntax for all control logic.
* Keep the existing `nlp.py` logic; we are only changing the *execution* method.