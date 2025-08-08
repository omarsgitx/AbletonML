class ActionMapper:
    def __init__(self):
        self.valid_actions = {
            "create": self._map_create_action,
            "set": self._map_set_action,
            "add_effect": self._map_add_effect_action,
            "set_effect_param": self._map_set_effect_param_action
        }
    
    def map_to_actions(self, parsed_command):
        """
        Convert parsed NLP command into a sequence of API actions
        """
        intent = parsed_command["intent"]
        parameters = parsed_command["parameters"]
        
        if intent not in self.valid_actions:
            return None
            
        return self.valid_actions[intent](parameters)
    
    def _map_create_action(self, parameters):
        """Map track creation commands to API actions"""
        actions = []
        
        track_type = parameters.get("track_type", "midi")
        instrument = parameters.get("instrument")
        
        actions.append({
            "action": "create_track",
            "params": {
                "type": track_type
            }
        })
        
        if instrument:
            actions.append({
                "action": "add_instrument",
                "params": {
                    "instrument": instrument
                }
            })
            
        return actions
    
    def _map_set_action(self, parameters):
        """Map setting commands to API actions"""
        actions = []
        
        if "tempo" in parameters:
            # Validate tempo range (20-999 BPM)
            tempo_value = parameters["tempo"]
            if 20 <= tempo_value <= 999:
                actions.append({
                    "action": "set_tempo",
                    "params": {
                        "value": tempo_value
                    }
                })
            
        return actions
    
    def _map_add_effect_action(self, parameters):
        """Map effect addition commands to API actions"""
        actions = []
        
        if "effect" in parameters and "track_number" in parameters:
            actions.append({
                "action": "add_effect",
                "params": {
                    "effect_type": parameters["effect"],
                    "track": parameters["track_number"]
                }
            })
            
        return actions
    
    def _map_set_effect_param_action(self, parameters):
        """Map effect parameter setting commands to API actions"""
        actions = []
        
        if "effect" in parameters and "parameter" in parameters and "value" in parameters:
            # Validate value range (0-100 for percentages)
            value = parameters["value"]
            if 0 <= value <= 100:
                actions.append({
                    "action": "set_effect_param",
                    "params": {
                        "effect": parameters["effect"],
                        "parameter": parameters["parameter"],
                        "value": value
                    }
                })
            
        return actions 