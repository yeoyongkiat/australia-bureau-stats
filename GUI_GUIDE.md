# ABS Data Fetcher GUI - User Guide

**Version:** 1.0  
**Last Updated:** November 2025

---

## 🎨 Overview

The **ABS Data Fetcher GUI** provides a beautiful, user-friendly interface for collecting Australian Bureau of Statistics labour force data. No command line needed!

### Features

✅ **One-Click Operations** - Run scripts with a button press  
✅ **Live Progress Bar** - Visual progress tracking  
✅ **Real-Time Logs** - See checkpoint saves and status updates  
✅ **Status Dashboard** - View last scrape time, record counts, freshness  
✅ **Color-Coded Messages** - Easily identify success, warnings, errors  
✅ **Crash Recovery** - Resume interrupted operations automatically

---

## 🚀 Quick Start

### Prerequisites

**Required:** Only 1 package!

```bash
# Install dependencies
pip install -r requirements.txt

# Or directly
pip install requests>=2.31.0
```

**GUI Note:** Uses `tkinter` (built-in with Python). If GUI won't launch, see [Troubleshooting](#gui-wont-launch).

### Launch the GUI

**Method 1: Double-click (macOS)**
```bash
./launch_gui.sh
```

**Method 2: Command line**
```bash
python3 abs_data_gui.py
```

**Method 3: From Finder**
- Right-click `launch_gui.sh` → Open With → Terminal

---

## 🖥️ Interface Overview

### 1. **Header Section** 🇦🇺
```
🇦🇺 ABS Labour Force Data Fetcher
Automated data collection with checkpoint support
```
- Title and description
- Always visible at the top

### 2. **Status Panel** 📊

Displays real-time information about your data:

| Field | Description | Example |
|-------|-------------|---------|
| **Last Run** | When data was last collected | "2025-11-15 14:30" |
| **Total Records** | Number of records in dataset | "930,000" |
| **Completed** | Progress on combinations | "1620 / 1620" |
| **Data Freshness** | How old is the data | "5 days ago" |
| **Latest Month** | Most recent data point | "2025-10" |
| **Status** | Current operation status | "Ready" / "Fetching..." |

**Status Colors:**
- 🟢 **Green** - Ready, data is fresh (< 7 days)
- 🟠 **Orange** - Warning, data aging (7-30 days)
- 🔴 **Red** - Needs refresh (> 30 days)
- 🔵 **Blue** - Operation in progress

### 3. **Control Panel** 🎮

Four main buttons for all operations:

#### ▶️ **Fetch Data** (Blue)
- **Action:** Runs the data collection script
- **Duration:** 
  - First run: ~65 minutes
  - If data < 30 days: ~10 seconds
- **What happens:**
  - Loads checkpoint (if exists)
  - Fetches needed data
  - Saves checkpoint every 50 requests
  - Auto-runs CSV fixer when done

#### 🔧 **Fix CSV** (Green)
- **Action:** Formats raw CSV into analysis-ready format
- **Duration:** ~5-10 seconds
- **Use when:**
  - After manual data fetch
  - To re-format existing raw CSV
- **Output:** `abs_labour_force_ALL_DATA_*_FIXED.csv`

#### 🔄 **Force Refresh** (Orange)
- **Action:** Deletes checkpoint and forces full data re-fetch
- **Duration:** ~65 minutes on next fetch
- **Use when:**
  - Need guaranteed fresh data
  - Checkpoint seems corrupted
  - Testing or troubleshooting
- **Warning:** Asks for confirmation!

#### ⏹️ **Stop** (Red)
- **Action:** Stops currently running operation
- **Enabled:** Only when a process is running
- **Note:** Progress is saved to checkpoint before stop

**Progress Bar:**
- Visual progress indicator (0-100%)
- Updates automatically during data fetch
- Shows percentage completed

### 4. **Activity Log** 📝

Real-time log of all operations with color coding:

