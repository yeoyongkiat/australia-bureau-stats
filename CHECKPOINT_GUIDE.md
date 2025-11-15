# Checkpoint System Guide
## ABS Labour Force Data Fetcher

**Last Updated:** November 2025

---

## Overview

The checkpoint system makes the data fetcher **crash-proof** and **efficient** for monthly updates. It automatically saves progress and can resume from interruptions.

---

## 🎯 Key Features

### ✅ 1. Crash Recovery
**Problem:** If script crashes after 60 minutes, you lose everything.  
**Solution:** Progress saved every 50 requests. Resume instantly.

### ✅ 2. Skip Fresh Data
**Problem:** Re-running monthly re-fetches ALL 1,620 combinations unnecessarily.  
**Solution:** Automatically skips data fetched within last 30 days.

### ✅ 3. Incremental Updates
**Problem:** Each run creates duplicate data.  
**Solution:** Merges new records with existing data, avoiding duplicates.

### ✅ 4. Periodic Saves
**Problem:** Long wait to see any results.  
**Solution:** Checkpoint saved every 50 requests (~2 minutes).

---

## 📁 Files Created

### `abs_fetch_checkpoint.json`
The checkpoint file that tracks what's been fetched.

**Structure:**
```json
{
  "completed_combinations": {
    "AUSTRALIA_CIVILIAN_POPULATION_15_AND_OVER_MALES_ORIGINAL": {
      "status": "completed",
      "records": 573,
      "latest_month": "2025-10",
      "fetched_at": "2025-11-15T14:30:45.123456"
    },
    "AUSTRALIA_CIVILIAN_POPULATION_15_AND_OVER_FEMALES_ORIGINAL": {
      "status": "completed",
      "records": 573,
      "latest_month": "2025-10",
      "fetched_at": "2025-11-15T14:31:12.654321"
    }
  },
  "last_run": "2025-11-15T16:45:30.123456",
  "total_records": 930000,
  "last_checkpoint_save": "2025-11-15T16:45:30.123456"
}
```

**Location:** Same directory as your scripts

---

## 🚀 Usage Scenarios

### Scenario 1: First Run (No Checkpoint)

```bash
./run_abs_fetch.sh
```

**What happens:**
1. No checkpoint found → starts fresh
2. Fetches all 1,620 combinations
3. Saves checkpoint every 50 requests
4. Takes ~65 minutes
5. Creates final checkpoint with all combinations

**Output:**
```
Starting Automated ABS Data Fetch (with Checkpoint Support)
No checkpoint file found. Starting fresh.
Total combinations: 1620
Already up-to-date (< 30 days old): 0
Combinations to fetch: 1620
Estimated time: 64.8 minutes
```

---

### Scenario 2: Monthly Re-run (Checkpoint Exists)

```bash
./run_abs_fetch.sh
```

**What happens:**
1. Loads checkpoint from last run (29 days ago)
2. Sees all 1,620 combinations are < 30 days old
3. **Skips ALL API calls** ✨
4. Loads existing data file
5. Completes in **seconds**

**Output:**
```
Starting Automated ABS Data Fetch (with Checkpoint Support)
Loaded checkpoint with 1620 completed combinations
Total combinations: 1620
Already up-to-date (< 30 days old): 1620
Combinations to fetch: 0
Estimated time: 0.0 minutes
```

---

### Scenario 3: Crash Recovery

**Initial Run:**
```bash
./run_abs_fetch.sh
# Crashes at request 847/1620 (minute 34)
^C  # Ctrl+C or crash
```

**Output:**
```
Progress: [850/1620] (52.5%) - Fetched: 847, Failed: 0, Skipped: 0
⚠️  Script interrupted by user (Ctrl+C)
💾 Partial progress has been saved to checkpoint file
🔄 Run the script again to resume from where you left off
```

**Resume:**
```bash
./run_abs_fetch.sh
```

**What happens:**
1. Loads checkpoint with 847 completed combinations
2. Skips those 847 combinations
3. Fetches remaining 773 combinations
4. Takes ~31 minutes (instead of 65)

**Output:**
```
Loaded checkpoint with 847 completed combinations
Total combinations: 1620
Already up-to-date (< 30 days old): 847
Combinations to fetch: 773
Estimated time: 30.9 minutes
Starting with 485,331 existing records
```

---

### Scenario 4: Partial Monthly Update

You run on **Nov 15**, then again on **Nov 25** (10 days later).

**Second run:**
```bash
./run_abs_fetch.sh
```

**What happens:**
1. Loads checkpoint from Nov 15 (10 days ago)
2. All combinations are < 30 days old
3. Skips all fetches
4. Completes instantly

