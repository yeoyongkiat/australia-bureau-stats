---
author: Yeo Yong Kiat, Ministry of Health
date: 14 Nov 2025
program phase: beta-testing (potential bugs, may require fixing if you find them)
---

# 🇦🇺 ABS Labour Force Data Fetcher

This is a Python application with a GUI for fetching, processing, and managing Australian Bureau of Statistics (ABS) Labour Force data. Features automatic checkpointing, rate limiting, and crash recovery.

## 🎯 What Does This Do?

This tool automatically fetches comprehensive labour force statistics from the ABS Labour Force API across:
- **All Australian regions** (Australia-wide + states/territories)
- **All demographic breakdowns** (age groups, sex, employment types)
- **All data items** (unemployment, employment, participation rates, etc.)
- **Historical data** spanning multiple years

The data is saved to timestamped CSV files, ready for analysis in Excel, Python, R, or any data analysis tool.

The ABS Labour Force API provides Australian Bureau of Statistics labor force data in an easily consumable format for developers. Labour force data includes employment statistics by region, sex, age groups and labour utilisation using original, seasonally adjusted and trend markers since 1978. Read the actual documentation at https://wovg-community.portal.prod.api.vic.gov.au/index.php?option=com_apiportal&view=apitester&usage=api&apitab=tests&apiName=ABS+Labour+Force+API&apiId=964c424e-ef9e-44d3-8c0c-64e145c0465b&managerId=1&type=rest&apiVersion=1.0.0&Itemid=153&swaggerVersion=2.0

---

## ⚡ Quick Start

### 1️⃣ **First Time Setup** (2 minutes)

1. Download all files into the same folder on your computer

2. Open your terminal and run the following commands:

```bash
# Install Python dependency (just one!)
pip3 install requests

# Run the GUI
python3 abs_data_gui.py
```

3. If any other Python packages need to be installed, there will be error messages. Read these messages to figure out what other packages you will need to install, if your default Python package in Anaconda doesn't have them.

### 2️⃣ **Enter Your API Key**
- Get your free API key from: https://developer.vic.gov.au
- Paste it in the GUI's API Key field
- Click "💾 Save"

### 3️⃣ **Fetch Data**
- Click "▶️ Fetch Data"
- Watch the progress bar
- Get your timestamped CSV file when complete!

**That's it!** 🎉

---

## 📁 What's In This Repository?

### 🖥️ **Application Files** (The Core)

| File | What It Does | When You Need It |
|------|-------------|------------------|
| **`abs_data_gui.py`** | 🖥️ Graphical interface for running everything | **START HERE** - Main app |
| **`fetch_abs_data_auto.py`** | 🤖 Automated data fetching script | Runs automatically via GUI |
| **`fix_abs_csv.py`** | 🔧 CSV formatting and cleanup utility | Runs automatically via GUI |
| **`requirements.txt`** | 📦 Python package dependencies (just `requests`) | For installation |

### 📚 **Documentation Files** (Read These)

| File | What It Contains | Read This When... |
|------|-----------------|-------------------|
| **`QUICK_REFERENCE.md`** | ⚡ **START HERE!** One-page cheat sheet | You need quick answers |
| **`TRANSFER_GUIDE.md`** | 🔄 How to transfer this to another computer | Setting up on new PC |
| **`ABS_DATA_ONBOARDING.md`** | 📘 Complete system documentation | You want full details |
| **`GUI_GUIDE.md`** | 🖥️ Detailed GUI user manual | Learning the interface |
| **`CHECKPOINT_GUIDE.md`** | 💾 Checkpoint system deep-dive | Advanced usage |
| **`WINDOWS_SETUP.md`** | 🪟 Windows-specific setup instructions | Using on Windows |

---

## 🎓 Documentation Guide

**Not sure what to read first?** Follow this path:

```
1. QUICK_REFERENCE.md     ⚡ Start here (5 min read)
   ↓
2. TRANSFER_GUIDE.md      🔄 Setup instructions (if new computer)
   ↓
3. GUI_GUIDE.md           🖥️ How to use the interface (10 min read)
   ↓
4. ABS_DATA_ONBOARDING.md 📘 Complete reference (when needed)
```

**For specific needs:**
- 🪟 **Windows user?** → Read `WINDOWS_SETUP.md`
- 💾 **Want to understand checkpoints?** → Read `CHECKPOINT_GUIDE.md`
- ⚡ **Just need commands?** → Read `QUICK_REFERENCE.md`

