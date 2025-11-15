import csv
import ast
import sys
import glob
import os

# Increase CSV field size limit
csv.field_size_limit(sys.maxsize)

# Find the most recent abs_labour_force file
files = glob.glob("abs_labour_force*.csv")
files = [f for f in files if not f.endswith("_FIXED.csv")]

if not files:
    print("No ABS labour force CSV files found!")
    print("Please run fetch_abs_data.py first.")
    exit(1)

# Use the most recent file
input_file = max(files, key=os.path.getctime)
output_file = input_file.replace(".csv", "_FIXED.csv")

print(f"Found file: {input_file}")
print(f"Reading {input_file}...")

with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # The data is in the 'labour_force_statistics' column
        data_str = row.get('labour_force_statistics', '')
        
        if not data_str:
            print("No data found in labour_force_statistics column")
            continue
        
        try:
            # Parse the string representation of the list
            data_records = ast.literal_eval(data_str)
            
            print(f"Found {len(data_records)} records")
            
            if len(data_records) == 0:
                print("No records to save!")
                exit(1)
            
            # Get all field names
            fieldnames = list(data_records[0].keys())
            
            print(f"Fields: {', '.join(fieldnames)}")
            print(f"\nWriting to {output_file}...")
            
            # Write to proper CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for record in data_records:
                    writer.writerow(record)
            
            print(f"✅ Success! Saved {len(data_records)} records to {output_file}")
            print(f"\nSample record:")
            first_record = data_records[0]
            for key, value in first_record.items():
                print(f"  {key}: {value}")
            
            print(f"\nDate range: {data_records[0].get('observation_month')} to {data_records[-1].get('observation_month')}")
            
        except Exception as e:
            print(f"Error parsing data: {e}")
            print(f"First 200 chars of data: {data_str[:200]}")

