import time
import random
from pythonosc import udp_client

# --- CONFIGURATION ---
IP = "127.0.0.1"
PORT = 11000  # Default port for AbletonOSC

def main():
    print(f"Attempting to connect to AbletonOSC at {IP}:{PORT}...")
    
    try:
        # Create the client
        client = udp_client.SimpleUDPClient(IP, PORT)

        # TEST 1: Transport Control
        # This checks if we can control global playback
        print("Test 1: Starting Playback...")
        client.send_message("/live/song/start_playing", [])
        time.sleep(2)
        
        print("Test 1: Stopping Playback...")
        client.send_message("/live/song/stop_playing", [])
        time.sleep(1)

        # TEST 2: Tempo
        # This checks if we can set properties
        new_tempo = random.randint(80, 140)
        print(f"Test 2: Setting Tempo to {new_tempo} BPM...")
        client.send_message("/live/song/set/tempo", [new_tempo])
        time.sleep(1)

        # TEST 3: Create Track
        # This checks if we can modify the project structure (impossible in standard M4L)
        print("Test 3: Creating a new MIDI track...")
        client.send_message("/live/song/create_midi_track", [-1]) # -1 creates it at the end
        
        print("\n✅ Tests sent! Check Ableton Live to see if the playback started/stopped and a track appeared.")
        print("If nothing happened, ensure 'AbletonOSC' is selected in Live > Preferences > Link/Tempo/MIDI.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()