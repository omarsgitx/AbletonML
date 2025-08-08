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
        "set tempo to 120",
        "create midi track",
        "add piano",
        "add reverb to track 2",
        "add delay to track 1",
        "create audio track",
        "add synth"
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
        if "reverb" in command or "delay" in command:
            if parsed["intent"] == "add_effect":
                print("  ✅ Correctly identified as add_effect")
            else:
                print("  ❌ Should be add_effect but got:", parsed["intent"])
        elif "piano" in command or "synth" in command:
            if parsed["intent"] == "create":
                print("  ✅ Correctly identified as create (instrument)")
            else:
                print("  ❌ Should be create but got:", parsed["intent"])
        elif "track" in command and ("midi" in command or "audio" in command):
            if parsed["intent"] == "create":
                print("  ✅ Correctly identified as create (track)")
            else:
                print("  ❌ Should be create but got:", parsed["intent"])
        elif "tempo" in command:
            if parsed["intent"] == "set":
                print("  ✅ Correctly identified as set")
            else:
                print("  ❌ Should be set but got:", parsed["intent"])

if __name__ == "__main__":
    test_nlp_parsing()
