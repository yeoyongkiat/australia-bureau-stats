# Quick Reference Card
## ABS Data Fetcher - At a Glance

---

## 📦 **Transfer to New Computer**

### Copy These Files:
```
✅ abs_data_gui.py
✅ fetch_abs_data_auto.py
✅ fix_abs_csv.py
✅ requirements.txt
```

### Install One Package:
```bash
pip install requests
```

### Launch:
```bash
python3 abs_data_gui.py
```

---

## 🚀 **Daily Use**

### Launch GUI:
```bash
python3 abs_data_gui.py
```

### Monthly Routine:
1. Launch GUI
2. Click "▶️ Fetch Data"
3. Wait (10 seconds if recent, 65 min if > 30 days)
4. Use the `_FIXED.csv` file

---

## 🔑 **API Key**

**Get key:** https://developer.vic.gov.au  
**Enter in:** GUI top panel → Click "💾 Save"  
**Saves to:** `abs_api_config.json` (auto-loads next time)

---

## 📁 **Output Files**

**Use this one for analysis:**
```
abs_labour_force_ALL_DATA_YYYYMMDD_HHMMSS_FIXED.csv
```

**Ignore:**
- Raw CSV (without _FIXED)
- .log files
- checkpoint.json

---

## 💾 **Checkpoint System**

- **Saves:** Every 2 minutes
- **Resumes:** Automatically after crash
- **Skips:** Data < 30 days old
- **Force refresh:** Click "🔄 Force Refresh" button

---

## 🎮 **GUI Buttons**

- **▶️ Fetch Data** - Start collection
- **🔄 Force Refresh** - Delete checkpoint, fetch all
- **⏹️ Stop** - Safely stop (progress saved)
- **❓ Help** - Show detailed help

---

## 📊 **Status Colors**

- 🟢 **Green** - Fresh (< 7 days)
- 🟠 **Orange** - Aging (7-30 days)
- 🔴 **Red** - Needs refresh (> 30 days)

---

## 🐛 **Quick Troubleshooting**

**GUI won't launch:**
```bash
pip install requests
python3 -c "import tkinter; print('OK')"
```

**No API key error:**
- Enter API key in GUI
- Click "💾 Save"

**Button text hard to see:**
- Updated! Text is now black

---

## 📖 **Documentation**

- **Setup:** `ABS_DATA_ONBOARDING.md`
- **GUI:** `GUI_GUIDE.md`
- **Transfer:** `TRANSFER_GUIDE.md`
- **Windows:** `WINDOWS_SETUP.md`
- **Checkpoints:** `CHECKPOINT_GUIDE.md`

---

## ⚡ **Super Quick Start**

```bash
# 1. Copy 4 files to folder
# 2. Install
pip install requests

# 3. Launch
python3 abs_data_gui.py

# 4. Enter API key, click Save
# 5. Click "Fetch Data"
# Done!
```

---

## 🔢 **Key Numbers**

- **Files to copy:** 4
- **Packages to install:** 1 (requests)
- **First run:** ~65 minutes
- **Monthly run:** ~10 seconds
- **Total data:** ~930,000 records
- **API calls:** 1,620 per complete run

---

## 💡 **Pro Tips**

1. Run monthly (15th of each month)
2. Always use `_FIXED.csv` files
3. Watch for purple checkpoint saves
4. Orange "not available" messages are normal
5. Can stop/resume anytime

---

**That's everything you need to know! 🎉**

---

*Ministry of Health | Policy Research*

