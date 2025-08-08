class SimpleNLPModule:
    def __init__(self):
        # Define command patterns without spaCy
        self.command_patterns = {
            "create": ["create", "make", "add"],
            "set": ["set", "change", "adjust"],
            "add_effect": ["add"]
        }
        
        # Define synonyms for normalization
        self.synonyms = {
            "bpm": "tempo",
            "audio": "audio",
            "midi": "midi",
            "echo": "delay",
            "reverb": "reverb",
            "compressor": "compressor",
            "piano": "piano",
            "synth": "synth",
            "drums": "drums",
            "wet": "wet",
            "dry": "dry",
            "dry/wet": "dry/wet",
            "mix": "dry/wet",
            "amount": "amount",
            "level": "level",
            "intensity": "intensity"
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
        
        # Normalize synonyms
        normalized_words = []
        for word in words:
            normalized_word = self.synonyms.get(word, word)
            normalized_words.append(normalized_word)
        
        # Extract verb (command type) - first word is usually the verb
        verb = normalized_words[0] if normalized_words else None
        
        # Determine intent - handle "add" specially
        if verb == "add":
            # Check what we're adding to determine intent
            has_effect = any(word in ["reverb", "delay", "compressor"] for word in normalized_words)
            has_instrument = any(word in ["piano", "synth", "drums"] for word in normalized_words)
            has_track_type = any(word in ["audio", "midi"] for word in normalized_words)
            
            if has_effect:
                result["intent"] = "add_effect"
            elif has_instrument:
                result["intent"] = "create"  # Adding instrument to current track
            elif has_track_type:
                result["intent"] = "create"  # Adding track
            else:
                result["intent"] = "add_effect"  # Default to effect if unclear
        elif verb == "set":
            # Check if this is setting effect parameters
            has_effect = any(word in ["reverb", "delay", "compressor"] for word in normalized_words)
            has_parameter = any(word in ["wet", "dry", "dry/wet", "mix", "amount", "level", "intensity"] for word in normalized_words)
            
            if has_effect and has_parameter:
                result["intent"] = "set_effect_param"
            else:
                result["intent"] = "set"  # Default to regular set commands
        elif verb:
            for intent, patterns in self.command_patterns.items():
                if verb in patterns:
                    result["intent"] = intent
                    break
        
        # Extract parameters based on intent
        if result["intent"] == "create":
            # Look for track type and instrument
            for i, word in enumerate(normalized_words):
                if word in ["midi", "audio"]:
                    result["parameters"]["track_type"] = word
                if word in ["piano", "synth", "drums"]:
                    result["parameters"]["instrument"] = word
                    
        elif result["intent"] == "set":
            # Look for setting type and value
            for i, word in enumerate(normalized_words):
                if word in ["tempo", "bpm"]:
                    # Look ahead for the tempo value
                    for j in range(i+1, len(normalized_words)):
                        try:
                            tempo_value = int(normalized_words[j])
                            result["parameters"]["tempo"] = tempo_value
                            break
                        except ValueError:
                            continue
                        
        elif result["intent"] == "add_effect":
            # Look for effect type and track number
            for i, word in enumerate(normalized_words):
                if word in ["reverb", "delay", "compressor"]:
                    result["parameters"]["effect"] = word
                if word == "track" and i + 1 < len(normalized_words):
                    try:
                        result["parameters"]["track_number"] = int(normalized_words[i + 1])
                    except ValueError:
                        pass
                        
        elif result["intent"] == "set_effect_param":
            # Look for effect, parameter, and value
            for i, word in enumerate(normalized_words):
                if word in ["reverb", "delay", "compressor"]:
                    result["parameters"]["effect"] = word
                if word in ["wet", "dry", "dry/wet", "mix", "amount", "level", "intensity"]:
                    result["parameters"]["parameter"] = word
                if word == "to" and i + 1 < len(normalized_words):
                    # Look for numeric value (with optional %)
                    try:
                        value_str = normalized_words[i + 1].replace('%', '')
                        value = float(value_str)
                        result["parameters"]["value"] = value
                        break
                    except ValueError:
                        continue
                        

        
        return result
