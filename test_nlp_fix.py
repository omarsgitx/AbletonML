#!/usr/bin/env python3
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.simple_nlp import SimpleNLPModule
from core.action_mapper import ActionMapper

def test_nlp_parsing():
    """Test the NLP parsing with various commands"""
    
    nlp = SimpleNLPModule()
    mapper = ActionMapper()
    
    test_commands = [
        # Phase 1: Enhanced tempo commands
        "set tempo to 120",
        "change bpm to 90",
        "set bpm to 140",
        "adjust tempo to 80",
        
        # Phase 1: Enhanced track creation
        "create midi track",
        "create audio track",
        "add audio track",
        "make midi track",
        
        # Phase 1: Enhanced effect commands
        "add reverb to track 2",
        "add delay to track 1",
        "add echo to track 3",
        "add compressor to track 4",
        
        # Phase 3: Effect parameter commands
        "set reverb dry/wet to 30%",
        "set delay mix to 50",
        "set compressor amount to 75%",
        "set reverb wet to 80",
        "set delay level to 25%",
        
        # Existing commands (should still work)
        "add piano",
        "add synth",
        "add drums"
    ]
    
    print("Testing NLP Parsing Fix")
    print("=" * 50)
    
    for command in test_commands:
        print(f"\nCommand: '{command}'")
        
        # Parse the command
        parsed = nlp.parse_command(command)
        print(f"  Parsed: {parsed}")
        
        # Map to actions
        actions = mapper.map_to_actions(parsed)
        print(f"  Actions: {actions}")
        
        # Check if it's correct
        if "reverb" in command or "delay" in command or "echo" in command or "compressor" in command:
            if "to" in command and ("wet" in command or "dry" in command or "mix" in command or "amount" in command or "level" in command):
                if parsed["intent"] == "set_effect_param":
                    print("  ✅ Correctly identified as set_effect_param")
                else:
                    print("  ❌ Should be set_effect_param but got:", parsed["intent"])
            elif parsed["intent"] == "add_effect":
                print("  ✅ Correctly identified as add_effect")
            else:
                print("  ❌ Should be add_effect but got:", parsed["intent"])
        elif "piano" in command or "synth" in command or "drums" in command:
            if parsed["intent"] == "create":
                print("  ✅ Correctly identified as create (instrument)")
            else:
                print("  ❌ Should be create but got:", parsed["intent"])
        elif "track" in command and ("midi" in command or "audio" in command):
            if parsed["intent"] == "create":
                print("  ✅ Correctly identified as create (track)")
            else:
                print("  ❌ Should be create but got:", parsed["intent"])
        elif "tempo" in command or "bpm" in command:
            if parsed["intent"] == "set":
                print("  ✅ Correctly identified as set")
            else:
                print("  ❌ Should be set but got:", parsed["intent"])

if __name__ == "__main__":
    test_nlp_parsing()
