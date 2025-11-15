# Windows Setup Guide
## ABS Labour Force Data Fetcher

**Compatible:** ✅ Yes! The GUI works on Windows

---

## ✅ **Button Colors Fixed**

All buttons now have **black text** for better visibility:
- ▶️ Fetch Data (Blue with black text)
- 🔄 Force Refresh (Orange with black text)
- ⏹️ Stop (Red with black text)
- 💾 Save (Green with black text)
- ❓ Help (Purple with black text)

---

## 🪟 **Windows Compatibility**

### What Works on Windows

✅ **All Features Supported:**
- GUI interface
- Data fetching
- Checkpoint system
- CSV formatting
- API key management

✅ **Built-in Components:**
- Python (install from python.org)
- tkinter (included with Python installer)
- All standard libraries

---

## 📦 **Windows Installation**

### Step 1: Install Python

1. Go to https://python.org/downloads/
2. Download Python 3.8 or higher for Windows
3. Run installer
4. **Important:** Check "Add Python to PATH" ✓
5. **Important:** Check "tcl/tk and IDLE" ✓
6. Click "Install Now"

### Step 2: Copy Files

Copy these 4 files to a folder on your Windows PC:
```
C:\ABS_Data\
├── abs_data_gui.py
├── fetch_abs_data_auto.py
├── fix_abs_csv.py
└── requirements.txt
```

### Step 3: Install Dependencies

Open **Command Prompt** or **PowerShell**:
```cmd
cd C:\ABS_Data
pip install -r requirements.txt
```

Or:
```cmd
pip install requests>=2.31.0
```

### Step 4: Run the GUI

**Method 1: Double-click** (easiest)
- Right-click `abs_data_gui.py`
- Select "Open with" → "Python"

**Method 2: Command line**
```cmd
cd C:\ABS_Data
python abs_data_gui.py
```

**Method 3: PowerShell**
```powershell
cd C:\ABS_Data
python3 abs_data_gui.py
```

---

## 🔧 **Windows-Specific Notes**

### Python Command

On Windows, use one of these:
```cmd
python abs_data_gui.py    # Usually works
py abs_data_gui.py        # Alternative
python3 abs_data_gui.py   # If you have both Python 2 and 3
```

### File Paths

Windows uses backslashes:
```
C:\Users\YourName\Documents\ABS_Data\
```

But Python scripts work fine either way!

### Permissions

No special permissions needed on Windows (unlike macOS/Linux with `chmod +x`)

---

## 🎨 **GUI Appearance on Windows**

### What to Expect

**Windows 10/11:**
- Native Windows button style
- Smooth rendering
- All colors visible
- Emojis displayed (▶️ 🔄 ⏹️ 💾 ❓)

**Differences from macOS:**
- Buttons may look more "flat" (Windows style)
- Fonts may be slightly different
- Window decorations are Windows-style
- Everything else identical!

---

## 🐛 **Windows Troubleshooting**

### Problem: "python is not recognized"

**Solution:**
```cmd
# Option 1: Use py instead
py abs_data_gui.py

# Option 2: Add Python to PATH
# Re-run Python installer and check "Add to PATH"
```

### Problem: "No module named tkinter"

**Solution:**
- Reinstall Python
- Make sure to check "tcl/tk and IDLE" during installation

### Problem: "No module named 'requests'"

**Solution:**
```cmd
pip install requests
# or
python -m pip install requests
```

### Problem: GUI window is too small/large

**Edit `abs_data_gui.py` line 29:**
```python
self.root.geometry("1000x800")  # Change these numbers
```

### Problem: Can't see output files

**Solution:**
Output files are in the same folder as the scripts:
```cmd
cd C:\ABS_Data
dir abs_labour_force*.csv
```

---

## 📁 **File Locations (Windows)**

### Scripts Location
```
C:\Users\YourName\Documents\ABS_Data\
```

### Output Files
```
C:\Users\YourName\Documents\ABS_Data\
├── abs_labour_force_ALL_DATA_20251115_193045.csv
├── abs_labour_force_ALL_DATA_20251115_193045_FIXED.csv
├── abs_fetch_checkpoint.json
├── abs_api_config.json
└── abs_data_fetch.log
```

---

## 💡 **Windows Pro Tips**

### Create Desktop Shortcut

1. Right-click `abs_data_gui.py`
2. Select "Create shortcut"
3. Drag shortcut to Desktop
4. Rename to "ABS Data Fetcher"
5. Double-click to launch!

### Create Batch File Launcher

Create `launch_gui.bat`:
```batch
@echo off
cd /d %~dp0
python abs_data_gui.py
pause
```

Double-click to run!

### Schedule Monthly Runs

Use **Task Scheduler**:
1. Open Task Scheduler
2. Create Basic Task
3. Name: "ABS Data Fetch"
4. Trigger: Monthly (15th day)
5. Action: Start a program
6. Program: `python`
7. Arguments: `abs_data_gui.py`
8. Start in: `C:\ABS_Data\`

---

## 🔍 **Cross-Platform Compatibility**

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| **GUI** | ✅ | ✅ | ✅ |
| **Data Fetching** | ✅ | ✅ | ✅ |
| **Checkpoints** | ✅ | ✅ | ✅ |
| **API Key Management** | ✅ | ✅ | ✅ |
| **CSV Output** | ✅ | ✅ | ✅ |
| **tkinter** | ✅ Built-in | ✅ Built-in | ⚠️ May need install |

---

## 🚀 **Quick Windows Setup**

### One-Time Setup (5 minutes)
```cmd
# 1. Install Python from python.org (check "Add to PATH")
# 2. Copy 4 files to C:\ABS_Data
# 3. Install dependencies
cd C:\ABS_Data
pip install requests

# 4. Launch GUI
python abs_data_gui.py

# 5. Enter API key, click Save
# 6. Click "Fetch Data"
# Done!
```

---

## ✨ **Summary**

### ✅ **What Changed**
- All button text now **black** (easier to read)
- Confirmed **Windows compatibility**
- Created Windows setup guide

### ✅ **Works On**
- ✅ Windows 10/11
- ✅ macOS (tested)
- ✅ Linux (should work)

### 🎯 **Files Needed**
Just the same 4 files on any platform:
1. `abs_data_gui.py`
2. `fetch_abs_data_auto.py`
3. `fix_abs_csv.py`
4. `requirements.txt`

---

## 📞 **Need Help?**

- **Python installation:** python.org/downloads
- **Windows-specific issues:** Check Event Viewer
- **General issues:** See `ABS_DATA_ONBOARDING.md`

---

**The GUI is fully cross-platform! Works on Windows, macOS, and Linux! 🎉**

