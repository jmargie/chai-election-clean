import argparse
import csv
import os
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])

import sys
csv.field_size_limit(sys.maxsize)
import nltk
from nltk import sent_tokenize  # Ensure you have NLTK installed

# Download the punkt tokenizer if not already downloaded
nltk.download('punkt')

def load_valfile(tsv_path):
    """Loads the valence-arousal-dominance lexicon file."""
    test = pd.read_csv(tsv_path, usecols=["word", "valence", "arousal", "dominance"], sep = "\t")
    return test.set_index('word')

#def value_in_dict(valfile, word):
    """Returns VAD scores for a given word, or None if not found."""
    word = word.strip().lower()
    return valfile.loc[word] if word in valfile.index else None

def value_in_dict(valfile, word):
    """Returns VAD scores for a given word, or None if not found."""
    word = word.strip().lower()
    doc = nlp(word)  # Process the word with spaCy
    if len(doc) == 0:
        return None
    token = doc[0]  # Get the first token (assuming a single word input)
    if token.text in valfile.index:
        return valfile.loc[token.text]
    elif token.lemma_ in valfile.index:
        return valfile.loc[token.lemma_]
    else:
        return None
    
def clean_up(line):
    """Cleans up text by splitting it into lowercase words."""
    return [word.strip().lower() for word in line.split()]

def calculate_scores(valfile, words):
    """Calculates average valence, arousal, and dominance scores for a list of words."""
    scores = [score for word in words if (score := value_in_dict(valfile, word)) is not None]
    
    if not scores:
        return None, None, None
    
    df = pd.DataFrame(scores)
    return df['valence'].mean(), df['arousal'].mean(), df['dominance'].mean()    

def avg_line(valfile, line):
    """Computes average VAD scores for a single line of text."""
    words = clean_up(line)
    return calculate_scores(valfile, words)

def avg_speech(valfile, speech):
    """Computes average VAD scores for an entire speech."""
    words = clean_up(speech)
    return calculate_scores(valfile, words)

def process_csv(valfile_path, input_csv, output_csv):
    """Processes a single CSV file, calculating VAD scores while preserving identifiers."""
    try:
        valfile = load_valfile(valfile_path)
        data = pd.read_csv(input_csv)
        
        # Ensure required columns exist
        required_columns = {'speech_id', 'line_id', 'sentence_id', 'sentence_text'}
        if not required_columns.issubset(data.columns):
            print(f"Skipping {input_csv}: Missing required columns {required_columns - set(data.columns)}")
            return

        if data.empty:
            print(f"Skipping {input_csv}: File is empty.")
            return

        # Calculate total speech VAD scores
        speech_text = data['sentence_text'].str.cat(sep=" ")
        total_score = avg_speech(valfile, speech_text)

        # Append speech-level VAD scores to a summary file
        with open("harris/harrisspeeches/vad_totalscore.csv", "a") as file:
            file.write(f"{input_csv}, {total_score[0]}, {total_score[1]}, {total_score[2]}, 1\n")
        
        print(f"Processed {input_csv}: Total VAD Scores = {total_score}")

        # Compute VAD scores per line while keeping identifiers
        data[['valence', 'arousal', 'dominance']] = data['sentence_text'].apply(
            lambda line: pd.Series(avg_line(valfile, line))
        )
        
        # Reorder columns: speech_id, line_id, sentence_id, sentence_text, valence, arousal, dominance
        output_columns = ['speech_id', 'line_id', 'sentence_id', 'sentence_text',  'valence', 'arousal', 'dominance']
        data = data[output_columns]

        # Save processed data
        data.to_csv(output_csv, index=False)

        print(f"Saved processed file: {output_csv}")
        
    except Exception as e:
        print(f"Error processing {input_csv}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Process CSV files to compute VAD scores for Kamala Harris speeches.")
    parser.add_argument('--input', required=True, help="Location of speech files.")
    parser.add_argument('--output', required=True, help="Location of resulting file.")
    parser.add_argument('--type', required=True, help="File extension of speech files (e.g., '.csv').")
    
    args = parser.parse_args()
    valfile = "NRC-VAD-Lexicon/NRC-VAD-Lexicon.tsv"
    
    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)

    # Process each file in the input directory
    for filename in os.listdir(args.input):
        if filename.endswith(args.type):
            input_path = os.path.join(args.input, filename)
            output_path = os.path.join(args.output, f"{filename[:-len(args.type)]}_vad.csv")
            process_csv(valfile, input_path, output_path)
            

if __name__ == "__main__":
    main()


"""python3 code/lemmatized_VAD.py --input "harris/harrisspeeches/sentence_split_ID" \
                                   --output "harris/VAD scores/lemma per sentence" \
                                   --type ".csv"
                                   """