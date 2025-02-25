#!/usr/bin/env python3
import sys
import os
import json
import logging
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.nlp import NLPModule
from core.action_mapper import ActionMapper
from core.max_controller import MaxController

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize our modules
logger.debug("Initializing NLP module")
nlp = NLPModule()
logger.debug("Initializing Action Mapper")
mapper = ActionMapper()
logger.debug("Initializing Max Controller")
controller = MaxController()

@app.route('/api/status', methods=['GET'])
def get_status():
    """API endpoint to check server status"""
    return jsonify({"status": "running"})

@app.route('/api/project_state', methods=['GET'])
def get_project_state():
    """API endpoint to get current project state"""
    state = controller.get_project_state()
    return jsonify(state)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.debug("Client connected")
    emit('response', {'success': True, 'message': 'Connected to AbletonML server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.debug("Client disconnected")

@socketio.on('command')
def handle_command(data):
    """Handle command from client"""
    command = data.get('command', '')
    logger.debug(f"Received command: {command}")
    
    try:
        # Process the command with NLP
        parsed_command = nlp.parse_command(command)
        logger.debug(f"Parsed command: {parsed_command}")
        
        # Map to actions
        actions = mapper.map_to_actions(parsed_command)
        logger.debug(f"Actions: {actions}")
        
        if not actions:
            emit('response', {'success': False, 'message': f"Could not understand command: {command}"})
            return
        
        # Execute actions
        results = []
        for action in actions:
            result = controller.execute_action(action)
            results.append(result)
        
        # Get updated project state
        state = controller.get_project_state()
        
        # Send response and updated state
        emit('response', {'success': True, 'message': f"Executed command: {command}"})
        emit('project_state', state)
        
    except Exception as e:
        logger.exception(f"Error processing command: {e}")
        emit('response', {'success': False, 'message': f"Error: {str(e)}"})

@socketio.on('get_project_state')
def handle_get_project_state():
    """Handle request for project state"""
    logger.debug("Client requested project state")
    state = controller.get_project_state()
    emit('project_state', state)

@socketio.on('get_max_status')
def handle_get_max_status():
    """Handle request for Max for Live connection status"""
    logger.debug("Client requested Max for Live status")
    try:
        # Check if Max for Live is connected
        # For now, we'll just return the controller's connected status
        emit('max_status', {
            "connected": controller.connected,
            "host": controller.host,
            "port": controller.port
        })
    except Exception as e:
        logger.exception(f"Error getting Max for Live status: {e}")
        emit('max_status', {
            "connected": False,
            "error": str(e)
        })

if __name__ == '__main__':
    logger.debug("Starting AbletonML API server")
    # Run the Socket.IO server
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)
    
    # Clean up when the server is stopped
    if hasattr(controller, 'close'):
        controller.close() 