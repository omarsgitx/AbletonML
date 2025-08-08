# AbletonML

AbletonML is a natural language interface for controlling Ableton Live. It allows you to control Ableton Live using simple English commands like "create a midi track with piano" or "set tempo to 120 BPM".

## Features

- Control Ableton Live using natural language commands
- Modern Electron-based GUI
- Max for Live integration
- Real-time project state visualization

## Requirements

- macOS (tested on macOS 11+)
- Ableton Live 11 or 12 with Max for Live
- Node.js 14+ and npm
- Python 3.9+

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/AbletonML.git
   cd AbletonML
   ```

2. Install Python dependencies:
   ```bash
   # Create virtual environment (recommended)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # For macOS users: If you get tkinter errors, install:
   brew install python-tk@3.13
   ```

3. Install Node.js dependencies (for Electron GUI):
   ```
   npm install
   ```

4. Set up the Max for Live device:
   - Open the `max/AbletonML_Bridge.maxpat` file in Max
   - Export it as a Max for Live device (see instructions in `max/export_to_amxd.txt`)
   - Load the device into a MIDI track in Ableton Live

## Usage

### Quick Start (Recommended)
1. Start the simple test GUI:
   ```bash
   source venv/bin/activate
   python test_simple_gui.py
   ```

2. Type commands like:
   - `set tempo to 120`
   - `create midi track`
   - `add piano`
   - `add reverb to track 2`

### Full Setup with Ableton Live
1. Start Ableton Live and load the AbletonML_Bridge device on a MIDI track.

2. Start the AbletonML application:
   ```bash
   # Option 1: Simple GUI (faster)
   python app/simple_gui.py
   
   # Option 2: Electron GUI
   npm start
   ```

3. Type natural language commands in the input field and press Enter or click "Execute".

### Example Commands

#### Tempo Control
- `"set tempo to 120"`
- `"change bpm to 90"`
- `"set bpm to 140"`
- `"adjust tempo to 80"`

#### Track Creation
- `"create midi track"`
- `"create audio track"`
- `"add audio track"`
- `"make midi track"`

#### Instruments
- `"add piano"`
- `"add synth"`
- `"add drums"`

#### Effects
- `"add reverb to track 2"`
- `"add delay to track 1"`
- `"add echo to track 3"`
- `"add compressor to track 4"`

## Architecture

AbletonML consists of several components:

1. **Electron Frontend**: A modern GUI for entering commands and visualizing the project state.

2. **Python Backend**: Processes natural language commands and communicates with Ableton Live.
   - NLP Module: Parses natural language commands
   - Action Mapper: Maps parsed commands to actions
   - Max Controller: Sends commands to Max for Live

3. **Max for Live Device**: Receives commands from the Python backend and controls Ableton Live.

## Communication Flow

1. User enters a command in the Electron frontend
2. Command is sent to the Python backend via Socket.IO
3. NLP module parses the command
4. Action mapper converts the parsed command to actions
5. Max controller sends the actions to the Max for Live device via UDP
6. Max for Live device executes the actions in Ableton Live
7. Updated project state is sent back to the frontend

## Troubleshooting

### Tkinter Import Error (macOS)
```bash
# Install tkinter support
brew install python-tk@3.13
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Max for Live Device Not Receiving Commands
- Make sure the Max for Live device is loaded in Ableton Live
- Check that UDP port 7400 is not blocked by a firewall
- Restart the AbletonML application and Ableton Live

### Commands Not Being Recognized
- Try using simpler commands
- Check the exact wording in the example commands
- Make sure the NLP module is properly initialized

### Testing Without Ableton Live
The system works in simulation mode when Ableton Live is not connected:
```bash
python test_simple_gui.py
```

## Development

### Project Structure

- `electron/`: Electron frontend files
- `backend/`: Python backend server
- `core/`: Core modules (NLP, action mapper, controller)
- `max/`: Max for Live device files

### Adding New Commands

To add support for new commands:

1. Update the NLP module in `core/nlp.py` to recognize the new command
2. Add a mapping function in `core/action_mapper.py`
3. Implement the action in `core/max_controller.py`
4. Update the Max for Live device to handle the new action

## License

MIT

## Acknowledgements

- [Ableton Live](https://www.ableton.com/en/live/)
- [Max for Live](https://www.ableton.com/en/live/max-for-live/)
- [Electron](https://www.electronjs.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Socket.IO](https://socket.io/)
- [spaCy](https://spacy.io/) 