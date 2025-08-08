# Changelog

## [2025-08-08] - Major Fixes and Working Prototype

### 🔧 Critical Fixes
- **FIXED**: Tkinter import error on macOS by installing `python-tk@3.13`
- **FIXED**: NLP parsing bug where 'add reverb to track 2' created new tracks instead of adding effects
- **FIXED**: Import error in `simple_gui.py` (`ableton_controller` → `max_controller`)

### 🎯 New Features
- **ADDED**: Simple NLP module (`core/simple_nlp.py`) for testing without spaCy dependency
- **ADDED**: UDP communication test script (`test_max_communication.py`)
- **ADDED**: NLP parsing test script (`test_nlp_fix.py`)
- **ADDED**: Simple test GUI (`test_simple_gui.py`) for rapid testing

### 🔍 Technical Improvements
- **IMPROVED**: NLP parsing logic to correctly distinguish between:
  - `'add reverb to track 2'` → `add_effect` intent
  - `'add piano'` → `create` intent (instrument)
  - `'create midi track'` → `create` intent (track)
- **IMPROVED**: Command pattern matching to avoid conflicts
- **IMPROVED**: Error handling and logging throughout the pipeline

### ✅ Current Status
- **WORKING**: Full command pipeline (NLP → Action Mapper → Max Controller → UDP)
- **WORKING**: Tkinter GUI with real-time project state updates
- **WORKING**: UDP communication with Max for Live device
- **WORKING**: Simulation mode when Max for Live not connected
- **WORKING**: All basic commands: tempo, track creation, instruments, effects

### 🎵 Supported Commands
#### Tempo Control
- `'set tempo to 120'` / `'change bpm to 90'` / `'set bpm to 140'`

#### Track Creation
- `'create midi track'` / `'create audio track'` / `'add audio track'`

#### Instruments
- `'add piano'` / `'add synth'` / `'add drums'`

#### Effects
- `'add reverb to track 2'` / `'add delay to track 1'` / `'add echo to track 3'`

### 🚀 Ready for
- Testing with Ableton Live and Max for Live device
- Electron GUI deployment
- Additional command expansion

## Previous Versions
- Initial project setup with basic architecture
- Max for Live device implementation
- Python backend with NLP and action mapping
- Electron frontend interface
