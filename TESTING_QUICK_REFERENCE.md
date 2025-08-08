# AbletonML Testing Quick Reference

## Essential Commands to Test

### ✅ Basic Commands
```
set tempo to 120
create midi track
add piano
add reverb to track 2
```

### 🔧 Advanced Commands
```
change bpm to 90
add audio track
set reverb dry/wet to 30%
set delay mix to 50
```

### 🧪 Edge Cases to Try
```
set tempo to 999
set reverb dry/wet to 150%
add reverb to track 99
make midi track
```

## Quick Troubleshooting

### If AbletonML won't start:
1. Check Python version: `python3 --version`
2. Check Node.js version: `node --version`
3. Reinstall dependencies: `pip install -r requirements.txt`

### If commands aren't working:
1. Check connection status in status bar
2. Verify Max for Live device is loaded in Ableton Live
3. Try restarting both Ableton Live and AbletonML

### If you see errors:
1. Copy the error message
2. Note what command you were trying
3. Take a screenshot if possible

## What to Look For

### ✅ Good Signs
- Commands execute within 1-2 seconds
- Status bar shows "Executed: [command]"
- Command history shows ✅ success icons
- Ableton Live responds immediately

### ❌ Problem Signs
- Commands take more than 5 seconds
- Status bar shows "Error: [message]"
- Command history shows ❌ error icons
- Ableton Live doesn't respond

## Rating Scale Reference

**1 = Very Poor** - Didn't work at all, very frustrating
**2 = Poor** - Worked poorly, needs major improvement
**3 = Fair** - Worked okay, but could be better
**4 = Good** - Worked well, minor issues
**5 = Excellent** - Worked perfectly, very intuitive

## Contact for Help

- **Email**: [Your email]
- **GitHub**: [Repository URL]
- **Documentation**: [README URL]

---

**Remember**: Your feedback is valuable! Even negative feedback helps us improve.