**Color Meanings:**
- 🔵 **Blue (Info)** - General information and progress updates
- 🟢 **Green (Success)** - Successful operations and completions
- 🟠 **Orange (Warning)** - Warnings and important notices
- 🔴 **Red (Error)** - Errors and failures
- 🟣 **Purple (Checkpoint)** - Checkpoint save notifications

**Sample Log:**
```
[14:30:15] Welcome! Click 'Fetch Data' to start collecting data.
[14:30:20] Starting data fetch...
[14:30:25] Progress: [50/1620] (3.1%)
[14:32:18] 💾 Checkpoint saved (50 successful, 0 failed)
[14:34:12] Progress: [100/1620] (6.2%)
[14:36:05] 💾 Checkpoint saved (100 successful, 0 failed)
...
[15:35:45] ✅ Data saved to: abs_labour_force_ALL_DATA_20251115_143545.csv
[15:35:50] ✅ Success! Saved 930,000 records
```

**Log Management:**
- Scrolls automatically to show latest
- "Clear Log" button to reset
- Timestamps for all messages

### 5. **Footer** 
- "🔄 Refresh Status" button - Updates status panel manually
- "Ministry of Health | Policy Research" - Organization info

---

## 📖 Usage Scenarios

### Scenario 1: First Time Data Collection

1. **Launch GUI**
   ```bash
   python3 abs_data_gui.py
   ```

2. **Check Status Panel**
   - Last Run: "Never"
   - Total Records: "0"
   - Data Freshness: "No data yet"

3. **Click "▶️ Fetch Data"**
   - Watch progress bar fill up
   - See checkpoint saves every ~2 minutes
   - Log shows real-time updates

4. **Wait ~65 minutes**
   - Progress bar reaches 100%
   - Status shows "✅ Success!"
   - CSV automatically formatted

5. **Check Updated Status**
   - Last Run: Shows current time
   - Total Records: "~930,000"
   - Completed: "1620 / 1620"

### Scenario 2: Monthly Update (< 30 Days)

1. **Launch GUI**

2. **Status Shows:**
   - Last Run: "15 days ago"
   - Data Freshness: "15 days ago" (Orange)

3. **Click "▶️ Fetch Data"**

4. **Watch Magic Happen:**
   ```
   [14:30:20] Loaded checkpoint with 1620 completed combinations
   [14:30:20] Already up-to-date: 1620
   [14:30:20] Combinations to fetch: 0
   [14:30:25] ✅ Completed in 5 seconds!
   ```

5. **Done!** - No new data needed, completes instantly

### Scenario 3: Force Refresh

1. **Click "🔄 Force Refresh"**

2. **Confirmation Dialog:**
   ```
   This will delete the checkpoint and fetch ALL data 
   from scratch (~65 minutes).
   
   Are you sure?
   [Yes] [No]
   ```

3. **Click "Yes"**
   - Checkpoint deleted
   - Log shows: "Checkpoint deleted. Next run will fetch all data."

4. **Click "▶️ Fetch Data"**
   - Fetches all 1,620 combinations
   - Takes ~65 minutes
   - Creates fresh checkpoint

### Scenario 4: Interrupted Operation (Crash Recovery)

**Initial Run:**
1. Click "▶️ Fetch Data"
2. At 50% (810/1620), network dies
3. Click "⏹️ Stop" or close GUI

**Resume:**
1. Launch GUI again
2. Click "▶️ Fetch Data"
3. Log shows:
   ```
   [14:45:10] Loaded checkpoint with 810 completed combinations
   [14:45:10] Already up-to-date: 810
   [14:45:10] Combinations to fetch: 810
   [14:45:10] Estimated time: 32.4 minutes
   ```
4. Resumes from 50% automatically!

### Scenario 5: Fix Existing CSV

1. **You have:** `abs_labour_force_ALL_DATA_20251115_143545.csv`
2. **Click:** "🔧 Fix CSV"
3. **Wait:** ~5-10 seconds
4. **Output:** `abs_labour_force_ALL_DATA_20251115_143545_FIXED.csv`

