class SimpleNLPModule:
    def __init__(self):
        # Define command patterns without spaCy
        self.command_patterns = {
            "create": ["create", "make"],
            "set": ["set", "change", "adjust"],
            "add_effect": ["add"]
        }
        
    def parse_command(self, command_text):
        """
        Parse a natural language command into structured intent and parameters
        Simple version without spaCy
        """
        words = command_text.lower().split()
        
        # Initialize result structure
        result = {
            "intent": None,
            "parameters": {}
        }
        
        # Extract verb (command type) - first word is usually the verb
        verb = words[0] if words else None
        
        # Determine intent - handle "add" specially
        if verb == "add":
            # Check what we're adding to determine intent
            has_effect = any(word in ["reverb", "delay", "compressor"] for word in words)
            has_instrument = any(word in ["piano", "synth", "drums"] for word in words)
            
            if has_effect:
                result["intent"] = "add_effect"
            elif has_instrument:
                result["intent"] = "create"  # Adding instrument to current track
            else:
                result["intent"] = "add_effect"  # Default to effect if unclear
        elif verb:
            for intent, patterns in self.command_patterns.items():
                if verb in patterns:
                    result["intent"] = intent
                    break
        
        # Extract parameters based on intent
        if result["intent"] == "create":
            # Look for track type and instrument
            for i, word in enumerate(words):
                if word in ["midi", "audio"]:
                    result["parameters"]["track_type"] = word
                if word in ["piano", "synth", "drums"]:
                    result["parameters"]["instrument"] = word
                    
        elif result["intent"] == "set":
            # Look for setting type and value
            for i, word in enumerate(words):
                if word == "tempo":
                    # Look ahead for the tempo value
                    for j in range(i+1, len(words)):
                        try:
                            tempo_value = int(words[j])
                            result["parameters"]["tempo"] = tempo_value
                            break
                        except ValueError:
                            continue
                        
        elif result["intent"] == "add_effect":
            # Look for effect type and track number
            for i, word in enumerate(words):
                if word in ["reverb", "delay", "compressor"]:
                    result["parameters"]["effect"] = word
                if word == "track" and i + 1 < len(words):
                    try:
                        result["parameters"]["track_number"] = int(words[i + 1])
                    except ValueError:
                        pass
                        

        
        return result
