# AbletonML User Testing Guide

## Overview
Thank you for participating in the AbletonML user testing! This guide will help you test our natural language interface for Ableton Live and provide valuable feedback.

**What is AbletonML?**
AbletonML allows you to control Ableton Live using simple English commands like "set tempo to 120" or "add reverb to track 2".

## Test Environment Setup Checklist

### Prerequisites
- [ ] macOS computer
- [ ] Ableton Live 11 or 12 installed
- [ ] Max for Live installed
- [ ] Python 3.9+ installed
- [ ] Node.js 14+ installed

### Setup Steps
1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/omarsgitx/AbletonML.git
   cd AbletonML
   ```

2. **Install Python dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

4. **Set up Max for Live device**:
   - Open `max/AbletonML_Bridge.maxpat` in Max
   - Export as Max for Live device (.amxd)
   - Load the device into a MIDI track in Ableton Live

5. **Launch AbletonML**:
   ```bash
   npm start
   ```

## Test Script for User Sessions

### Session Duration: 30-45 minutes

### Step 1: Basic Setup (5 minutes)
1. Open Ableton Live and create a new project
2. Load the AbletonML_Bridge device on a MIDI track
3. Launch the AbletonML Electron app
4. Verify connection status shows "Connected"

### Step 2: Basic Commands (10 minutes)
Try these commands in order and observe the results:

#### Tempo Control
- Type: `set tempo to 120`
- Expected: Tempo changes to 120 BPM in Ableton Live
- Try variations: `change bpm to 90`, `set bpm to 140`

#### Track Creation
- Type: `create midi track`
- Expected: New MIDI track appears in Ableton Live
- Try: `create audio track`, `add audio track`

#### Instrument Addition
- Type: `add piano`
- Expected: Piano instrument added to current track
- Try: `add synth`, `add drums`

### Step 3: Effect Commands (10 minutes)
#### Adding Effects
- Type: `add reverb to track 2`
- Expected: Reverb effect added to track 2
- Try: `add delay to track 1`, `add echo to track 3`

#### Effect Parameters
- Type: `set reverb dry/wet to 30%`
- Expected: Reverb dry/wet parameter set to 30%
- Try: `set delay mix to 50`, `set compressor amount to 75%`

### Step 4: Exploration and Edge Cases (10 minutes)
**Try these variations and observe what happens:**

#### Command Variations
- `make midi track` (synonym for create)
- `adjust tempo to 80` (synonym for set)
- `set reverb wet to 80` (different parameter)

#### Edge Cases
- `set tempo to 999` (very high tempo)
- `set tempo to 0` (very low tempo)
- `add reverb to track 99` (non-existent track)
- `set reverb dry/wet to 150%` (invalid percentage)

### Step 5: UI Testing (5 minutes)
- Check the command history panel on the right
- Verify status updates in the status bar
- Try the "Clear History" button
- Observe real-time project state updates

## Feedback Questionnaire Template

### Section 1: Overall Experience
**Rate each item from 1 (Very Poor) to 5 (Excellent)**

| Aspect | Rating (1-5) | Comments |
|--------|-------------|----------|
| Overall ease of use | ___ | |
| Command intuitiveness | ___ | |
| Response speed | ___ | |
| UI clarity | ___ | |
| Would you use this regularly? | ___ | |

### Section 2: Command Understanding
**For each command type, rate how well AbletonML understood your intent:**

| Command Type | Rating (1-5) | What worked well? | What was confusing? |
|--------------|-------------|-------------------|-------------------|
| Tempo commands | ___ | | |
| Track creation | ___ | | |
| Instrument addition | ___ | | |
| Effect addition | ___ | | |
| Effect parameters | ___ | | |

### Section 3: User Interface
**Rate the following UI elements:**

| UI Element | Rating (1-5) | Comments |
|------------|-------------|----------|
| Command input field | ___ | |
| Command history panel | ___ | |
| Status bar updates | ___ | |
| Project state display | ___ | |
| Overall layout | ___ | |

### Section 4: Performance
- **Response time**: How quickly did commands execute? (Too slow / Just right / Too fast)
- **Accuracy**: How often did AbletonML understand your commands correctly? (Rarely / Sometimes / Usually / Always)
- **Reliability**: Did the system crash or freeze during testing? (Yes / No)

### Section 5: Suggestions and Improvements

#### New Commands
What additional commands would you find useful?
```
Examples:
- "mute track 2"
- "record for 30 seconds"
- "add EQ to track 1"
- "set volume to 80%"
```

#### UI Improvements
What would make the interface easier to use?
```
Examples:
- Voice input
- Command suggestions
- Keyboard shortcuts
- Better visual feedback
```

#### General Feedback
What else would you like to share about your experience?
```
```

## Bug Reporting Guidelines

### How to Report Issues

#### 1. Basic Information
- **Date and Time**: When did the issue occur?
- **Command Used**: What command were you trying to execute?
- **Expected Result**: What did you expect to happen?
- **Actual Result**: What actually happened?

#### 2. Error Details
If you see error messages:
- Copy the exact error text
- Note which part of the interface showed the error
- Take a screenshot if possible

#### 3. Reproduction Steps
Provide step-by-step instructions to reproduce the issue:
1. Open Ableton Live
2. Type command: `[your command]`
3. Press Enter
4. Observe: `[what happened]`

#### 4. System Information
- macOS version: `[version]`
- Ableton Live version: `[version]`
- Max for Live version: `[version]`

### Example Bug Report
```
Date: [Date]
Command: "set reverb dry/wet to 150%"
Expected: Error message about invalid percentage
Actual: System crashed
Steps to reproduce:
1. Type "set reverb dry/wet to 150%"
2. Press Enter
3. System crashes
Screenshot: [attached]
```

## Testing Tips

### For Best Results
- **Take your time**: Don't rush through commands
- **Try variations**: Experiment with different ways to say the same thing
- **Observe carefully**: Watch both the AbletonML interface and Ableton Live
- **Note everything**: Even small issues are valuable feedback

### Common Issues to Watch For
- Commands not being recognized
- Delayed responses
- UI not updating
- Ableton Live not responding
- Error messages that aren't helpful

### What to Ignore
- Minor UI glitches that don't affect functionality
- Temporary connection issues that resolve quickly
- Performance issues on slower computers

## Contact Information

If you encounter serious issues or need help:
- **Email**: [Your contact email]
- **GitHub Issues**: [Repository issues page]
- **Documentation**: [Project README]

---

**Thank you for your valuable feedback!** Your input will help make AbletonML better for all users.