---

## 🚀 Installation

### Option 1: Simple (Recommended)

```bash
pip3 install requests
```

That's it! Only one package needed.

### Option 2: Using requirements.txt

```bash
pip3 install -r requirements.txt
```

---

## 💡 Usage Examples

### GUI Mode (Recommended)

```bash
python3 abs_data_gui.py
```

Then:
1. Enter API key → Click "💾 Save"
2. Click "▶️ Fetch Data"
3. Watch progress bar
4. Get CSV file: `abs_labour_force_data_FIXED_YYYYMMDD_HHMMSS.csv`

Using the GUI, you only need to click "▶️ Fetch Data" and all the execution will be performed manually for you.

### Command Line Mode (Advanced)

If you prefer the Command Line, or maybe if there's a bug in the code that you want to fix, you then need to run the fetch_abs_data_auto.py file first. Once it completes, run the fix_abs_csv.py file.

```bash
# Fetch all data
python3 fetch_abs_data_auto.py --api-key YOUR_API_KEY

# Fix a specific CSV file
python3 fix_abs_csv.py
```

---

## ✨ Key Features

### 🎮 **User-Friendly GUI**
- One-click data fetching
- Real-time progress tracking
- Color-coded status indicators
- Built-in help system

### 💾 **Smart Checkpointing**
- Automatic progress saving every 50 requests
- Resume from interruption
- Skip already-fetched combinations
- Only fetch new data on subsequent runs

### ⚡ **Rate Limiting**
- Respects ABS API limit (25 requests/minute)
- Sliding window algorithm
- Automatic throttling
- No manual delays needed

### 🔧 **Automatic CSV Fixing**
- Corrects nested JSON formatting
- Expands data into proper rows
- Creates timestamped output files
- Runs automatically after fetching

### 📊 **Comprehensive Data**
- All Australian regions
- All data items (unemployment, employment, participation, etc.)
- All demographic breakdowns
- Historical time series data

### 🛡️ **Robust Error Handling**
- Handles API errors gracefully
- Skips unavailable combinations (404s)
- Logs all activities
- Crash recovery via checkpoints

---

## 📂 What Files Will Be Created?

### During Operation:
- `abs_api_config.json` - Your saved API key
- `abs_fetch_checkpoint.json` - Progress tracking
- `abs_labour_force_data_YYYYMMDD_HHMMSS.csv` - Raw API output
- `fetch_abs_data.log` - Detailed operation logs

### Final Output:
- `abs_labour_force_data_FIXED_YYYYMMDD_HHMMSS.csv` - **Your clean data!** ✨

---

## 🖥️ Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **macOS** | ✅ Fully Supported | Native tkinter included |
| **Windows** | ✅ Fully Supported | See `WINDOWS_SETUP.md` |
| **Linux** | ✅ Fully Supported | May need `python3-tk` package |

---

## 🎯 Common Use Cases

### **Monthly Data Updates**
1. Open GUI once per month
2. Click "▶️ Fetch Data"
3. Wait ~20-40 minutes (depending on new data)
4. Use the fixed CSV file in your analysis

### **Initial Data Collection**
1. First run fetches ALL historical data
2. Takes 2-3 hours (thousands of combinations)
3. Subsequent runs only fetch new months
4. Takes minutes instead of hours

### **Transfer to Another Computer**
1. Copy the 4 core files + documentation
2. Install `requests` package
3. Run GUI and enter API key
4. Done!

---

## 📊 Sample Output

The fixed CSV file contains columns like:
- `region` - Australia, New South Wales, Victoria, etc.
- `data_item` - UNEMPLOYMENT_RATE, EMPLOYMENT_TO_POPULATION_RATIO, etc.
- `age` - 15_AND_OVER, 15_TO_19, 20_TO_24, etc.
- `sex` - MALES, FEMALES, PERSONS
- `adjustment_type` - ORIGINAL, SEASONALLY_ADJUSTED, TREND
- `period` - 2020-01, 2020-02, etc.
- `value` - The actual statistic

Perfect for:
- Time series analysis
- Regional comparisons
- Demographic breakdowns
- Economic research
- Policy analysis

---

## 🛠️ Troubleshooting

### GUI won't open?
```bash
# macOS/Linux
pip3 install --upgrade tk

# Windows
# Python installer includes tkinter by default
```

### "No API key provided" error?
1. Get key from https://developer.vic.gov.au
2. Enter in GUI's API Key field
3. Click "💾 Save"

