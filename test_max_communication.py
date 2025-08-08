#!/usr/bin/env python3
import socket
import json
import time
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_max_communication():
    """Test UDP communication with the Max for Live device"""
    
    # Max for Live device settings
    host = '127.0.0.1'
    port = 7400
    
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("Testing Max for Live Device Communication")
    print("=" * 50)
    print(f"Target: {host}:{port}")
    print()
    
    # Test commands
    test_commands = [
        {
            "type": "set_tempo",
            "params": {"value": 120}
        },
        {
            "type": "set_tempo", 
            "params": {"value": 140}
        },
        {
            "type": "create_track",
            "params": {"type": "midi"}
        },
        {
            "type": "add_instrument",
            "params": {"instrument": "piano"}
        }
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"Test {i}: Sending command: {command['type']}")
        
        try:
            # Send command
            message = json.dumps(command).encode()
            sock.sendto(message, (host, port))
            print(f"  ✓ Sent: {message.decode()}")
            
            # Wait a bit for processing
            time.sleep(1)
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()
    
    sock.close()
    print("Test completed!")
    print()
    print("If the Max for Live device is running, you should see:")
    print("- Tempo changes in Ableton Live")
    print("- New tracks being created")
    print("- Instruments being added")
    print()
    print("Check the Max console for any error messages.")

if __name__ == "__main__":
    test_max_communication()
