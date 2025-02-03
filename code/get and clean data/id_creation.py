import os
import pandas as pd
import re
from datetime import datetime

# Ask the user for the input directory
input_dir = input("Enter the path to the directory containing the CSV files: ").strip()

# Validate the directory
if not os.path.isdir(input_dir):
    print("Error: The provided path is not a valid directory.")
    exit(1)

# Set output directory to a subfolder named "processed_output" within the input directory
output_dir = os.path.join(input_dir, "with_IDs")
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# List to store speech metadata
speech_metadata = []

# Process each CSV file in the directory
for idx, filename in enumerate(os.listdir(input_dir)):
    if not filename.endswith("_KAMALA.csv"):
        continue  # Skip files that don't match the pattern
    
    # Extract date and title from filename
    match = re.match(r"(.+)-(.+)_KAMALA\.csv", filename)
    if not match:
        continue
    
    date_str, title = match.groups()
    
    # Convert date to YYYY-MM-DD format
    try:
        date = datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"Skipping file with invalid date format: {filename}")
        continue

    # Assign a speech ID (e.g., S001, S002, ...)
    speech_id = f"S{idx+1:03d}"
    
    # Read CSV
    file_path = os.path.join(input_dir, filename)
    df = pd.read_csv(file_path)
    
    # Process text into line IDs
    df = df.rename(columns={"Text": "line_text"})  # Rename column for clarity
    df = df[["line_text"]].reset_index()
    df.columns = ["line_id", "line_text"]  # Line ID starts from 0
    df["speech_id"] = speech_id  # Add speech ID
    
    # Save processed CSV for this speech
    output_file = os.path.join(output_dir, f"{speech_id}.csv")
    df.to_csv(output_file, index=False)

    # Store metadata for the master CSV
    speech_metadata.append([speech_id, date, title])

# Create and save the master CSV
master_df = pd.DataFrame(speech_metadata, columns=["speech_id", "date", "title"])
master_df.to_csv(os.path.join(output_dir, "all_speeches.csv"), index=False)

print("Processing complete. Output saved in:", output_dir)
