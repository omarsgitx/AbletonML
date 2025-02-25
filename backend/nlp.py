import spacy

class NLPModule:
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Define command patterns
        self.command_patterns = {
            "create": ["create", "make", "add"],
            "set": ["set", "change", "adjust"],
            "add_effect": ["add"]
        }
        
    def parse_command(self, command_text):
        """
        Parse a natural language command into structured intent and parameters
        """
        doc = self.nlp(command_text.lower())
        
        # Initialize result structure
        result = {
            "intent": None,
            "parameters": {}
        }
        
        # Extract verb (command type)
        verb = None
        for token in doc:
            if token.pos_ == "VERB":
                verb = token.text
                break
        
        # Determine intent
        if verb:
            for intent, patterns in self.command_patterns.items():
                if verb in patterns:
                    result["intent"] = intent
                    break
        
        # Extract parameters based on intent
        if result["intent"] == "create":
            # Look for track type and instrument
            for token in doc:
                if token.text in ["midi", "audio"]:
                    result["parameters"]["track_type"] = token.text
                if token.text in ["piano", "synth", "drums"]:
                    result["parameters"]["instrument"] = token.text
                    
        elif result["intent"] == "set":
            # Look for setting type and value
            for i, token in enumerate(doc):
                if token.text == "tempo":
                    # Look ahead for the tempo value
                    for j in range(i+1, len(doc)):
                        try:
                            tempo_value = int(doc[j].text)
                            result["parameters"]["tempo"] = tempo_value
                            break
                        except ValueError:
                            continue
                        
        elif result["intent"] == "add_effect":
            # Look for effect type and track number
            for i, token in enumerate(doc):
                if token.text in ["reverb", "delay", "compressor"]:
                    result["parameters"]["effect"] = token.text
                if token.text == "track" and i + 1 < len(doc):
                    try:
                        result["parameters"]["track_number"] = int(doc[i + 1].text)
                    except ValueError:
                        pass
        
        return result 