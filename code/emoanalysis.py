import argparse
import os
import pandas as pd

def load_valfile(tsv_path):
    """Loads the valence-arousal-dominance lexicon file."""
    test = pd.read_csv(tsv_path)
    return test.set_index('word')

def get_anger_score(valfile, word):
    """Returns the anger score for a given word from the VAD lexicon."""
    word = word.strip().lower()
    return valfile.loc[word, "anger"] if word in valfile.index else 0

def clean_up(line):
    """Cleans up a line by splitting it into lowercase words."""
    return [word.strip().lower() for word in line.split()]

def calculate_anger(valfile, words):
    """Calculates the average anger score for a list of words."""
    scores = [get_anger_score(valfile, word) for word in words if get_anger_score(valfile, word) is not None]
    return sum(scores) / len(scores) if scores else 0

def avg_line_anger(valfile, line):
    """Calculates the anger score for a single line of text."""
    words = clean_up(line)
    return calculate_anger(valfile, words)

def avg_speech_anger(valfile, speech):
    """Calculates the anger score for an entire speech (concatenated text)."""
    words = clean_up(speech)
    return calculate_anger(valfile, words)

def process_csv(valfile_path, input_csv, output_csv):
    """Processes a single CSV file, calculating anger scores and preserving speech & line IDs."""
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

        # Calculate total speech anger score
        speech_text = data['sentence_text'].str.cat(sep=" ")
        total_anger_score = avg_speech_anger(valfile, speech_text)

        # Append speech-level anger score to a summary file
        with open("harris/harrisspeeches/anger_totalscore.csv", "a") as file:
            file.write(f"{input_csv}, {total_anger_score}, 0\n")
        
        print(f"Processed {input_csv}: Total Anger Score = {total_anger_score}")

        # Compute anger scores per line
        data['anger'] = data['sentence_text'].apply(lambda line: avg_line_anger(valfile, line))
        
        # Save processed data
        data.to_csv(output_csv, index=False)

        print(f"Saved processed file: {output_csv}")
        
    except Exception as e:
        print(f"Error processing {input_csv}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Process CSV files to compute anger scores for Kamala Harris speeches.")
    parser.add_argument('--input', required=True, help="Location of speech files.")
    parser.add_argument('--output', required=True, help="Location of resulting file.")
    parser.add_argument('--type', required=True, help="File extension of speech files (e.g., '.csv').")
    
    args = parser.parse_args()
    valfile = "NRC-Emotion-Lexicon/emotionlex_justenglish.csv"
    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)

    # Process each file in the input directory
    for filename in os.listdir(args.input):
        if filename.endswith(args.type):
            input_path = os.path.join(args.input, filename)
            output_path = os.path.join(args.output, f"{filename[:-len(args.type)]}_anger.csv")
            process_csv(valfile, input_path, output_path)

if __name__ == "__main__":
    main()


"""python3 code/emoanalysis.py --input "harris/harrisspeeches/sentence_split_ID" \
                                   --output "harris/NRC emotion scores/per sentence" \
                                   --type ".csv"
                                   """