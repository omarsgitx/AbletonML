import socket
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MaxController:
    def __init__(self, host='127.0.0.1', port=7400):
        """Initialize UDP connection to Max for Live"""
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connected = True  # Assume connection is successful
        
        # Simulation state (used when Max connection fails)
        self.sim_tempo = 120
        self.sim_tracks = []
        self.sim_selected_track = 0
        
        logger.info(f"Initialized Max controller with host={host}, port={port}")
        self._sim_create_default_project()
        
    def _sim_create_default_project(self):
        """Create a default project structure for simulation mode"""
        logger.debug("Creating default project structure for simulation mode")
        
        # Add a master track
        self.sim_tracks.append({
            "name": "Master",
            "type": "audio",
            "devices": []
        })
        logger.debug("Added Master track")
        
        # Add a default audio track
        self.sim_tracks.append({
            "name": "Audio Track 1",
            "type": "audio",
            "devices": []
        })
        logger.debug("Added Audio Track 1")
        
        # Add a default MIDI track
        self.sim_tracks.append({
            "name": "MIDI Track 1",
            "type": "midi",
            "devices": []
        })
        logger.debug("Added MIDI Track 1")
        
        # Set the selected track to the MIDI track
        self.sim_selected_track = 2
        logger.debug(f"Set selected track to index {self.sim_selected_track}")
        
        # Log the complete default project
        logger.debug(f"Default project created with {len(self.sim_tracks)} tracks")
    
    def _sim_get_project_state(self):
        """Get the current project state in simulation mode"""
        logger.debug("Getting project state in simulation mode")
        state = {
            "tempo": self.sim_tempo,
            "tracks": self.sim_tracks,
            "selected_track": self.sim_selected_track
        }
        logger.debug(f"Project state: {json.dumps(state, indent=2)}")
        return state
        
    def _send_command(self, command_type, params):
        """Send a command to Max for Live"""
        message = {
            'type': command_type,
            'params': params
        }
        try:
            logger.debug(f"Sending command to Max: {message}")
            self.socket.sendto(json.dumps(message).encode(), (self.host, self.port))
            return True
        except Exception as e:
            logger.error(f"Error sending command: {e}")
            return False
    
    def set_tempo(self, tempo):
        """Set the project tempo"""
        if not self.connected:
            logger.debug(f"Simulation: Setting tempo to {tempo} BPM")
            self.sim_tempo = tempo
            return True
            
        if 20 <= tempo <= 999:
            result = self._send_command('set_tempo', {'value': tempo})
            if result:
                logger.info(f"Set tempo to {tempo} BPM")
                # Update simulation state as well
                self.sim_tempo = tempo
            return result
        return False
    
    def create_track(self, track_type):
        """Create a new track"""
        if not self.connected:
            track_number = len(self.sim_tracks)
            track_name = f"{track_type.capitalize()} Track {track_number}"
            
            new_track = {
                "name": track_name,
                "type": track_type,
                "devices": []
            }
            
            self.sim_tracks.append(new_track)
            self.sim_selected_track = len(self.sim_tracks) - 1
            
            logger.debug(f"Simulation: Created {track_type} track '{track_name}'")
            return True
            
        result = self._send_command('create_track', {'type': track_type})
        if result:
            logger.info(f"Created {track_type} track")
            
            # Update simulation state as well
            track_number = len(self.sim_tracks)
            track_name = f"{track_type.capitalize()} Track {track_number}"
            
            new_track = {
                "name": track_name,
                "type": track_type,
                "devices": []
            }
            
            self.sim_tracks.append(new_track)
            self.sim_selected_track = len(self.sim_tracks) - 1
        return result
    
    def add_instrument(self, instrument):
        """Add an instrument to the current track"""
        if not self.connected:
            if self.sim_selected_track < 1:
                logger.warning("Simulation: Cannot add instrument to master track")
                return False
                
            track = self.sim_tracks[self.sim_selected_track]
            
            if track["type"] != "midi":
                logger.warning("Simulation: Cannot add instrument to audio track")
                return False
                
            # Map instrument names to device names
            instrument_mapping = {
                "piano": "Grand Piano",
                "synth": "Analog",
                "drums": "Drum Rack"
            }
            
            device_name = instrument_mapping.get(instrument, instrument)
            track["devices"].append({
                "name": device_name,
                "type": "instrument"
            })
            
            logger.debug(f"Simulation: Added {device_name} to track '{track['name']}'")
            return True
            
        result = self._send_command('add_instrument', {'instrument': instrument})
        if result:
            logger.info(f"Added {instrument} to current track")
            
            # Update simulation state as well
            if self.sim_selected_track < 1:
                return True
                
            track = self.sim_tracks[self.sim_selected_track]
            
            if track["type"] != "midi":
                return True
                
            # Map instrument names to device names
            instrument_mapping = {
                "piano": "Grand Piano",
                "synth": "Analog",
                "drums": "Drum Rack"
            }
            
            device_name = instrument_mapping.get(instrument, instrument)
            track["devices"].append({
                "name": device_name,
                "type": "instrument"
            })
        return result
    
    def add_effect(self, effect_type, track_number):
        """Add an effect to a specific track"""
        if not self.connected:
            if track_number < 1 or track_number >= len(self.sim_tracks):
                logger.warning(f"Simulation: Track {track_number} does not exist")
                return False
                
            # Adjust track_number to be 0-indexed for internal use
            track_index = track_number - 1
            logger.debug(f"Adjusting track number {track_number} to index {track_index}")
            track = self.sim_tracks[track_index]
            
            # Map effect names to device names
            effect_mapping = {
                "reverb": "Reverb",
                "delay": "Delay",
                "compressor": "Compressor"
            }
            
            device_name = effect_mapping.get(effect_type, effect_type)
            track["devices"].append({
                "name": device_name,
                "type": "effect"
            })
            
            logger.debug(f"Simulation: Added {device_name} to track '{track['name']}'")
            return True
            
        result = self._send_command('add_effect', {
            'effect': effect_type,
            'track': track_number
        })
        
        if result:
            logger.info(f"Added {effect_type} to track {track_number}")
            
            # Update simulation state as well
            if track_number < 1 or track_number >= len(self.sim_tracks):
                return True
                
            track_index = track_number - 1
            track = self.sim_tracks[track_index]
            
            # Map effect names to device names
            effect_mapping = {
                "reverb": "Reverb",
                "delay": "Delay",
                "compressor": "Compressor"
            }
            
            device_name = effect_mapping.get(effect_type, effect_type)
            track["devices"].append({
                "name": device_name,
                "type": "effect"
            })
        return result
    
    def set_effect_param(self, effect, parameter, value):
        """Set an effect parameter value"""
        if not self.connected:
            logger.debug(f"Simulation: Setting {effect} {parameter} to {value}%")
            # In simulation mode, we could update the effect in the track
            # For now, just log the action
            return True
            
        result = self._send_command('set_effect_param', {
            'effect': effect,
            'parameter': parameter,
            'value': value
        })
        
        if result:
            logger.info(f"Set {effect} {parameter} to {value}%")
        return result
    
    def get_project_state(self):
        """Get the current project state"""
        logger.debug("get_project_state called")
        # For now, we'll use the simulation state
        # In a real implementation, we would query Max for Live for the current state
        return self._sim_get_project_state()
    
    def execute_action(self, action):
        """Execute a single action"""
        action_type = action["action"]
        params = action["params"]
        
        logger.debug(f"Executing action: {action_type} with params: {params}")
        
        if action_type == "create_track":
            return self.create_track(params["type"])
        elif action_type == "add_instrument":
            return self.add_instrument(params["instrument"])
        elif action_type == "set_tempo":
            return self.set_tempo(params["value"])
        elif action_type == "add_effect":
            return self.add_effect(params["effect_type"], params["track"])
        elif action_type == "set_effect_param":
            return self.set_effect_param(params["effect"], params["parameter"], params["value"])
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return False
    
    def close(self):
        """Close socket connection"""
        try:
            self.socket.close()
            logger.debug("Closed socket connection")
        except Exception as e:
            logger.error(f"Error closing socket: {e}") 