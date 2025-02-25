const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

// Express app for API communication
const expressApp = express();
const server = http.createServer(expressApp);
const io = new Server(server);

// Python backend process
let pythonProcess = null;

// Create the browser window
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#2D2D2D',
    show: false
  });

  // Load the index.html file
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
  
  // Show window when ready to avoid flickering
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Open DevTools in development
  // mainWindow.webContents.openDevTools();
  
  return mainWindow;
}

// Start the Python backend
function startPythonBackend() {
  // Determine the Python executable (python3 or python)
  const pythonExecutable = process.platform === 'win32' ? 'python' : 'python3';
  
  // Path to the Python script relative to the project root
  const scriptPath = path.join(__dirname, '..', 'backend', 'api_server.py');
  
  console.log(`Starting Python backend: ${pythonExecutable} ${scriptPath}`);
  
  // Spawn the Python process
  pythonProcess = spawn(pythonExecutable, [scriptPath]);
  
  // Log Python process output
  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });
  
  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });
  
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });
}

// Start the Express server
function startExpressServer() {
  const PORT = 3000;
  
  // API routes
  expressApp.get('/api/status', (req, res) => {
    res.json({ status: 'running' });
  });
  
  // Socket.io connection
  io.on('connection', (socket) => {
    console.log('Client connected');
    
    socket.on('disconnect', () => {
      console.log('Client disconnected');
    });
    
    // Handle command from UI
    socket.on('command', (data) => {
      console.log('Received command:', data);
      // Forward to Python backend via HTTP or other means
      // Then emit response back to client
      socket.emit('response', { 
        success: true, 
        message: `Command "${data.command}" processed` 
      });
    });
  });
  
  // Start server
  server.listen(PORT, () => {
    console.log(`Express server running on port ${PORT}`);
  });
}

// When Electron app is ready
app.whenReady().then(() => {
  const mainWindow = createWindow();
  
  // Start backend services
  startPythonBackend();
  startExpressServer();
  
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    // Kill the Python process when the app is closed
    if (pythonProcess) {
      pythonProcess.kill();
    }
    app.quit();
  }
});

// On macOS, re-create window when dock icon is clicked
app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// Clean up on app quit
app.on('quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
}); 