import os
import pandas as pd
import re

def split_text_into_sentences(text):
    # Split text into sentences based on punctuation
    return re.split(r'(?<=[.!?]) +', text.strip())

def process_csv(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # List to hold new rows
    new_rows = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        #speaker = row['Speaker']
        text = row['line']

        # Split text into sentences
        sentences = split_text_into_sentences(text)

        # Create new rows for each sentence
        for sentence in sentences:
            new_rows.append({
                #'speaker': speaker,
                'line': sentence.strip()
            })

    # Create a new DataFrame from the new rows
    new_df = pd.DataFrame(new_rows)

    # Save the new DataFrame to a CSV file
    new_df.to_csv(output_csv, index=False, mode ='w')



# Example input text
for filename in os.listdir("/Users/juliamargie/Desktop/work/election chai/harris/harrisspeeches/csvsplit/"):
    print(filename)
    namefile = filename[:-9]
    input_csv_file = f"harris/harrisspeeches/only harris's words/{filename}" # Change this to your input CSV file path
    output_csv_file = f'harris/harrisspeeches/sentence split/{namefile}_SPLIT.csv'  # Change this to your desired output CSV file path
    process_csv(input_csv_file, output_csv_file)
    print(f"file {namefile} created")

""" filename = "Apr 9, 2024-VPHarris_SOLO.csv"
file = "harris/harrisspeeches/csvsplit/Apr 9, 2024-VPHarris_SOLO.csv"
output = f"harris/harrisspeeches/csvsplit/sentences/{filename}"

process_csv(file, output) """
