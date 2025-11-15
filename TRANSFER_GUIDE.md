# Transfer Guide - Moving to Another Computer
## ABS Labour Force Data Fetcher

**Time Required:** 5 minutes  
**Difficulty:** Easy

---

## 📦 **What to Copy**

### Essential Files (Required)

Copy these **4 files** to your new computer:

```
✅ abs_data_gui.py
✅ fetch_abs_data_auto.py
✅ fix_abs_csv.py
✅ requirements.txt
```

**Size:** ~50 KB total (very small!)

### Optional Files (Recommended)

If these exist, copy them to preserve your settings:

```
⭐ abs_api_config.json          (Saves your API key)
⭐ abs_fetch_checkpoint.json    (Preserves progress)
```

**Why optional?**
- Without them, you'll just re-enter the API key
- Checkpoint will start fresh (no big deal)

### Documentation (Optional but Helpful)

```
📖 ABS_DATA_ONBOARDING.md
📖 GUI_GUIDE.md
📖 CHECKPOINT_GUIDE.md
📖 TRANSFER_GUIDE.md (this file)
📖 WINDOWS_SETUP.md (if transferring to Windows)
```

---

## 🖥️ **Step-by-Step Transfer**

### Step 1: Copy Files

**From your current computer:**

**Option A: USB Drive**
```bash
# Copy to USB
cp abs_data_gui.py /Volumes/USB_DRIVE/
cp fetch_abs_data_auto.py /Volumes/USB_DRIVE/
cp fix_abs_csv.py /Volumes/USB_DRIVE/
cp requirements.txt /Volumes/USB_DRIVE/

# Optional: Copy settings
cp abs_api_config.json /Volumes/USB_DRIVE/
cp abs_fetch_checkpoint.json /Volumes/USB_DRIVE/
```

**Option B: Cloud (Dropbox, Google Drive, OneDrive)**
```bash
# Copy to cloud folder
cp *.py ~/Dropbox/ABS_Transfer/
cp requirements.txt ~/Dropbox/ABS_Transfer/
cp abs_api_config.json ~/Dropbox/ABS_Transfer/  # Optional
```

**Option C: Email to Yourself**
- Attach all 4 files to an email
- Send to yourself
- Download on new computer

**Option D: GitHub/Git**
```bash
# On current computer
git add abs_data_gui.py fetch_abs_data_auto.py fix_abs_csv.py requirements.txt
git commit -m "ABS Data Fetcher files"
git push

# On new computer
git clone <your-repo>
```

**⚠️ Note:** Don't commit `abs_api_config.json` to git (contains your API key!)

### Step 2: Setup on New Computer

**On your new computer:**

1. **Check Python is installed** (3.8 or higher)
   ```bash
   python3 --version
   # Should show: Python 3.8.x or higher
   ```

2. **Create a folder**
   ```bash
   # macOS/Linux
   mkdir ~/ABS_Data
   cd ~/ABS_Data
   
   # Windows
   mkdir C:\ABS_Data
   cd C:\ABS_Data
   ```

3. **Copy the files into this folder**

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or:
   ```bash
   pip install requests>=2.31.0
   ```

5. **Launch the GUI**
   ```bash
   python3 abs_data_gui.py
   ```