---

## 🎯 Tips & Tricks

### Daily/Weekly Checks
```
1. Launch GUI
2. Look at "Data Freshness"
3. If green (< 7 days): Do nothing!
4. If orange (7-30 days): Optional update
5. If red (> 30 days): Click "Fetch Data"
```

### Monthly Routine
```
15th of each month:
1. Launch GUI
2. Click "Fetch Data"
3. If last run < 30 days: Completes in 10 seconds ✨
4. If last run > 30 days: Takes 65 minutes
```

### Before Important Analysis
```
1. Click "Force Refresh" (to get absolutely fresh data)
2. Confirm the dialog
3. Click "Fetch Data"
4. Wait ~65 minutes
5. Use the FIXED.csv file for analysis
```

### Monitoring Long Runs
```
- Watch the progress bar
- Look for purple "💾 Checkpoint saved" messages every ~2 minutes
- Progress updates show [current/total] combinations
- If something looks stuck, check the log
```

### Quick Status Check
```
- Click "🔄 Refresh Status" button
- Updates all status panel fields
- Reads from checkpoint file
- No network required
```

---

## ⚠️ Important Notes

### Do Not Close Terminal While Running
- GUI needs terminal window to run
- Closing terminal = stops the process
- **Exception:** Progress is saved to checkpoint, can resume later

### Progress Bar Behavior
- Updates based on log messages
- May not move smoothly (updates every 50 requests)
- 0% → periodic jumps → 100%
- This is normal!

### Status Panel Updates
- Auto-updates after each operation
- Can manually refresh with "🔄 Refresh Status" button
- Reads from `abs_fetch_checkpoint.json`

### Stop Button Safety
- Stopping mid-fetch is safe
- Progress saved to checkpoint
- Can resume by clicking "Fetch Data" again
- Already-fetched data is not lost

---

## 🐛 Troubleshooting

### GUI Won't Launch

**Problem:** `python3 abs_data_gui.py` shows error

**Solutions:**
```bash
# Check Python version (need 3.8+)
python3 --version

# Check tkinter is installed
python3 -c "import tkinter; print('OK')"

# If tkinter missing (macOS):
brew install python-tk

# If tkinter missing (Linux):
sudo apt-get install python3-tk
```

### Buttons Don't Work

**Problem:** Clicking buttons does nothing

**Solution:**
- Check terminal for error messages
- Ensure `fetch_abs_data_auto.py` and `fix_abs_csv.py` exist in same folder
- Check file permissions: `ls -l *.py`

### Status Panel Shows "Error"

**Problem:** Status fields show "Error" or "Unknown"

**Solution:**
```bash
# Check if checkpoint file exists
ls -lh abs_fetch_checkpoint.json

# If corrupted, delete and refresh
rm abs_fetch_checkpoint.json

# Click "Refresh Status" in GUI
```

### Progress Bar Stuck

**Problem:** Progress bar not moving during fetch

**Check:**
- Look at log messages - are they appearing?
- If yes: Progress bar updates every 50 requests (~2 min)
- If no: Check terminal for errors

**Solution:**
- If truly stuck for > 5 minutes, click "Stop"
- Check `abs_data_fetch.log` for errors
- Try running command line to see error: `python3 fetch_abs_data_auto.py`

### Log Shows Errors

**Common Errors:**

1. **"401 Authentication Error"**
   - API key invalid or expired
   - Update API key in `fetch_abs_data_auto.py`

2. **"ModuleNotFoundError: requests"**
   - Dependencies not installed
   - Run: `pip install -r requirements.txt`

3. **"FileNotFoundError"**
   - Wrong working directory
   - Launch GUI from project folder

---

## 🎨 Customization

### Change Window Size

Edit `abs_data_gui.py`, line 29:
```python
self.root.geometry("1000x800")  # Width x Height
```

### Change Colors

