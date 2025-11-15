# ABS Labour Force Data Collection System
## Technical Onboarding Documentation

**Version:** 1.0  
**Last Updated:** November 2025  
**Author:** Yeo Yong Kiat, Ministry of Health

---

## Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Running the Scripts](#running-the-scripts)
6. [Understanding the Output](#understanding-the-output)
7. [File Structure](#file-structure)
8. [API Configuration](#api-configuration)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Overview

### Purpose
This system automates the collection of Australian Bureau of Statistics (ABS) labour force data from the Victorian Government API. It fetches comprehensive employment, unemployment, and population statistics across all Australian regions.

### What Data Is Collected
- **9 Regions**: Australia, NSW, VIC, QLD, SA, WA, TAS, NT, ACT
- **20 Data Items**: Civilian population, employment rates, unemployment rates, labour force statistics, etc.
- **3 Sex Categories**: Males, Females, Persons
- **3 Adjustment Types**: Original, Seasonally Adjusted, Trend
- **Time Coverage**: Monthly data from February 1978 to present (~573 observations per combination)

### Total Data Volume
- **API Calls**: 1,620 requests per run
- **Expected Records**: ~930,000 rows per complete fetch
- **Time Required**: ~65 minutes per run
- **Rate Limit**: 25 requests per minute

---

## System Requirements

### Software
- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Operating System**: macOS, Linux, or Windows

### Python Packages

**Required (install via pip):**
- `requests` >= 2.31.0 - For API calls

**Built-in (no installation needed):**
- `tkinter` - For GUI (usually included with Python)
- `threading`, `subprocess`, `json`, `csv`, `datetime` - All built-in

**Note:** Only 1 package needs installation! Everything else is included with Python.

### Network
- Stable internet connection
- Access to `wovg-community.gateway.prod.api.vic.gov.au`

### API Access
- Valid API key from https://developer.vic.gov.au
- Active subscription to the ABS Labour Force API

---

## Quick Start

### For Existing Users (Transferring to New Computer)

**Files to Copy (4 essential files):**
```
✅ abs_data_gui.py              (GUI interface)
✅ fetch_abs_data_auto.py       (Data fetcher)
✅ fix_abs_csv.py               (CSV formatter)
✅ requirements.txt             (Dependencies)
```

**Optional (to preserve settings):**
```
⭐ abs_api_config.json          (Saved API key)
⭐ abs_fetch_checkpoint.json    (Progress checkpoint)
```

**Setup on New Computer:**

**Step 1:** Install dependencies (only 1 package!)
```bash
cd /path/to/project/folder
pip install -r requirements.txt

# This installs:
# - requests (for API calls)
# That's it! Everything else is built-in with Python.
```

**Step 2:** Launch the GUI
```bash
python3 abs_data_gui.py
```

**Step 3:** Configure API Key
- If you copied `abs_api_config.json`: API key auto-loads ✅
- If not: Enter your API key in the GUI field and click "💾 Save"

**Step 4:** Fetch Data
- Click "▶️ Fetch Data"
- First run: ~65 minutes
- Monthly runs: ~10 seconds (if data < 30 days old)

**Complete Transfer Guide:** See `TRANSFER_GUIDE.md` for detailed instructions

---

## Detailed Setup

### Step 1: Obtain API Credentials

1. **Register** at https://developer.vic.gov.au
2. **Navigate** to "My API Requests" → "Create API Access Request"
3. **Select** the "ABS Labour Force API"
4. **Submit** the request (usually approved instantly)
5. **Copy** your API Key from the portal (looks like: `80d6e850-77a6-417c-b6c2-b5e113c403d7`)

**Note**: You only need the API Key, not the Secret Key for this API.

### Step 2: Configure the Scripts

Open `fetch_abs_data_auto.py` in a text editor and update line 20:

```python
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
```

Replace `"YOUR_API_KEY_HERE"` with your actual API key from Step 1.

### Step 3: Install Dependencies

**Only 1 package to install!**

```bash
# Install required package
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt

# Or install directly
pip install requests>=2.31.0
```

**What gets installed:**
- `requests` (>= 2.31.0) - For making API calls to ABS

**What's already included:**
- Everything else is built-in with Python! 🎉

**For GUI users (if needed):**

If you get an error launching the GUI, install tkinter:

```bash
# macOS
brew install python-tk

# Linux (Ubuntu/Debian)
sudo apt-get install python3-tk

# Windows - included with Python installer
```

### Step 4: Verify Setup

Run a quick test to ensure everything works:

```bash
python3 fetch_abs_data_auto.py --help
# If no errors, you're good to go!
```

---

## Running the Scripts

### Method 1: GUI Application (Easiest!) 🎨

Beautiful graphical interface with buttons, progress bar, and real-time logs.

```bash
python3 abs_data_gui.py
# or
./launch_gui.sh
```

**Features:**
- ✅ One-click data fetching
- ✅ Live progress bar
- ✅ Real-time checkpoint notifications
- ✅ Status dashboard (last run, freshness, records)
- ✅ Color-coded logs
- ✅ Stop/resume capabilities

**See:** `GUI_GUIDE.md` for complete interface documentation

### Method 2: Automated Pipeline (Command Line) ⭐

This runs the complete process: fetch data → fix CSV → cleanup old files

```bash
./run_abs_fetch.sh
```

**What happens:**
1. Loads checkpoint (if exists) to skip recent data
2. Fetches needed data combinations (smart skipping)
3. Saves checkpoint every 50 requests (crash-proof!)
4. Saves raw data to `abs_labour_force_ALL_DATA_[timestamp].csv`
5. Automatically runs CSV formatter
6. Creates `abs_labour_force_ALL_DATA_[timestamp]_FIXED.csv`
7. Cleans up old files (keeps most recent 5)
8. Logs everything to `abs_data_fetch.log`

**Expected duration:**
- **First run:** ~65 minutes (fetches all 1,620 combinations)
- **Monthly re-run (< 30 days):** ~10 seconds (skips everything!)
- **After crash:** Resumes from last checkpoint automatically

### Method 3: Manual Step-by-Step

Run each script separately:

```bash
# Step 1: Fetch data
python3 fetch_abs_data_auto.py

# Step 2: Fix CSV format (run after fetch completes)
python3 fix_abs_csv.py
```

### Method 4: Interactive Mode (Original Script)

For testing or customized runs:

```bash
python3 fetch_abs_data.py
# This will ask for confirmation before running
```

---

## Understanding the Output

### File Naming Convention

```
abs_labour_force_ALL_DATA_20251114_164354.csv
                         ^^^^^^^^_^^^^^^
                         YYYYMMDD_HHMMSS (timestamp)

abs_labour_force_ALL_DATA_20251114_164354_FIXED.csv
                                          ^^^^^^
                                          Formatted version
```

### CSV Structure

The FIXED CSV contains these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `region_description` | Australian region | "Victoria" |
| `data_item_description` | What is measured | "Unemployment rate (%)" |
| `sex_description` | Gender category | "Males" |
| `age_description` | Age group | "15 and over" |
| `adjustment_type_description` | Data adjustment | "Seasonally Adjusted" |
| `observation_month` | Month of observation | "2025-10" |
| `observation_value` | Actual value | "5.2" |

### Sample Data Row

```csv
region_description,data_item_description,sex_description,age_description,adjustment_type_description,observation_month,observation_value
Victoria,Unemployment rate (%),Males,15 and over,Seasonally Adjusted,2025-10,5.2
```

### Log Files

**`abs_data_fetch.log`**
- Contains detailed execution logs
- Shows progress, errors, and completion status
- Useful for debugging

**Format:**
```
2025-11-14 16:43:54,123 - INFO - Starting Automated ABS Data Fetch
2025-11-14 16:43:54,124 - INFO - Total API calls to make: 1620
2025-11-14 16:43:54,125 - INFO - Estimated time: 64.8 minutes
...
2025-11-14 17:48:32,456 - INFO - ✅ Data saved to: abs_labour_force_ALL_DATA_20251114_164354.csv
```

---

## File Structure

### Essential Files (Required)

```
fetch_abs_data_auto.py     # Main data collection script
fix_abs_csv.py             # CSV formatting utility
requirements.txt           # Python dependencies
run_abs_fetch.sh          # Pipeline automation script
abs_data_gui.py           # GUI application (recommended!)
launch_gui.sh             # GUI launcher script
```

### Output Files (Generated)

```
abs_labour_force_ALL_DATA_*.csv        # Raw API response data
abs_labour_force_ALL_DATA_*_FIXED.csv  # Formatted, analysis-ready data
abs_data_fetch.log                     # Execution logs
abs_fetch_checkpoint.json              # Progress checkpoint (for crash recovery)
```

### Documentation Files (Reference)

```
ABS_DATA_ONBOARDING.md        # This file (comprehensive onboarding)
GUI_GUIDE.md                  # GUI application user guide
README_ABS_API.md             # API-specific documentation
CHECKPOINT_GUIDE.md           # Checkpoint system detailed guide
CHECKPOINT_QUICKSTART.md      # Checkpoint quick reference
AUTOMATION_GUIDE.md           # Scheduling/automation guide
QUICK_AUTOMATION_START.md     # Quick automation setup
API_TROUBLESHOOTING.md        # Common issues and solutions
SUBSCRIPTION_CHECKLIST.md     # API subscription verification
```

### Optional Files (Not Required for Basic Use)

```
fetch_abs_data.py             # Interactive version (asks for confirmation)
test_fetch_abs.py             # Quick test script (3 API calls)
com.abs.datafetch.plist       # macOS launchd configuration
```

---

## API Configuration

### Endpoint Details

**Base URL:** `https://wovg-community.gateway.prod.api.vic.gov.au/abs/v1.0`  
**Endpoint:** `/labour-force-statistics`  
**Method:** GET  
**Authentication:** API Key (simple header-based)

### Request Format

```http
GET /abs/v1.0/labour-force-statistics?region=VICTORIA&data_item=UNEMPLOYMENT_RATE&age=15_AND_OVER&sex=MALES&adjustment_type=SEASONALLY_ADJUSTED
Host: wovg-community.gateway.prod.api.vic.gov.au
Accept: application/json
apikey: YOUR_API_KEY_HERE
```

### Response Format

```json
{
  "_meta": {
    "response_time": "0.494 seconds",
    "total_records": 573,
    "page": 1,
    "limit": 1000
  },
  "labour_force_statistics": [
    {
      "region_description": "Victoria",
      "data_item_description": "Unemployment rate (%)",
      "sex_description": "Males",
      "age_description": "15 and over",
      "adjustment_type_description": "Seasonally Adjusted",
      "observation_month": "2025-10",
      "observation_value": "5.2"
    }
  ]
}
```

### Rate Limiting

- **Limit:** 25 requests per minute
- **Handling:** Automatic rate limiting built into scripts
- **Total time:** ~1,620 requests ÷ 25 req/min = ~65 minutes

---

## Troubleshooting

### Common Issues

#### 1. "401 Authentication Error"

**Problem:** Invalid or inactive API key

**Solution:**
- Verify your API key is correct in `fetch_abs_data_auto.py`
- Check your subscription status at https://developer.vic.gov.au
- Wait 5-10 minutes after creating new API key (propagation time)

#### 2. "ModuleNotFoundError: No module named 'requests'"

**Problem:** Python dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
# or
pip install requests
```

#### 3. "Permission denied: ./run_abs_fetch.sh"

**Problem:** Script not executable

**Solution:**
```bash
chmod +x run_abs_fetch.sh
```

#### 4. CSV Shows Malformed Data

**Problem:** CSV not properly formatted

**Solution:**
```bash
python3 fix_abs_csv.py
```

This automatically finds and fixes the most recent CSV file.

#### 5. Script Runs But No Data Collected

**Problem:** Network issues or API unavailable

**Solution:**
- Check internet connection
- Check `abs_data_fetch.log` for specific errors
- Verify API is operational: https://developer.vic.gov.au
- Try a test run: `python3 test_fetch_abs.py`

#### 6. "Rate limit exceeded" Errors

**Problem:** Making requests too quickly

**Solution:**
- Scripts have built-in rate limiting - this shouldn't happen
- If it does, wait 1 minute and restart
- Check if multiple instances are running

#### 7. Script Not Resuming After Crash

**Problem:** Script starts from beginning after interruption

**Solution:**
```bash
# Check if checkpoint exists
ls -lh abs_fetch_checkpoint.json

# If missing or empty, crash happened before first save (< 50 requests)
# Just run again from start

# If exists, script should auto-resume
./run_abs_fetch.sh
```

#### 8. Always Skipping Everything

**Problem:** Script says "Combinations to fetch: 0" but you need new data

**Solution:**
```bash
# Force full refresh by deleting checkpoint
rm abs_fetch_checkpoint.json
./run_abs_fetch.sh
```

### Getting Help

1. **Check logs:**
   ```bash
   tail -100 abs_data_fetch.log
   ```

2. **Test API connectivity:**
   ```bash
   python3 test_fetch_abs.py
   ```

3. **Verify API key:**
   - Log into https://developer.vic.gov.au
   - Check "My API Requests" → ABS Labour Force API
   - Ensure status is "Active"

4. **Contact support:**
   - API issues: apisupport@dgs.vic.gov.au
   - ABS data questions: abs@abs.gov.au

---

## Best Practices

### When to Run

**Frequency:** Monthly
- ABS releases new data monthly
- Recommended: Run on the 15th of each month (ensures new data is available)
- **With checkpoints:** If you run within 30 days, script completes in seconds!

**Time of Day:** Off-peak hours
- 2-4 AM if automated (first run only - takes 65 minutes)
- Anytime if running manually
- Monthly re-runs take ~10 seconds (checkpoint magic!)

### Data Management

**Storage:**
- Each complete fetch creates ~100-200 MB of data
- Keep last 3-6 months of historical data
- Archive older data to long-term storage

**Backup:**
- Backup FIXED CSV files (these are analysis-ready)
- Raw CSV files can be regenerated by re-running fix script
- Optionally backup `abs_fetch_checkpoint.json` (preserves progress)

**Version Control:**
- Don't commit API keys to git
- Don't commit large CSV files to git
- Don't commit checkpoint files to git (they're machine-specific)
- Do commit the scripts and documentation

### Performance

**Optimization:**
- Don't increase rate limit (will get blocked)
- Run during off-peak hours if possible
- Use wired internet connection for stability

**Monitoring:**
- Check `abs_data_fetch.log` after each run
- Verify record counts match expectations
- Monitor for failed requests

### Security

**API Key:**
- Never commit API keys to version control
- Don't share API keys publicly
- Rotate keys if compromised
- Use environment variables for production deployments

**Data:**
- ABS data is public, no confidentiality concerns
- Follow Creative Commons Attribution 4.0 license
- Attribute ABS when publishing derived works

---

## Appendix: Parameter Reference

### Available Regions
```
AUSTRALIA
NEW_SOUTH_WALES
VICTORIA
QUEENSLAND
SOUTH_AUSTRALIA
WESTERN_AUSTRALIA
TASMANIA
NORTHERN_TERRITORY
AUSTRALIAN_CAPITAL_TERRITORY
```

### Available Data Items
```
CIVILIAN_POPULATION
EMPLOYED_FULL_TIME
EMPLOYED_PART_TIME
EMPLOYED_PERSONS
EMPLOYMENT_TO_POPULATION_RATIO
UNEMPLOYED_LOOKING_FOR_FULL_TIME_WORK
UNEMPLOYED_LOOKING_FOR_PART_TIME_WORK
UNEMPLOYED_PERSONS
LABOUR_FORCE_FULL_TIME
LABOUR_FORCE_PART_TIME
LABOUR_FORCE
NOT_IN_THE_LABOUR_FORCE
UNEMPLOYMENT_RATE_LOOKING_FOR_PART_TIME_WORK
UNEMPLOYMENT_RATE_LOOKING_FOR_FULL_TIME_WORK
UNEMPLOYMENT_RATE
UNEMPLOYMENT_TO_POPULATION_RATIO_LOOKING_FOR_FULL_TIME_WORK
PARTICIPATION_RATE
EMPLOYED_PERSONS_MONTHLY_HOURS_WORKED_IN_ALL_JOBS
FULL_TIME_EMPLOYED_MONTHLY_HOURS_WORKED_IN_ALL_JOBS
PART_TIME_EMPLOYED_MONTHLY_HOURS_WORKED_IN_ALL_JOBS
```

### Available Sex Values
```
MALES
FEMALES
PERSONS
```

### Available Adjustment Types
```
ORIGINAL          # Raw, unadjusted data
SEASONALLY_ADJUSTED  # Adjusted for seasonal patterns
TREND             # Smoothed trend data
```

### Available Age Groups
```
15_AND_OVER       # Currently the only age group available
```

---

## Quick Reference Card

### Essential Commands

```bash
# Run complete data collection
./run_abs_fetch.sh

# Manual fetch
python3 fetch_abs_data_auto.py

# Fix CSV format
python3 fix_abs_csv.py

# Quick test (3 API calls)
python3 test_fetch_abs.py

# View logs
tail -f abs_data_fetch.log

# List output files
ls -lht abs_labour_force_ALL_DATA_*_FIXED.csv
```

### Key Files to Transfer

```
✓ fetch_abs_data_auto.py
✓ fix_abs_csv.py
✓ requirements.txt
✓ run_abs_fetch.sh
```

### Important URLs

- **Developer Portal:** https://developer.vic.gov.au
- **API Docs:** https://developer.vic.gov.au/apis/abs-labour-force
- **ABS Website:** https://www.abs.gov.au
- **Support:** apisupport@dgs.vic.gov.au

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2025 | Initial documentation |

---

## License & Attribution

This system uses data from the Australian Bureau of Statistics. When using this data:
- Attribute: "Australian Bureau of Statistics, Labour Force Statistics"
- License: Creative Commons Attribution 4.0 International
- More info: https://www.abs.gov.au/about/data-services/help/copyright

---

**End of Documentation**

For questions or issues, contact the Policy Research Team.

