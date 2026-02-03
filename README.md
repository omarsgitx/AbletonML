# AbletonML

AbletonML is an accessibility-focused interface for Ableton Live: control your session with **voice** (F4 wake key + speech) or **text** using natural language. Commands like "set tempo to 120" or "add reverb" are routed over OSC (AbletonOSC) and automated macros (PyAutoGUI) so you can work hands-free.

## Features

- **Voice control**: Press F4, speak a command; speech is transcribed and executed (text input also supported).
- **Natural language**: Type or say "create midi track", "set tempo to 125", "add reverb to track 2".
- **OSC + macro backend**: OSC for transport, tempo, and track creation; UI automation for searching and loading instruments/effects via Ableton’s browser.
- **Command routing**: Intent is routed to the right backend (OSC vs. macro) automatically.
- **Simple GUI**: Tk-based app with console output, project state, and a "Start Voice Assistant" toggle.
- Real-time project state visualization.

## Requirements

- macOS (tested on macOS 11+)
- Ableton Live 11 or 12 with **AbletonOSC** enabled (Preferences → Link/Tempo/MIDI). Max for Live is optional.
- Python 3.9+

### OS Permissions (macOS)

For the **voice assistant** (F4 hotkey) and **macro actions** (e.g. Add Instrument / Add Effect via browser) to work, grant **Accessibility** permission to the app that runs Python (Terminal, iTerm, Cursor, VS Code, etc.):

1. Open **System Settings** → **Privacy & Security** → **Privacy** → **Accessibility**.
2. Add your **Terminal** (or **Cursor** / **Code**) and enable the toggle.

Without this, the global F4 key may not be detected when the app is in the background, and PyAutoGUI may not send keystrokes to Ableton.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/AbletonML.git
   cd AbletonML
   ```

2. Install Python dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # macOS: if you get tkinter errors:
   brew install python-tk@3.13
   ```

3. Enable AbletonOSC in Ableton Live:
   - **Live** → **Preferences** → **Link/Tempo/MIDI** → under "Control Surface", select **AbletonOSC** (listens on port 11000).

4. (Optional) Node.js and Electron for the Electron GUI:
   ```
   npm install
   ```

## Usage

### Quick Start
1. Start the simple GUI:
   ```bash
   source venv/bin/activate
   python app/simple_gui.py
   ```

2. Type commands (e.g. "set tempo to 120", "create midi track", "add reverb to track 2") and press Enter or click **Execute**.

3. Click **Start Voice Assistant**, then press **F4** and speak a command. Feedback appears in the console.

### Example Commands

- **Tempo:** "set tempo to 120", "change bpm to 90"
- **Tracks:** "create midi track", "create audio track"
- **Instruments:** "add piano", "add synth", "add drums"
- **Effects:** "add reverb to track 2", "add delay to track 1"
- **Parameters:** "set reverb dry/wet to 30%", "set delay mix to 50"

## Architecture

The system has moved from a Max for Live–only setup to an **OSC and macro-based** pipeline:

- **`core/osc_controller.py`** — High-speed bridge to Ableton via the AbletonOSC Remote Script. Sends OSC over UDP (port 11000) for set tempo, create track, and other OSC-capable actions.

- **`core/macro_controller.py`** — UI automation for searching and loading devices. Uses PyAutoGUI to open Ableton’s browser search, type the device name, and select the first result (used when OSC cannot add instruments/effects).

- **`core/command_executor.py`** — Functional router: chooses OSC vs. macro execution based on intent. Routes `add_instrument` and `add_effect` to the macro controller; `set_tempo`, `create_track`, and `set_effect_param` to the OSC controller.

- **`core/voice_listener.py`** — Background engine for the F4 wake-key and speech-to-text. Listens for the global F4 hotkey, captures microphone input, transcribes (e.g. Google Speech Recognition), then parses and executes via the command executor.

- **`core/nlp.py`** and **`core/action_mapper.py`** — Natural language parsing and mapping of parsed commands to a sequence of actions.

## Communication Flow

1. User types a command or presses F4 and speaks.
2. (Voice path) F4 → microphone → speech-to-text → same pipeline as text.
3. NLP parses the command; action mapper produces a list of actions.
4. Command executor routes each action: OSC for tempo/tracks, macro for add instrument/effect.
5. OSC controller sends UDP/OSC to AbletonOSC; macro controller sends keystrokes to Ableton’s UI.
6. GUI console and project state update.

## Troubleshooting

### Tkinter Import Error (macOS)
```bash
brew install python-tk@3.13
# Recreate venv if needed, then pip install -r requirements.txt
```

### OSC / Ableton Not Responding
- Ensure AbletonOSC is selected in Live → Preferences → Link/Tempo/MIDI.
- Port 11000 must be free; restart Live and the app if needed.

### Voice or Macro Not Working
- Grant **Accessibility** to Terminal/IDE (see OS Permissions above).
- For voice: check microphone permissions and that you pressed F4 before speaking.

### Testing Without a Microphone
Run the full system check (OSC + macro only):
```bash
python full_system_check.py
```

## Development

### Project Structure

- `app/` — Simple Tk GUI (`simple_gui.py`).
- `core/` — Core logic: `osc_controller.py`, `macro_controller.py`, `command_executor.py`, `voice_listener.py`, `nlp.py`, `action_mapper.py`.
- `backend/` — Optional Flask/Socket.IO server for Electron frontend.
- `electron/` — Optional Electron frontend.
- `max/` — Legacy Max for Live device files (optional when using AbletonOSC).

### Adding New Commands

1. Update `core/nlp.py` to recognize the new command.
2. Add a mapping in `core/action_mapper.py`.
3. Implement the action in `core/osc_controller.py` (OSC) or use `core/macro_controller.py` (UI automation) and route it in `core/command_executor.py`.

## License

MIT

## Acknowledgements

- [Ableton Live](https://www.ableton.com/en/live/)
- [AbletonOSC](https://github.com/ideoforms/AbletonOSC)
- [Electron](https://www.electronjs.org/)
- [spaCy](https://spacy.io/)