Edit color scheme, lines 36-40:
```python
self.accent_color = "#2196F3"   # Blue (fetch button)
self.success_color = "#4CAF50"  # Green (success/fix button)
self.warning_color = "#FF9800"  # Orange (warning/refresh button)
self.error_color = "#F44336"    # Red (error/stop button)
```

### Change Freshness Thresholds

Edit `fetch_abs_data_auto.py`, line 77:
```python
DATA_FRESHNESS_DAYS = 30  # Change this
```

---

## 📊 Status Panel Reference

### Last Run
- **Format:** `YYYY-MM-DD HH:MM`
- **Source:** Checkpoint file `last_run` field
- **Example:** `2025-11-15 14:30`

### Total Records
- **Format:** Number with commas
- **Source:** Checkpoint file `total_records` field
- **Example:** `930,000`

### Completed
- **Format:** `current / total`
- **Total:** Always 1,620 (9 regions × 20 data items × 3 sex × 3 adj types)
- **Example:** `1620 / 1620`

### Data Freshness
- **Today** (Green) - Data collected today
- **Yesterday** (Green) - Data from yesterday
- **X days ago** (Green) - < 7 days old
- **X days ago** (Orange) - 7-30 days old
- **X days ago (Needs refresh)** (Red) - > 30 days old

### Latest Month
- **Format:** `YYYY-MM`
- **Source:** Most recent `observation_month` from checkpoint
- **Example:** `2025-10`

### Status
- **Ready** (Green) - No operation running
- **Fetching data...** (Blue) - Data collection in progress
- **Fixing CSV...** (Blue) - CSV formatting in progress
- **Stopped** (Orange) - Operation stopped by user

---

## 🔧 Advanced Features

### Run in Background

Keep GUI running while doing other work:
```bash
# Launch and minimize terminal
python3 abs_data_gui.py &
```

### Multiple Monitors

GUI remembers window position. Drag to preferred monitor for future launches.

### Keyboard Shortcuts

Currently not implemented, but could add:
- `Cmd+R` / `Ctrl+R` - Refresh status
- `Cmd+L` / `Ctrl+L` - Clear log
- `Cmd+Q` / `Ctrl+Q` - Quit

---

## 📋 Quick Reference Card

| Action | Button | Duration | Notes |
|--------|--------|----------|-------|
| **First data fetch** | ▶️ Fetch Data | ~65 min | Creates checkpoint |
| **Monthly update** | ▶️ Fetch Data | ~10 sec | If < 30 days |
| **Format CSV** | 🔧 Fix CSV | ~10 sec | After fetch |
| **Force fresh** | 🔄 Force Refresh | ~65 min | Deletes checkpoint |
| **Stop operation** | ⏹️ Stop | Instant | Progress saved |
| **Update status** | 🔄 Refresh Status | Instant | Reads checkpoint |

---

## 📚 See Also

- **CHECKPOINT_QUICKSTART.md** - Checkpoint system basics
- **CHECKPOINT_GUIDE.md** - Detailed checkpoint documentation
- **ABS_DATA_ONBOARDING.md** - Complete system documentation

---

## 💡 Pro Tips

1. **Leave GUI running** during fetch - you can minimize and do other work
2. **Watch for purple checkpoint messages** - ensures progress is saved
3. **Status panel auto-refreshes** after operations - no manual refresh needed
4. **Clear log periodically** - keeps interface clean and responsive
5. **Force refresh quarterly** - ensures highest quality data

---

## 🎓 Key Takeaways

- **Easy to use** - Just click buttons!
- **Visual feedback** - Progress bar + colored logs
- **Crash-proof** - Checkpoint system auto-resumes
- **Smart skipping** - Monthly runs complete instantly
- **Status dashboard** - Always know your data state

---

**Questions?** Check the log panel for hints or see `ABS_DATA_ONBOARDING.md` for detailed help.

**Enjoy your user-friendly ABS data collection! 🎉**

