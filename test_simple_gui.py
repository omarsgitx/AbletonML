#!/usr/bin/env python3
import sys
import os
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.simple_nlp import SimpleNLPModule
from core.action_mapper import ActionMapper
from core.max_controller import MaxController

class SimpleAbletonMLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AbletonML - Simple Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#2D2D2D")
        
        # Set dark theme colors
        self.bg_color = "#2D2D2D"
        self.text_color = "#FFFFFF"
        self.input_bg = "#3D3D3D"
        self.highlight_color = "#5D5D5D"
        self.accent_color = "#007BFF"
        
        # Initialize our modules
        logger.debug("Initializing Simple NLP module")
        self.nlp = SimpleNLPModule()
        logger.debug("Initializing Action Mapper")
        self.mapper = ActionMapper()
        logger.debug("Initializing Max Controller")
        self.controller = MaxController()
        
        # Create the UI
        logger.debug("Creating UI widgets")
        self.create_widgets()
        
        # Update project state
        logger.debug("Scheduling initial project state update")
        self.root.after(1000, self.update_project_state)
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="AbletonML - Simple Test Interface",
            bg=self.bg_color,
            fg=self.accent_color,
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Output text area
        output_frame = tk.Frame(main_frame, bg=self.highlight_color, bd=1)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            bg=self.input_bg, 
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("Courier", 10),
            height=15,
            padx=5,
            pady=5
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.output_text.config(state=tk.DISABLED)
        
        # Input area
        input_frame = tk.Frame(main_frame, bg=self.highlight_color, bd=1)
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
        
        # Button
        execute_button = tk.Button(
            main_frame, 
            text="Execute", 
            command=lambda: self.process_command(None),
            bg=self.accent_color,
            fg=self.text_color,
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2"
        )
        execute_button.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_label = tk.Label(
            main_frame,
            text="Ready - Type a command like 'set tempo to 120' or 'create midi track'",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9)
        )
        self.status_label.pack(side=tk.LEFT, pady=10)
        
        # Add initial welcome message
        self.add_to_output("Welcome to AbletonML Simple Test Interface\n")
        self.add_to_output("This version uses a simplified NLP parser (no spaCy required)\n")
        self.add_to_output("Try commands like:\n")
        self.add_to_output("  - set tempo to 120\n")
        self.add_to_output("  - create midi track\n")
        self.add_to_output("  - add piano\n")
        self.add_to_output("  - add reverb to track 2\n\n")
        
        # Focus on input field
        self.input_field.focus_set()
        
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
        
        # Process in a separate thread
        threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()
        
    def execute_command(self, command_text):
        try:
            # Parse the command
            parsed_command = self.nlp.parse_command(command_text)
            self.add_to_output(f"Parsed: {parsed_command}\n")
            
            if not parsed_command["intent"]:
                self.add_to_output("Could not understand command\n")
                return
                
            # Map to actions
            actions = self.mapper.map_to_actions(parsed_command)
            self.add_to_output(f"Actions: {actions}\n")
            
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
            state = self.controller.get_project_state()
            
            if state:
                self.add_to_output(f"Project State: Tempo={state['tempo']} BPM, Tracks={len(state['tracks'])}\n")
                self.status_label.config(text=f"Tempo: {state['tempo']} BPM | Tracks: {len(state['tracks'])}")
            else:
                self.add_to_output("Could not get project state\n")
                
        except Exception as e:
            self.add_to_output(f"Error updating project state: {str(e)}\n")

if __name__ == "__main__":
    logger.debug("Starting Simple AbletonML application")
    root = tk.Tk()
    app = SimpleAbletonMLApp(root)
    logger.debug("Entering Tkinter main loop")
    root.mainloop()
    logger.debug("Application closed")
