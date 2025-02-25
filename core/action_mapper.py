class ActionMapper:
    def __init__(self):
        self.valid_actions = {
            "create": self._map_create_action,
            "set": self._map_set_action,
            "add_effect": self._map_add_effect_action
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
            actions.append({
                "action": "set_tempo",
                "params": {
                    "value": parameters["tempo"]
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