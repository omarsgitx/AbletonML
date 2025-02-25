# AbletonML Project Structure

## Components

### 1. Max for Live Bridge Device
- `AbletonML_Bridge.amxd` - Max for Live device that interfaces with Ableton
- Handles UDP communication with the macOS app
- Directly controls Ableton parameters using live.object
- Sends feedback to the app

### 2. macOS App (Electron-based)
- `app/` - Directory containing the Electron app
  - `main.js` - Main Electron process
  - `renderer.js` - UI logic
  - `index.html` - App interface
  - `styles.css` - App styling
  - `package.json` - Dependencies and build config

### 3. Python Backend (reusing our existing code)
- `backend/` - Directory containing Python backend
  - `nlp.py` - NLP module (from our existing code)
  - `action_mapper.py` - Action mapper (from our existing code)
  - `max_controller.py` - New module to send commands to Max via UDP
  - `server.py` - Simple server to connect the Electron app to our Python backend

## Communication Flow

1. User types command in macOS app
2. Electron app sends command to Python backend
3. Python backend parses command using NLP module
4. Action mapper converts parsed command to actions
5. Max controller sends actions to Max for Live device via UDP
6. Max for Live device executes actions in Ableton
7. Max for Live device sends feedback to Python backend
8. Python backend forwards feedback to Electron app
9. Electron app displays feedback to user

## Development Plan

1. Create Max for Live bridge device
2. Set up Python backend with UDP communication
3. Create basic Electron app
4. Connect all components
5. Add advanced features and polish UI 