6. **Enter API key** (if you didn't copy `abs_api_config.json`)
   - Paste your API key in the field
   - Click "💾 Save"

7. **Done!** Click "▶️ Fetch Data"

---

## 🔄 **Platform-Specific Notes**

### Transferring macOS → macOS
✅ **Direct copy works perfectly**
- No changes needed
- All files compatible

### Transferring macOS → Windows
✅ **Works with minor adjustments**
- Use `python` instead of `python3`
- Paths use backslashes: `C:\ABS_Data\`
- See `WINDOWS_SETUP.md` for details

### Transferring macOS → Linux
✅ **Works perfectly**
- May need to install tkinter: `sudo apt-get install python3-tk`
- Everything else identical

### Transferring Windows → macOS
✅ **Works perfectly**
- Use `python3` instead of `python`
- Everything else identical

---

## 📋 **Quick Checklist**

Before you start:
- [ ] Python 3.8+ installed on new computer
- [ ] pip installed (`python3 -m pip --version`)
- [ ] Internet connection (to install packages)
- [ ] Your API key handy (if not copying config file)

Files to copy:
- [ ] `abs_data_gui.py`
- [ ] `fetch_abs_data_auto.py`
- [ ] `fix_abs_csv.py`
- [ ] `requirements.txt`
- [ ] `abs_api_config.json` (optional)
- [ ] `abs_fetch_checkpoint.json` (optional)

On new computer:
- [ ] Created destination folder
- [ ] Copied all files
- [ ] Ran `pip install -r requirements.txt`
- [ ] Launched GUI successfully
- [ ] Entered/loaded API key
- [ ] Tested data fetch

---

## 💾 **What Gets Created on New Computer**

After first run, these files will be created:

```
Your Folder/
├── abs_data_gui.py                    (copied)
├── fetch_abs_data_auto.py             (copied)
├── fix_abs_csv.py                     (copied)
├── requirements.txt                   (copied)
├── abs_api_config.json                (created when you save API key)
├── abs_fetch_checkpoint.json          (created during data fetch)
├── abs_data_fetch.log                 (created during data fetch)
├── abs_labour_force_ALL_DATA_*.csv    (output - raw data)
└── abs_labour_force_ALL_DATA_*_FIXED.csv (output - analysis-ready)
```

---

## 🔑 **About the API Key**

### Option 1: Copy the Config File
If you copy `abs_api_config.json`:
- ✅ API key auto-loads
- ✅ No re-entry needed
- ✅ Ready to go immediately

### Option 2: Re-enter in GUI
If you don't copy the config file:
1. Launch GUI
2. Enter API key in field
3. Click "💾 Save"
4. Done!

**Your API key:** You can find it at https://developer.vic.gov.au

---

## 📊 **What About Existing Data?**

### Your CSV Files
**Don't need to transfer!**
- Old data stays on old computer
- New computer starts fresh
- Each computer can have its own data

**But if you want to transfer data:**
```bash
# Copy the FIXED CSV files (these are analysis-ready)
cp abs_labour_force_*_FIXED.csv /path/to/new/computer/
```

### Your Checkpoint
**Optional to transfer:**
- If you transfer `abs_fetch_checkpoint.json`:
  - New computer knows what's already fetched
  - Won't re-fetch recent data
  - Saves time on first run

- If you don't transfer it:
  - New computer starts fresh
  - Will fetch everything (takes ~65 min first time)
  - No problem, just takes a bit longer

---

## 🚀 **Quick Transfer (5 Minutes)**

### Absolute Fastest Method

**On current computer:**
```bash
# Create a zip file with everything
zip abs_fetcher.zip abs_data_gui.py fetch_abs_data_auto.py fix_abs_csv.py requirements.txt abs_api_config.json

# Transfer abs_fetcher.zip to new computer (email, USB, cloud)
```

**On new computer:**
```bash
# Extract
unzip abs_fetcher.zip

# Install
pip install requests

# Run
python3 abs_data_gui.py

# Done! API key already loaded, ready to fetch!
```

**Total time: 5 minutes** ⚡

---

## 🐛 **Troubleshooting**

### "python3: command not found"
**Solution:**
```bash
# Try just 'python'
python abs_data_gui.py

# Or install Python from python.org
```

### "No module named 'tkinter'"
**Solution:**
```bash
# macOS
brew install python-tk

# Linux
sudo apt-get install python3-tk

# Windows - reinstall Python, check "tcl/tk and IDLE"
```

### "No module named 'requests'"
**Solution:**
```bash
pip install requests
```

### GUI won't launch
**Check:**
```bash
# Verify files copied correctly
ls -la abs_data_gui.py fetch_abs_data_auto.py fix_abs_csv.py requirements.txt

# Check Python version
python3 --version  # Should be 3.8+

# Check tkinter
python3 -c "import tkinter; print('OK')"
```

---

## 📱 **Multiple Computers Setup**

### Scenario: Work Computer + Home Computer

**Option 1: Independent Setup**
- Each computer has its own files
- Each collects data independently
- Keep most recent data from either

**Option 2: Synced Setup**
- Put files in Dropbox/OneDrive/Google Drive
- Both computers use same folder
- Share API key and checkpoint
- ⚠️ Don't run simultaneously!

**Option 3: USB Drive**
- Keep files on USB drive
- Plug into whichever computer you're using
- Take your data with you

---

## ✅ **Summary**

### Must Copy (4 files):
```
abs_data_gui.py
fetch_abs_data_auto.py
fix_abs_csv.py
requirements.txt
```

### Python Package (1 package):
```
requests
```

### That's It!
- No database setup needed
- No complex configuration
- No additional software
- Just copy files and run!

---

## 🎯 **Final Checklist**

Transfer complete when:
- [✓] 4 essential files copied
- [✓] `pip install requests` run successfully
- [✓] GUI launches without errors
- [✓] API key entered and saved
- [✓] Test fetch works (try for 30 seconds, then stop)

**You're ready to collect ABS data on your new computer! 🎉**

---

## 📞 **Need Help?**

- **General setup:** See `ABS_DATA_ONBOARDING.md`
- **GUI help:** See `GUI_GUIDE.md`
- **Windows specific:** See `WINDOWS_SETUP.md`
- **Checkpoint system:** See `CHECKPOINT_GUIDE.md`

---

**Transfer is simple: 4 files + 1 package = Done!** ✨