**If you want to force a refresh:**
```bash
rm abs_fetch_checkpoint.json
./run_abs_fetch.sh
```

---

## ⚙️ Configuration

### Adjust Freshness Threshold

Edit `fetch_abs_data_auto.py`, line 77:

```python
DATA_FRESHNESS_DAYS = 30  # Skip combinations fetched within this many days
```

**Examples:**
- `7` - Re-fetch if older than 1 week
- `14` - Re-fetch if older than 2 weeks
- `30` - Re-fetch if older than 1 month (default)
- `0` - Always re-fetch everything (disables smart skipping)

### Adjust Checkpoint Save Frequency

Edit `fetch_abs_data_auto.py`, line 76:

```python
CHECKPOINT_SAVE_INTERVAL = 50  # Save checkpoint every N requests
```

**Examples:**
- `25` - Save every 25 requests (~1 minute) - safer but more I/O
- `50` - Save every 50 requests (~2 minutes) - balanced (default)
- `100` - Save every 100 requests (~4 minutes) - less frequent

---

## 🔧 Management Commands

### View Checkpoint Status

```bash
cat abs_fetch_checkpoint.json | python3 -m json.tool | head -50
```

### Count Completed Combinations

```bash
python3 -c "import json; data=json.load(open('abs_fetch_checkpoint.json')); print(f'Completed: {len(data[\"completed_combinations\"])}')"
```

### Check Last Run Time

```bash
python3 -c "import json; data=json.load(open('abs_fetch_checkpoint.json')); print(f'Last run: {data[\"last_run\"]}')"
```

### Force Full Refresh

```bash
# Delete checkpoint to start fresh
rm abs_fetch_checkpoint.json

# Run script
./run_abs_fetch.sh
```

### Backup Checkpoint

```bash
cp abs_fetch_checkpoint.json abs_fetch_checkpoint_backup_$(date +%Y%m%d).json
```

---

## 📊 Understanding Progress Messages

### During First Run

```
Progress: [50/1620] (3.1%) - Fetched: 50, Failed: 0, Skipped: 0
💾 Checkpoint saved (50 successful, 0 failed)

Progress: [100/1620] (6.2%) - Fetched: 100, Failed: 0, Skipped: 0
💾 Checkpoint saved (100 successful, 0 failed)
```

**Meaning:**
- Processing request 50 of 1620
- Successfully fetched 50 combinations
- No failures
- No skips (fresh run)
- Checkpoint saved

### During Resume

```
Progress: [900/1620] (55.6%) - Fetched: 53, Failed: 0, Skipped: 847

Progress: [950/1620] (58.6%) - Fetched: 103, Failed: 0, Skipped: 847
```

**Meaning:**
- Checked 900 combinations total
- Actually fetched only 53 (the new ones)
- Skipped 847 (from previous run)
- Still processing the remaining

### After Monthly Re-run

```
Total combinations: 1620
Already up-to-date (< 30 days old): 1620
Combinations to fetch: 0
New records added: 0
Total records in dataset: 930,000 (started with 930,000)
Total time: 0.1 minutes
```

**Meaning:**
- All data is recent
- Nothing needed fetching
- No new records (ABS only publishes monthly)
- Completed in 6 seconds

---

## 🐛 Troubleshooting

### Problem: Checkpoint Not Saving

**Symptom:**
```
Error saving checkpoint: [Errno 13] Permission denied
```

**Solution:**
```bash
# Check file permissions
ls -la abs_fetch_checkpoint.json

# Fix permissions
chmod 644 abs_fetch_checkpoint.json

# Or delete and recreate
rm abs_fetch_checkpoint.json
./run_abs_fetch.sh
```

### Problem: Checkpoint Corrupted

**Symptom:**
```
Error loading checkpoint: Expecting value: line 1 column 1 (char 0)
```

**Solution:**
```bash
# Backup corrupted file
mv abs_fetch_checkpoint.json abs_fetch_checkpoint_corrupted.json

# Start fresh
./run_abs_fetch.sh
```

### Problem: Always Skipping Everything

**Symptom:**
```
Combinations to fetch: 0
```
But you know there's new data available.

**Solution:**
```bash
# Force full refresh
rm abs_fetch_checkpoint.json
./run_abs_fetch.sh
```

### Problem: Not Resuming After Crash

**Symptom:**
Script starts from beginning after crash.

**Check:**
```bash
# Verify checkpoint exists and has content
ls -lh abs_fetch_checkpoint.json
cat abs_fetch_checkpoint.json | head
```

