import os
import pandas as pd
import re

def split_text_into_sentences(text):
    """Splits text into sentences based on punctuation (., !, ?)."""
    return [s.strip() for s in re.split(r'(?<=[.!?]) +', text.strip()) if s.strip()]

def process_csv(input_csv, output_csv):
    """Processes a CSV by splitting each line's text into sentences while preserving speech and line IDs."""
    # Read the input CSV
    df = pd.read_csv(input_csv)

    # Ensure the required columns exist
    if not {'speech_id', 'line_id', 'line_text'}.issubset(df.columns):
        print(f"Skipping {input_csv}: Missing required columns.")
        return

    # List to hold new rows
    new_rows = []

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        speech_id = row['speech_id']
        line_id = row['line_id']
        text = str(row['line_text']).strip()  # Ensure text is string

        # Split text into sentences
        sentences = split_text_into_sentences(text)

        # Add sentences with a sentence ID
        for sentence_id, sentence in enumerate(sentences):
            new_rows.append({
                'speech_id': speech_id,
                'line_id': line_id,
                'sentence_id': sentence_id,
                'sentence_text': sentence
            })

    # Create a new DataFrame from the processed data
    new_df = pd.DataFrame(new_rows)

    # Save the new DataFrame to a CSV file
    new_df.to_csv(output_csv, index=False)
    print(f"Processed: {output_csv}")

# Directory paths
input_dir = "/Users/juliamargie/Desktop/chai election clean/harris/harrisspeeches/with_IDs/"
output_dir = "/Users/juliamargie/Desktop/chai election clean/harris/harrisspeeches/sentence_split/"

os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Process all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        input_csv_file = os.path.join(input_dir, filename)
        output_csv_file = os.path.join(output_dir, f"{filename[:-4]}_SPLIT.csv")  # Keep filename and add _SPLIT

        process_csv(input_csv_file, output_csv_file)
