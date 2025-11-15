"""
Automated version of fetch_abs_data.py for scheduled runs.
Enhanced with checkpoint functionality for crash recovery and incremental updates.
"""

import requests
import csv
import json
import time
import logging
import os
import sys
import argparse
from datetime import datetime, timedelta
from collections import deque

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('abs_data_fetch.log'),
        logging.StreamHandler()
    ]
)

# API Configuration
BASE_URL = "https://wovg-community.gateway.prod.api.vic.gov.au/abs/v1.0/labour-force-statistics"

# API Key will be loaded from command-line argument or config file
API_KEY = None

def load_api_key_from_config():
    """Load API key from config file if available."""
    config_file = "abs_api_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('api_key', '')
        except:
            return None
    return None

# Request Parameters - ALL POSSIBLE VALUES
REGIONS = [
    "AUSTRALIA",
    "NEW_SOUTH_WALES",
    "VICTORIA",
    "QUEENSLAND",
    "SOUTH_AUSTRALIA",
    "WESTERN_AUSTRALIA",
    "TASMANIA",
    "NORTHERN_TERRITORY",
    "AUSTRALIAN_CAPITAL_TERRITORY"
]

DATA_ITEMS = [
    "CIVILIAN_POPULATION",
    "EMPLOYED_FULL_TIME",
    "EMPLOYED_PART_TIME",
    "EMPLOYED_PERSONS",
    "EMPLOYMENT_TO_POPULATION_RATIO",
    "UNEMPLOYED_LOOKING_FOR_FULL_TIME_WORK",
    "UNEMPLOYED_LOOKING_FOR_PART_TIME_WORK",
    "UNEMPLOYED_PERSONS",
    "LABOUR_FORCE_FULL_TIME",
    "LABOUR_FORCE_PART_TIME",
    "LABOUR_FORCE",
    "NOT_IN_THE_LABOUR_FORCE",
    "UNEMPLOYMENT_RATE_LOOKING_FOR_PART_TIME_WORK",
    "UNEMPLOYMENT_RATE_LOOKING_FOR_FULL_TIME_WORK",
    "UNEMPLOYMENT_RATE",
    "UNEMPLOYMENT_TO_POPULATION_RATIO_LOOKING_FOR_FULL_TIME_WORK",
    "PARTICIPATION_RATE",
    "EMPLOYED_PERSONS_MONTHLY_HOURS_WORKED_IN_ALL_JOBS",
    "FULL_TIME_EMPLOYED_MONTHLY_HOURS_WORKED_IN_ALL_JOBS",
    "PART_TIME_EMPLOYED_MONTHLY_HOURS_WORKED_IN_ALL_JOBS"
]

AGE_GROUPS = ["15_AND_OVER"]
SEX_VALUES = ["MALES", "FEMALES", "PERSONS"]
ADJUSTMENT_TYPES = ["ORIGINAL", "SEASONALLY_ADJUSTED", "TREND"]

# Rate Limiting Configuration
MAX_REQUESTS_PER_MINUTE = 25
RATE_LIMIT_WINDOW = 60

