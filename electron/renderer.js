// Renderer process

// DOM Elements
const outputElement = document.getElementById('output');
const commandInput = document.getElementById('command-input');
const executeBtn = document.getElementById('execute-btn');
const tempoValue = document.getElementById('tempo-value');
const tracksList = document.getElementById('tracks-list');
const connectionStatus = document.getElementById('connection-status');
const statusMessage = document.getElementById('status-message');
const statusDot = document.querySelector('.status-dot');
const historyList = document.getElementById('history-list');
const clearHistoryBtn = document.getElementById('clear-history-btn');

// Command history storage
let commandHistory = [];
const MAX_HISTORY = 10;

// Connect to Socket.io server
const socket = io('http://localhost:3000');

// Socket event handlers
socket.on('connect', () => {
  updateConnectionStatus(true);
  addToOutput('Connected to server', 'success');
  
  // Request Max for Live status
  socket.emit('get_max_status');
});

socket.on('disconnect', () => {
  updateConnectionStatus(false);
});



socket.on('project_state', (state) => {
  updateProjectState(state);
});

socket.on('max_status', (data) => {
  displayMaxStatus(data);
});

// Event listeners
executeBtn.addEventListener('click', sendCommand);
commandInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendCommand();
  }
});

clearHistoryBtn.addEventListener('click', clearHistory);

// Functions
function sendCommand() {
  const command = commandInput.value.trim();
  if (!command) return;
  
  // Add command to output
  addToOutput(`> ${command}`, 'command');
  
  // Add to command history
  addToHistory(command, 'pending');
  
  // Send command to server
  socket.emit('command', { command });
  
  // Clear input
  commandInput.value = '';
}

function addToOutput(message, type = '') {
  const messageElement = document.createElement('div');
  messageElement.textContent = message;
  if (type) {
    messageElement.classList.add(type);
  }
  
  outputElement.appendChild(messageElement);
  
  // Scroll to bottom
  outputElement.scrollTop = outputElement.scrollHeight;
}

function updateConnectionStatus(connected) {
  if (connected) {
    connectionStatus.textContent = 'Connected';
    statusDot.classList.remove('disconnected');
    statusDot.classList.add('connected');
    statusMessage.textContent = 'Ready';
  } else {
    connectionStatus.textContent = 'Disconnected';
    statusDot.classList.remove('connected');
    statusDot.classList.add('disconnected');
    statusMessage.textContent = 'Connection lost';
  }
}

function updateProjectState(state) {
  // Update tempo
  tempoValue.textContent = state.tempo;
  
  // Update tracks
  tracksList.innerHTML = '';
  
  state.tracks.forEach((track, index) => {
    const trackElement = document.createElement('div');
    trackElement.classList.add('track-item');
    
    if (index === state.selected_track) {
      trackElement.classList.add('selected');
    }
    
    const trackName = document.createElement('div');
    trackName.classList.add('track-name');
    trackName.textContent = track.name;
    trackElement.appendChild(trackName);
    
    // Add devices if any
    if (track.devices && track.devices.length > 0) {
      const devicesElement = document.createElement('div');
      devicesElement.classList.add('track-devices');
      
      track.devices.forEach(device => {
        const deviceElement = document.createElement('div');
        deviceElement.textContent = `- ${device.name}`;
        devicesElement.appendChild(deviceElement);
      });
      
      trackElement.appendChild(devicesElement);
    }
    
    tracksList.appendChild(trackElement);
  });
}

function displayMaxStatus(data) {
  // Add Max for Live status information to output
  addToOutput('Max for Live Connection:', 'info');
  
  if (data.connected) {
    addToOutput(`Connected to Max for Live at ${data.host}:${data.port}`, 'success');
    statusMessage.textContent = 'Connected to Max for Live';
  } else {
    if (data.error) {
      addToOutput(`Not connected to Max for Live: ${data.error}`, 'warning');
    } else {
      addToOutput('Not connected to Max for Live. Running in simulation mode.', 'warning');
    }
    statusMessage.textContent = 'Simulation Mode';
  }
  
  // Add instructions for Max for Live setup
  addToOutput('', 'info');
  addToOutput('To use Max for Live:', 'info');
  addToOutput('1. Open Ableton Live', 'info');
  addToOutput('2. Create a MIDI track', 'info');
  addToOutput('3. Drag the AbletonML_Bridge.amxd device from the max folder to the track', 'info');
  addToOutput('4. Make sure the device is enabled', 'info');
}

// Command History Functions
function addToHistory(command, status, details = '') {
  const timestamp = new Date().toLocaleTimeString();
  const historyItem = {
    command,
    status,
    timestamp,
    details
  };
  
  // Add to beginning of array
  commandHistory.unshift(historyItem);
  
  // Keep only last MAX_HISTORY items
  if (commandHistory.length > MAX_HISTORY) {
    commandHistory = commandHistory.slice(0, MAX_HISTORY);
  }
  
  updateHistoryDisplay();
}

function updateHistoryDisplay() {
  historyList.innerHTML = '';
  
  commandHistory.forEach(item => {
    const historyElement = document.createElement('div');
    historyElement.classList.add('history-item');
    historyElement.classList.add(item.status);
    
    const statusIcon = document.createElement('span');
    statusIcon.classList.add('status-icon');
    
    if (item.status === 'success') {
      statusIcon.innerHTML = '✅';
      statusIcon.classList.add('success');
    } else if (item.status === 'error') {
      statusIcon.innerHTML = '❌';
      statusIcon.classList.add('error');
    } else if (item.status === 'pending') {
      statusIcon.innerHTML = '⏳';
    }
    
    const commandText = document.createElement('span');
    commandText.classList.add('command-text');
    commandText.textContent = item.command;
    
    const timestamp = document.createElement('span');
    timestamp.classList.add('timestamp');
    timestamp.textContent = item.timestamp;
    
    historyElement.appendChild(statusIcon);
    historyElement.appendChild(commandText);
    historyElement.appendChild(timestamp);
    
    historyList.appendChild(historyElement);
  });
}

function clearHistory() {
  commandHistory = [];
  updateHistoryDisplay();
}

// Update socket response handler to update history
socket.on('response', (data) => {
  if (data.success) {
    addToOutput(data.message, 'success');
    // Update the most recent pending command to success
    if (commandHistory.length > 0 && commandHistory[0].status === 'pending') {
      commandHistory[0].status = 'success';
      commandHistory[0].details = data.message;
      updateHistoryDisplay();
    }
    // Update status bar
    statusMessage.textContent = `Executed: ${data.message}`;
  } else {
    addToOutput(`Error: ${data.message}`, 'error');
    // Update the most recent pending command to error
    if (commandHistory.length > 0 && commandHistory[0].status === 'pending') {
      commandHistory[0].status = 'error';
      commandHistory[0].details = data.message;
      updateHistoryDisplay();
    }
    // Update status bar
    statusMessage.textContent = `Error: ${data.message}`;
  }
});

// Add welcome message
addToOutput('Welcome to AbletonML');
addToOutput('Type commands like "create midi track with piano" or "set tempo to 120"');

// Request initial project state
setTimeout(() => {
  socket.emit('get_project_state');
}, 1000); 