### Rate limit errors?
- Built-in rate limiting handles this automatically
- Just wait, it will resume

### Need more help?
- Check `QUICK_REFERENCE.md` for common solutions
- Read `ABS_DATA_ONBOARDING.md` for troubleshooting section
- Check the log file: `fetch_abs_data.log`

---

## 📖 Getting Help

**Quick answers:** `QUICK_REFERENCE.md`  
**Setup help:** `TRANSFER_GUIDE.md`  
**GUI help:** Click the "❓ Help" button in the GUI  
**Complete docs:** `ABS_DATA_ONBOARDING.md`  

---

## 🔗 Links

- **ABS API Portal:** https://developer.vic.gov.au
- **Get API Key:** https://developer.vic.gov.au (free registration)
- **ABS Website:** https://www.abs.gov.au

---

## 📝 Requirements

- **Python:** 3.7 or higher
- **Dependencies:** `requests` (that's it!)
- **API Key:** Free from Victorian Government API Portal
- **Internet:** Required for API access

---

## 🎓 For Developers

### Project Architecture

```
┌─────────────────┐
│  abs_data_gui   │  ← Main GUI application
└────────┬────────┘
         │
         ├──▶ fetch_abs_data_auto.py  ← Data fetching engine
         │         │
         │         ├─ Checkpoint system
         │         ├─ Rate limiter
         │         └─ API client
         │
         └──▶ fix_abs_csv.py          ← CSV formatter
```

### Key Components

1. **GUI (`abs_data_gui.py`)**
   - tkinter-based interface
   - Threading for background tasks
   - Real-time subprocess output parsing
   - Status dashboard with live updates

2. **Fetcher (`fetch_abs_data_auto.py`)**
   - Iterates through all data combinations
   - Checkpoint system for crash recovery
   - Sliding window rate limiter (25 req/min)
   - Incremental fetching (only new data)

3. **Fixer (`fix_abs_csv.py`)**
   - Parses nested JSON in CSV fields
   - Expands data into proper rows
   - Handles field size limits
   - Creates timestamped output

### Extending the System

- **Add new regions:** Modify `REGIONS` list in `fetch_abs_data_auto.py`
- **Add new data items:** Modify `DATA_ITEMS` list
- **Change rate limit:** Adjust `RateLimiter` initialization
- **Modify checkpoint frequency:** Change `CHECKPOINT_INTERVAL`

---

## 📦 Transferring to Another Computer

### Essential Files (Must Copy):
```
✅ abs_data_gui.py
✅ fetch_abs_data_auto.py
✅ fix_abs_csv.py
✅ requirements.txt
```

### Recommended Documentation:
```
✅ QUICK_REFERENCE.md
✅ TRANSFER_GUIDE.md
```

**Total size:** ~100 KB (tiny!)

**See `TRANSFER_GUIDE.md` for complete instructions.**

---

## 🏆 Best Practices

1. **Run monthly** for fresh data updates
2. **Keep checkpoint files** for resume capability
3. **Don't delete raw CSV** until you verify the fixed version
4. **Back up your API key** in a secure location
5. **Check logs** if something seems wrong

---

## 🤝 Contributing

This is a research tool. Feel free to:
- Report issues
- Suggest improvements
- Fork and customize
- Share with colleagues

---

## 📄 License

This project is for research and educational purposes.

**Data Source:** Australian Bureau of Statistics (ABS)  
**API Provider:** Victorian Government API Portal  

---

## 🎉 Quick Success Path

```
1. pip3 install requests          (30 seconds)
2. python3 abs_data_gui.py        (2 seconds)
3. Enter API key + Save           (30 seconds)
4. Click "Fetch Data"             (2 seconds)
5. Wait for completion            (20-180 min depending on data)
6. Analyze your CSV file!         (Your research begins! 📊)
```

---

## 💬 Support

**Questions?** Read the docs in this order:
1. `QUICK_REFERENCE.md` (fastest)
2. `GUI_GUIDE.md` (if using GUI)
3. `ABS_DATA_ONBOARDING.md` (comprehensive)

**Still stuck?** Check:
- The `fetch_abs_data.log` file
- The "❓ Help" button in the GUI
- The troubleshooting sections in the docs

---

## ⭐ Star This Repo

If this tool helps your research, give it a star! ⭐

---

**Built with ❤️ for policy researchers and data analysts**

*Last updated: November 2025*

