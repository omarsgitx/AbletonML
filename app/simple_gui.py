import sys
import os
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import json
import logging  # Add logging module

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.nlp import NLPModule
from core.action_mapper import ActionMapper
from core.max_controller import MaxController

class AbletonMLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AbletonML")
        self.root.geometry("1000x700")  # Increased window size for better visibility
        self.root.configure(bg="#2D2D2D")
        
        # Set dark theme colors
        self.bg_color = "#2D2D2D"
        self.text_color = "#FFFFFF"
        self.input_bg = "#3D3D3D"
        self.highlight_color = "#5D5D5D"
        self.accent_color = "#007BFF"  # Added accent color for better visual hierarchy
        
        # Initialize our modules
        logger.debug("Initializing NLP module")
        self.nlp = NLPModule()
        logger.debug("Initializing Action Mapper")
        self.mapper = ActionMapper()
        logger.debug("Initializing Ableton Controller")
        self.controller = MaxController()
        
        # Create the UI
        logger.debug("Creating UI widgets")
        self.create_widgets()
        
        # Update project state with a longer delay to ensure controller is ready
        logger.debug("Scheduling initial project state update")
        self.root.after(1000, self.update_project_state)
        
    def create_widgets(self):
        # Create main frame to hold everything
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create main horizontal paned window with fixed sash width
        self.paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, 
                                          bg=self.bg_color, 
                                          sashwidth=6, 
                                          sashrelief=tk.RAISED,
                                          sashpad=2)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Command area
        left_frame = tk.Frame(self.paned_window, bg=self.bg_color, width=600)
        left_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Output text area with border and padding
        output_frame = tk.Frame(left_frame, bg=self.highlight_color, bd=1)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            bg=self.input_bg, 
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("Courier", 12),
            height=20,
            padx=5,
            pady=5
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.output_text.config(state=tk.DISABLED)
        
        # Input area with border
        input_frame = tk.Frame(left_frame, bg=self.highlight_color, bd=1)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_inner_frame = tk.Frame(input_frame, bg=self.input_bg, padx=5, pady=5)
        input_inner_frame.pack(fill=tk.X, padx=2, pady=2)
        
        prompt_label = tk.Label(
            input_inner_frame, 
            text="> ", 
            bg=self.input_bg, 
            fg=self.accent_color,
            font=("Courier", 12, "bold")
        )
        prompt_label.pack(side=tk.LEFT)
        
        self.input_field = tk.Entry(
            input_inner_frame, 
            bg=self.input_bg, 
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("Courier", 12),
            bd=0,
            highlightthickness=0
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_field.bind("<Return>", self.process_command)
        
        # Button area
        button_frame = tk.Frame(left_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X)
        
        execute_button = tk.Button(
            button_frame, 
            text="Execute", 
            command=lambda: self.process_command(None),
            bg=self.accent_color,
            fg=self.text_color,
            font=("Courier", 10, "bold"),
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2"  # Change cursor on hover
        )
        execute_button.pack(side=tk.RIGHT)
        
        # Add left frame to paned window
        self.paned_window.add(left_frame, stretch="always", minsize=400)
        
        # Right side - Project state
        right_frame = tk.Frame(self.paned_window, bg=self.input_bg, width=300)
        right_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Project state header
        state_header = tk.Label(
            right_frame,
            text="Project State",
            bg=self.highlight_color,
            fg=self.text_color,
            font=("Courier", 14, "bold"),
            pady=10,
            width=100  # Make header full width
        )
        state_header.pack(fill=tk.X)
        
        # Tempo display with better visual separation
        tempo_frame = tk.Frame(right_frame, bg=self.input_bg, pady=10)
        tempo_frame.pack(fill=tk.X, padx=10)
        
        tempo_label = tk.Label(
            tempo_frame,
            text="Tempo:",
            bg=self.input_bg,
            fg=self.accent_color,
            font=("Courier", 12, "bold"),
            width=10,
            anchor="w"
        )
        tempo_label.pack(side=tk.LEFT)
        
        self.tempo_value = tk.Label(
            tempo_frame,
            text="120 BPM",
            bg=self.input_bg,
            fg=self.text_color,
            font=("Courier", 12),
            anchor="w"
        )
        self.tempo_value.pack(side=tk.LEFT)
        
        # Separator
        separator = ttk.Separator(right_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=5)
        
        # Tracks header
        tracks_header = tk.Label(
            right_frame,
            text="Tracks:",
            bg=self.input_bg,
            fg=self.accent_color,
            font=("Courier", 12, "bold"),
            anchor="w",
            pady=5,
            padx=10
        )
        tracks_header.pack(fill=tk.X)
        
        # Tracks display area with scrollbar and border
        tracks_frame = tk.Frame(right_frame, bg=self.highlight_color, bd=1)
        tracks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tracks_display = scrolledtext.ScrolledText(
            tracks_frame,
            bg=self.input_bg,
            fg=self.text_color,
            font=("Courier", 10),
            padx=10,
            pady=5,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.tracks_display.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add right frame to paned window
        self.paned_window.add(right_frame, minsize=300)
        
        # Set initial position of sash
        self.paned_window.sash_place(0, 650, 0)
        
        # Add initial welcome message
        self.add_to_output("Welcome to AbletonML\n")
        self.add_to_output("Type commands like 'create midi track with piano' or 'set tempo to 120'\n")
        
        # Focus on input field
        self.input_field.focus_set()
        
        logger.debug("All widgets created")
        
    def add_to_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def process_command(self, event):
        command = self.input_field.get()
        if not command:
            return
            
        # Add command to output
        self.add_to_output(f"> {command}\n")
        
        # Clear input field
        self.input_field.delete(0, tk.END)
        
        # Process in a separate thread to keep UI responsive
        threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()
        
    def execute_command(self, command_text):
        try:
            # Parse the command
            parsed_command = self.nlp.parse_command(command_text)
            
            if not parsed_command["intent"]:
                self.add_to_output("Could not understand command\n")
                return
                
            # Map to actions
            actions = self.mapper.map_to_actions(parsed_command)
            
            if not actions:
                self.add_to_output("Could not map command to actions\n")
                return
                
            # Execute actions
            success = True
            for action in actions:
                if not self.controller.execute_action(action):
                    success = False
                    break
                    
            if success:
                self.add_to_output("Command executed successfully\n")
                # Update project state
                self.root.after(100, self.update_project_state)
            else:
                self.add_to_output("Command failed\n")
                
        except Exception as e:
            self.add_to_output(f"Error: {str(e)}\n")
    
    def update_project_state(self):
        """Update the project state display"""
        try:
            # Get current project state
            logger.debug("Fetching project state from controller")
            state = self.controller.get_project_state()
            
            if state:
                logger.debug(f"Received project state: {json.dumps(state, indent=2)}")
                
                # Update tempo
                self.tempo_value.config(text=f"{state['tempo']} BPM")
                logger.debug(f"Updated tempo display to {state['tempo']} BPM")
                
                # Update tracks display
                self.tracks_display.config(state=tk.NORMAL)
                self.tracks_display.delete(1.0, tk.END)
                
                # Add tracks
                logger.debug(f"Adding {len(state['tracks'])} tracks to display")
                for i, track in enumerate(state['tracks']):
                    logger.debug(f"Creating display for track {i}: {track['name']}")
                    
                    # Highlight selected track
                    if i == state.get('selected_track', -1):
                        self.tracks_display.insert(tk.END, f"→ {track['name']}\n", "selected")
                    else:
                        self.tracks_display.insert(tk.END, f"  {track['name']}\n")
                    
                    # Add devices if any
                    if 'devices' in track and track['devices']:
                        logger.debug(f"Adding {len(track['devices'])} devices for track {track['name']}")
                        for device in track['devices']:
                            self.tracks_display.insert(tk.END, f"    - {device['name']}\n", "device")
                
                # Configure tags
                self.tracks_display.tag_configure("selected", background="#4D4D4D")
                self.tracks_display.tag_configure("device", foreground="#AAAAAA")
                
                self.tracks_display.config(state=tk.DISABLED)
                logger.debug("Updated tracks display")
                
            else:
                logger.error("Received None or empty project state")
                
        except Exception as e:
            logger.exception(f"Error updating project state: {e}")

if __name__ == "__main__":
    logger.debug("Starting AbletonML application")
    root = tk.Tk()
    app = AbletonMLApp(root)
    logger.debug("Entering Tkinter main loop")
    root.mainloop()
    logger.debug("Application closed") 