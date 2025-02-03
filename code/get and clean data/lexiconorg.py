import os
import csv
import re

def format_transcript(text):
    """Extracts only Kamala Harris' speech sections, keeping timestamps and text formatting."""
    lines = text.split("\n")
    output = []

    current_speaker = None
    current_timestamp = None
    current_text = []

    for line in lines:
        line = line.strip()

        # Detect speaker lines
        speaker_match = re.match(r"Speaker: ([\w\s]+) \((\d{2}:\d{2}:\d{2}|\d{2}:\d{2})\):", line)
        if speaker_match:
            speaker_name = speaker_match.group(1).strip()

            # Skip all speakers except Kamala Harris
            if speaker_name.lower() != "kamala harris":
                current_speaker, current_timestamp, current_text = None, None, []  # Reset tracking
                continue  # Ignore this speaker's section

            # Save previous speaker's text before switching
            if current_speaker and current_text:
                output.append([current_speaker, current_timestamp, " ".join(current_text)])
                current_text = []  # Reset text storage

            # Set new speaker and timestamp
            current_speaker = speaker_name
            current_timestamp = speaker_match.group(2).strip()
            continue  # Move to next line

        # Detect text lines
        if line.startswith("Text:"):
            # Skip if not Kamala Harris (i.e., current_speaker is None)
            if not current_speaker:
                continue

            # Extract inline timestamp if present
            inline_timestamp_match = re.search(r'\((\d{2}:\d{2}:\d{2}|\d{2}:\d{2})\)', line)
            inline_timestamp = inline_timestamp_match.group(1) if inline_timestamp_match else None

            # Remove "Text:" prefix and inline timestamp
            cleaned_text = re.sub(r"Text:\s*|\(\d{2}:\d{2}(:\d{2})?\)", "", line).strip()

            if cleaned_text:
                # If there's an inline timestamp, treat it as a new speaker entry
                if inline_timestamp:
                    output.append([current_speaker, inline_timestamp, cleaned_text])
                else:
                    current_text.append(cleaned_text)  # Otherwise, append to the current speaker's text

    # Add last speaker's remaining text
    if current_speaker and current_text:
        output.append([current_speaker, current_timestamp, " ".join(current_text)])

    return output

# Directories
input_dir = "../../harris/harrisspeeches/mult_speak_txtfile"
output_dir = "../../harris/harrisspeeches/kamala_only_csv"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each file
for filename in os.listdir(input_dir):
    if not filename.endswith(".txt"):  # Ensure it's a text file
        continue

    input_path = os.path.join(input_dir, filename)

    # Read file contents
    with open(input_path, 'r', encoding="utf-8") as file:
        text = file.read()

    # Generate CSV filename
    namefile = filename[:-4]
    output_path = os.path.join(output_dir, f"{namefile}_KAMALA.csv")

    # Write to CSV
    with open(output_path, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Speaker', 'Timestamp', 'Text'])  # Header
        writer.writerows(format_transcript(text))

    print(f"✅ File {namefile}_KAMALA.csv created successfully (only Kamala Harris' speech).")