**Solution:**
If file is empty or missing, the crash happened before first checkpoint save (< 50 requests). Run again from start.

---

## 🎓 Advanced Usage

### Run with Custom Freshness

Create a custom script:

```bash
#!/bin/bash
# weekly_update.sh

# Modify freshness threshold temporarily
python3 << 'EOF'
import json
with open('fetch_abs_data_auto.py', 'r') as f:
    content = f.read()
content = content.replace('DATA_FRESHNESS_DAYS = 30', 'DATA_FRESHNESS_DAYS = 7')
with open('fetch_abs_data_auto_weekly.py', 'w') as f:
    f.write(content)
EOF

# Run with weekly refresh
python3 fetch_abs_data_auto_weekly.py

# Cleanup
rm fetch_abs_data_auto_weekly.py
```

### Monitor Long Runs

```bash
# Run in background with real-time log viewing
./run_abs_fetch.sh &
tail -f abs_data_fetch.log
```

### Checkpoint Analysis

```python
import json
from datetime import datetime

# Load checkpoint
with open('abs_fetch_checkpoint.json', 'r') as f:
    checkpoint = json.load(f)

# Analyze
completed = checkpoint['completed_combinations']
total_records = sum(c['records'] for c in completed.values() if c.get('status') == 'completed')
failed = [k for k, v in completed.items() if v.get('status') == 'failed']

print(f"Total combinations: {len(completed)}")
print(f"Total records: {total_records}")
print(f"Failed: {len(failed)}")

# Find oldest data
oldest = min(completed.values(), key=lambda x: x.get('fetched_at', ''))
print(f"Oldest fetch: {oldest['fetched_at']}")
```

---

## 📋 Best Practices

### 1. Monthly Routine
```bash
# Just run the script - it handles everything
./run_abs_fetch.sh

# If it's been < 30 days, it completes instantly
# If it's been > 30 days, it fetches everything
```

### 2. Before Important Updates
```bash
# Backup current checkpoint
cp abs_fetch_checkpoint.json abs_fetch_checkpoint_backup.json

# Run update
./run_abs_fetch.sh

# If something goes wrong
mv abs_fetch_checkpoint_backup.json abs_fetch_checkpoint.json
```

### 3. Periodic Full Refresh (Quarterly)
```bash
# Every 3 months, do a full refresh
rm abs_fetch_checkpoint.json
./run_abs_fetch.sh
```

### 4. Monitor Disk Space
```bash
# Check space before run
df -h .

# Checkpoint file is small (~100KB)
# CSV files are large (~200MB per run)
```

---

## 🔄 Migration Guide

### From Old Script (No Checkpoint) to New Script

**Your existing files:**
```
abs_labour_force_ALL_DATA_20251114_164354.csv
abs_labour_force_ALL_DATA_20251114_164354_FIXED.csv
```

**First run with new script:**
```bash
./run_abs_fetch.sh
```

**What happens:**
1. No checkpoint exists → starts fresh
2. But wait! Script finds your existing FIXED CSV
3. Loads those records as the starting point
4. Fetches all 1,620 combinations (to build checkpoint)
5. Merges any new records with existing
6. Creates checkpoint for future runs

**Next run:**
- Uses checkpoint
- Skips everything if < 30 days
- Super fast!

---

## 📝 Summary Table

| Scenario | First Run | Subsequent Run | Time |
|----------|-----------|----------------|------|
| **No checkpoint** | Fetch all 1,620 | Fetch all 1,620 | 65 min each |
| **With checkpoint (< 30 days)** | Fetch all 1,620 | Skip all | 65 min → 10 sec |
| **With checkpoint (> 30 days)** | Fetch all 1,620 | Fetch all 1,620 | 65 min each |
| **Crash at 50%** | Fetch 810/1,620 | Resume: 810/1,620 | 33 min → 33 min |

---

## 🎯 Key Takeaways

1. **Set it and forget it** - Run monthly, it handles the rest
2. **Crash-proof** - Resume from any interruption
3. **Efficient** - Skips unnecessary re-fetching
4. **Flexible** - Adjust freshness threshold as needed
5. **Safe** - Checkpoint saved every 50 requests

---

## 💡 Tips

- **Monthly runs**: Just run it. If data is fresh, completes instantly.
- **After crash**: Just run it again. Resumes automatically.
- **Need fresh data**: Delete checkpoint file to force full refresh.
- **Debugging**: Check `abs_data_fetch.log` for detailed progress.
- **Disk space**: Each run adds ~200MB. Clean old CSVs periodically.

---

**Questions? Issues?**

Check `abs_data_fetch.log` for detailed execution logs.