# Checkpoint Configuration
CHECKPOINT_FILE = "abs_fetch_checkpoint.json"
CHECKPOINT_SAVE_INTERVAL = 50  # Save checkpoint every N requests
DATA_FRESHNESS_DAYS = 30  # Skip combinations fetched within this many days

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_times = deque()
    
    def wait_if_needed(self):
        now = time.time()
        while self.request_times and self.request_times[0] < now - self.time_window:
            self.request_times.popleft()
        
        if len(self.request_times) >= self.max_requests:
            sleep_time = self.time_window - (now - self.request_times[0]) + 0.1
            if sleep_time > 0:
                logging.info(f"Rate limit reached. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                now = time.time()
                while self.request_times and self.request_times[0] < now - self.time_window:
                    self.request_times.popleft()
        
        self.request_times.append(now)

rate_limiter = RateLimiter(MAX_REQUESTS_PER_MINUTE, RATE_LIMIT_WINDOW)

def get_combination_key(region, data_item, age, sex, adjustment_type):
    """Generate unique key for a data combination."""
    return f"{region}_{data_item}_{age}_{sex}_{adjustment_type}"

def load_checkpoint():
    """Load checkpoint from file, or return empty checkpoint structure."""
    if not os.path.exists(CHECKPOINT_FILE):
        logging.info("No checkpoint file found. Starting fresh.")
        return {
            "completed_combinations": {},
            "last_run": None,
            "total_records": 0,
            "last_checkpoint_save": None
        }
    
    try:
        with open(CHECKPOINT_FILE, 'r') as f:
            checkpoint = json.load(f)
        logging.info(f"Loaded checkpoint with {len(checkpoint['completed_combinations'])} completed combinations")
        return checkpoint
    except Exception as e:
        logging.error(f"Error loading checkpoint: {e}. Starting fresh.")
        return {
            "completed_combinations": {},
            "last_run": None,
            "total_records": 0,
            "last_checkpoint_save": None
        }

def save_checkpoint(checkpoint):
    """Save checkpoint to file."""
    try:
        checkpoint["last_checkpoint_save"] = datetime.now().isoformat()
        with open(CHECKPOINT_FILE, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        logging.debug("Checkpoint saved")
    except Exception as e:
        logging.error(f"Error saving checkpoint: {e}")

def is_combination_fresh(checkpoint, combination_key, freshness_days=DATA_FRESHNESS_DAYS):
    """Check if a combination was fetched recently and doesn't need re-fetching."""
    if combination_key not in checkpoint["completed_combinations"]:
        return False
    
    combo_data = checkpoint["completed_combinations"][combination_key]
    status = combo_data.get("status")
    
    # If data is not available in the API, don't retry it
    if status == "not_available":
        return True
    
    # Only check freshness for completed fetches
    if status != "completed":
        return False
    
    fetched_at_str = combo_data.get("fetched_at")
    if not fetched_at_str:
        return False
    
    try:
        fetched_at = datetime.fromisoformat(fetched_at_str)
        age_days = (datetime.now() - fetched_at).days
        return age_days < freshness_days
    except:
        return False

def load_existing_data(checkpoint):
    """Load existing data from previous runs based on checkpoint."""
    all_data = []
    
    # Find the most recent FIXED CSV file
    import glob
    fixed_files = glob.glob("abs_labour_force_ALL_DATA_*_FIXED.csv")
    if not fixed_files:
        logging.info("No existing data files found")
        return all_data
    
    most_recent = max(fixed_files, key=os.path.getctime)
    logging.info(f"Loading existing data from: {most_recent}")
    
    try:
        with open(most_recent, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_data.append(row)
        logging.info(f"Loaded {len(all_data)} existing records")
    except Exception as e:
        logging.error(f"Error loading existing data: {e}")
    
    return all_data

def fetch_data(region, data_item, age, sex, adjustment_type):
    """Fetch data from API."""
    rate_limiter.wait_if_needed()
    
    endpoint = BASE_URL
    params = {
        "region": region,
        "data_item": data_item,
        "age": age,
        "sex": sex,
        "adjustment_type": adjustment_type
    }
    
    headers = {
        "accept": "application/json",
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # 404 means this combination doesn't exist - not an error, just unavailable
            logging.debug(f"Data not available for {region}/{data_item}/{age}/{sex}/{adjustment_type}")
            return "NOT_AVAILABLE"
        else:
            logging.error(f"Error fetching {region}/{data_item}/{age}/{sex}/{adjustment_type}: {e}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {region}/{data_item}/{age}/{sex}/{adjustment_type}: {e}")
        return None

def extract_records_from_response(data):
    """Extract records from API response."""
    records = []
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        if 'labour_force_statistics' in data:
            records = data['labour_force_statistics']
        elif 'data' in data:
            records = data['data']
    return records

def get_latest_observation_month(records):
    """Get the most recent observation month from a list of records."""
    if not records:
        return None
    
    months = [r.get('observation_month') for r in records if 'observation_month' in r]
    if not months:
        return None
    
    return max(months)

def merge_new_records(existing_data, new_records, combination_key):
    """Merge new records with existing data, avoiding duplicates."""
    # Create a set of existing record keys for quick lookup
    existing_keys = set()
    for record in existing_data:
        # Create a unique key for each record
        key = (
            record.get('region_description', ''),
            record.get('data_item_description', ''),
            record.get('age_description', ''),
            record.get('sex_description', ''),
            record.get('adjustment_type_description', ''),
            record.get('observation_month', '')
        )
        existing_keys.add(key)
    
    # Add only new records
    added_count = 0
    for record in new_records:
        key = (
            record.get('region_description', ''),
            record.get('data_item_description', ''),
            record.get('age_description', ''),
            record.get('sex_description', ''),
            record.get('adjustment_type_description', ''),
            record.get('observation_month', '')
        )
        if key not in existing_keys:
            existing_data.append(record)
            existing_keys.add(key)
            added_count += 1
    
    return added_count

def save_to_csv(all_data, filename):
    """Save data to CSV file."""
    if not all_data:
        logging.warning("No data to save")
        return
    
    fieldnames = set()
    for data_entry in all_data:
        if isinstance(data_entry, dict):
            fieldnames.update(data_entry.keys())
    
    fieldnames = sorted(list(fieldnames))
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for data_entry in all_data:
            if isinstance(data_entry, dict):
                writer.writerow(data_entry)
    
    logging.info(f"Data saved to {filename}")

def main():
    logging.info("="*70)
    logging.info("Starting Automated ABS Data Fetch (with Checkpoint Support)")
    logging.info("="*70)
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    
    # Load existing data for incremental updates
    all_data = load_existing_data(checkpoint)
    initial_record_count = len(all_data)
    
    total_combinations = len(REGIONS) * len(DATA_ITEMS) * len(AGE_GROUPS) * len(SEX_VALUES) * len(ADJUSTMENT_TYPES)
    
    # Count how many combinations are already fresh
    fresh_count = 0
    for region in REGIONS:
        for data_item in DATA_ITEMS:
            for age in AGE_GROUPS:
                for sex in SEX_VALUES:
                    for adj_type in ADJUSTMENT_TYPES:
                        combo_key = get_combination_key(region, data_item, age, sex, adj_type)
                        if is_combination_fresh(checkpoint, combo_key):
                            fresh_count += 1
    
    combinations_to_fetch = total_combinations - fresh_count
    estimated_minutes = combinations_to_fetch / MAX_REQUESTS_PER_MINUTE
    
    logging.info(f"Total combinations: {total_combinations}")
    logging.info(f"Already up-to-date (< {DATA_FRESHNESS_DAYS} days old): {fresh_count}")
    logging.info(f"Combinations to fetch: {combinations_to_fetch}")
    logging.info(f"Estimated time: {estimated_minutes:.1f} minutes ({estimated_minutes/60:.1f} hours)")
    logging.info(f"Starting with {initial_record_count} existing records")
    
    successful_requests = 0
    failed_requests = 0
    skipped_requests = 0
    new_records_added = 0
    start_time = time.time()
    current_request = 0
    
    for region in REGIONS:
        for data_item in DATA_ITEMS:
            for age in AGE_GROUPS:
                for sex in SEX_VALUES:
                    for adj_type in ADJUSTMENT_TYPES:
                        current_request += 1
                        combo_key = get_combination_key(region, data_item, age, sex, adj_type)
                        
                        # Check if combination is fresh and can be skipped
                        if is_combination_fresh(checkpoint, combo_key):
                            skipped_requests += 1
                            if current_request % 100 == 0:
                                progress = (current_request / total_combinations) * 100
                                logging.info(f"Progress: [{current_request}/{total_combinations}] ({progress:.1f}%) - Skipped {skipped_requests} fresh")
                            continue
                        
                        # Log progress periodically
                        if (successful_requests + failed_requests) % 50 == 0 and (successful_requests + failed_requests) > 0:
                            progress = (current_request / total_combinations) * 100
                            logging.info(f"Progress: [{current_request}/{total_combinations}] ({progress:.1f}%) - Fetched: {successful_requests}, Failed: {failed_requests}, Skipped: {skipped_requests}")
                        
                        # Fetch data
                        data = fetch_data(region, data_item, age, sex, adj_type)
                        
                        if data == "NOT_AVAILABLE":
                            # This combination doesn't exist in the API (404)
                            checkpoint["completed_combinations"][combo_key] = {
                                "status": "not_available",
                                "fetched_at": datetime.now().isoformat()
                            }
                            skipped_requests += 1
                            logging.info(f"🚫 {region}/{data_item}/{sex}/{adj_type}: Not available in API")
                        elif data:
                            records = extract_records_from_response(data)
                            
                            if records:
                                # Merge with existing data (avoid duplicates)
                                added = merge_new_records(all_data, records, combo_key)
                                new_records_added += added
                                
                                # Update checkpoint
                                latest_month = get_latest_observation_month(records)
                                checkpoint["completed_combinations"][combo_key] = {
                                    "status": "completed",
                                    "records": len(records),
                                    "latest_month": latest_month,
                                    "fetched_at": datetime.now().isoformat()
                                }
                                checkpoint["total_records"] = len(all_data)
                                
                                successful_requests += 1
                                
                                # Log success with details
                                logging.info(f"✅ {region}/{data_item}/{sex}/{adj_type}: {len(records)} records (latest: {latest_month})")
                                
                                # Save checkpoint periodically
                                if (successful_requests + failed_requests) % CHECKPOINT_SAVE_INTERVAL == 0:
                                    save_checkpoint(checkpoint)
                                    logging.info(f"💾 Checkpoint saved ({successful_requests} successful, {failed_requests} failed)")
                            else:
                                logging.warning(f"No records in response for {combo_key}")
                                failed_requests += 1
                        else:
                            failed_requests += 1
                            # Mark as failed in checkpoint but don't block retry
                            checkpoint["completed_combinations"][combo_key] = {
                                "status": "failed",
                                "fetched_at": datetime.now().isoformat()
                            }
    
    elapsed_time = (time.time() - start_time) / 60
    
    # Final checkpoint save
    checkpoint["last_run"] = datetime.now().isoformat()
    save_checkpoint(checkpoint)
    
    # Count not_available combinations
    not_available_count = sum(1 for combo in checkpoint["completed_combinations"].values() 
                             if combo.get("status") == "not_available")
    
    logging.info("="*70)
    logging.info("Fetch Complete!")
    logging.info(f"Successful requests: {successful_requests}")
    logging.info(f"Failed requests: {failed_requests}")
    logging.info(f"Skipped (fresh data): {skipped_requests - not_available_count}")
    logging.info(f"Not available in API (404): {not_available_count}")
    logging.info(f"New records added: {new_records_added}")
    logging.info(f"Total records in dataset: {len(all_data)} (started with {initial_record_count})")
    logging.info(f"Total time: {elapsed_time:.1f} minutes")
    logging.info("="*70)
    
    # Save data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"abs_labour_force_ALL_DATA_{timestamp}.csv"
    
    if all_data:
        save_to_csv(all_data, filename)
        logging.info(f"✅ Raw data saved to: {filename}")
        
        # Auto-run the CSV fixer
        logging.info("Running CSV formatter...")
        try:
            import subprocess
            result = subprocess.run(['python3', 'fix_abs_csv.py'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=300)
            if result.returncode == 0:
                logging.info("✅ CSV formatting completed")
                logging.info(result.stdout)
            else:
                logging.error(f"CSV formatting failed: {result.stderr}")
        except Exception as e:
            logging.error(f"Error running CSV formatter: {e}")
        
        return filename
    else:
        logging.error("❌ No data was fetched")
        return None

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Fetch ABS Labour Force data')
    parser.add_argument('--api-key', type=str, help='API key for ABS API')
    args = parser.parse_args()
    
    # Set API key from command-line or config file
    if args.api_key:
        API_KEY = args.api_key
        logging.info("Using API key from command-line argument")
    else:
        API_KEY = load_api_key_from_config()
        if API_KEY:
            logging.info("Using API key from config file")
        else:
            logging.error("❌ No API key provided!")
            logging.error("Please provide API key via:")
            logging.error("  1. Command line: python3 fetch_abs_data_auto.py --api-key YOUR_KEY")
            logging.error("  2. Save in GUI and it will be loaded automatically")
            sys.exit(1)
    
    try:
        logging.info(f"Checkpoint file: {CHECKPOINT_FILE}")
        logging.info(f"Data freshness threshold: {DATA_FRESHNESS_DAYS} days")
        logging.info(f"Checkpoint save interval: every {CHECKPOINT_SAVE_INTERVAL} requests")
        logging.info("")
        
        result_file = main()
        if result_file:
            logging.info("✅ Script completed successfully")
            logging.info(f"💡 Tip: To force a full refresh, delete {CHECKPOINT_FILE}")
        else:
            logging.error("Script completed with errors")
    except KeyboardInterrupt:
        logging.warning("\n⚠️  Script interrupted by user (Ctrl+C)")
        logging.warning("💾 Partial progress has been saved to checkpoint file")
        logging.warning(f"🔄 Run the script again to resume from where you left off")
    except Exception as e:
        logging.error(f"Script failed with exception: {e}", exc_info=True)
