### extremityrun.py
### julia margie
### run previously trained and finetuned roBERTa on Anthropic's persuasion

import argparse
import os
import pandas as pd

from transformers import pipeline
from datasets import load_dataset

anger_model = "/Users/juliamargie/Desktop/chai election clean/emotion models/angerextremitymodel"
"""joy_model = "./joyextremitymodel"
sadness_model = "./sadnessextremitymodel"
fear_model = "./fearextremitymodel"
"""

tokenizer2 = "/Users/juliamargie/Desktop/chai election clean/emotion models/tokenizer for emotion models"

angerclassifier = pipeline("sentiment-analysis", model = anger_model, tokenizer = tokenizer2)
"""joyclassifier = pipeline("sentiment-analysis", model = joy_model, tokenizer = tokenizer2)
sadnessclassifier = pipeline("sentiment-analysis", model = sadness_model, tokenizer = tokenizer2)
fearclassifier = pipeline("sentiment-analysis", model = fear_model, tokenizer = tokenizer2)"""


# Function to add columns to the dataset with classification and score
def classify_anger(examples):
    results = angerclassifier(examples['line_text'])
    examples['anger_score'] = [result['score'] for result in results]
    return examples

def process_csv(input_csv, output_csv):
    try:
        data = load_dataset("csv", data_files=input_csv)
        
        if len(data['train']) == 0:  # Check for empty dataset
            print(f"Warning: The file '{input_csv}' is empty. Skipping...")
            return

        print(data['train'].column_names)
        if 'line_text' not in data['train'].column_names:
            print(f"Error: The input CSV '{input_csv}' must have a 'line_text' column.")
            return
        

        sentiment_dataset = data.map(classify_anger, batched=True)
        #sentiment_dataset = sentiment_dataset.map(classify_joy, batched=True)
        #sentiment_dataset = sentiment_dataset.map(classify_sadness, batched=True)
        #sentiment_dataset = sentiment_dataset.map(classify_fear, batched=True)
        toprint = sentiment_dataset['train'].to_pandas()  # Convert the 'train' split to a pandas DataFrame


        toprint.to_csv(output_csv, sep='\t', index=False)
        #sentiment_dataset.to_csv(output_csv, index=False)

        print(f"Processed {input_csv} saved to: {output_csv}")
        
    except Exception as e:
        print(f"Error processing file '{input_csv}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Process CSV files for Kamala Harris speeches and compute VAD scores.")
    parser.add_argument('--directory', required=True, help="Directory containing speech files.")
    parser.add_argument('--input', required=True, help="Location of speech files.")
    parser.add_argument('--output', required=True, help="Location of resulting file.")
    parser.add_argument('--type', required=True, help="File extension of speech files (e.g., '.csv').")
    
    args = parser.parse_args()
    
    files = os.listdir(args.directory)
    for filename in files:
        if filename.endswith(args.type):
            namefile = filename[:-len(args.type)]
            process_csv(
                os.path.join(args.input, filename),
                os.path.join(args.output, f"{namefile}_emotion.tsv")
            )

if __name__ == "__main__":
    main()


"""python3 code/extremityrun.py --directory "harris/harrisspeeches/line_split_ID" \
                           --input "harris/harrisspeeches/line_split_ID" \
                           --output "harris/bert emotion scores/per line" \
                           --type ".csv"
                           """



"""dsfull = load_dataset("Anthropic/persuasion", split='train')"""
#partial = Dataset.from_dict(dsfull[0:10])
"""sentiment_dataset = dsfull.map(classify_anger, batched=True)
sentiment_dataset = sentiment_dataset.map(classify_joy, batched=True)
sentiment_dataset = sentiment_dataset.map(classify_sadness, batched=True)
sentiment_dataset = sentiment_dataset.map(classify_fear, batched=True)"""


