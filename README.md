***getting data ready in order:***
- **scrapeurls.py** 
- **scrapetranscripts.py** 
- **cleantranscripts.py** 
    - turns transcript into ordered textfile
    - sends to `mult_speak_txtfile`
- **lexiconorg.py** 
    - turns only textfile (with `cleantranscripts.py` formatting) into usable CSV
    - only kamala harris's lines
    - sends to `harris/harrisspeeches/kamala_only_csv`
- **id_creation.py**
    - remember to do `../..` before the input in terminal
    - sends to `harris/harrisspeeches/line_split_ID`
- **sentencesplit.py** 
    - csv with sentences rather than lines
    - sends to `harris/harrisspeeches/sentence_split_ID`
- **cleanNRCemotion.py** 
    - cleans the NRC emotion data for easier use
- **clean_output.py**
    - turns the many lines / sentences into one file each, combining the pieces


***analyzing data***
- **emoanalysis.py**
    - lexicon analysis of emotion
    - uses `NRC-Emotion-Lexicon/emotionlex_justenglish.csv`
    - sends to `
- **lemmatized_emo.py**
    - lexicon analysis of emotion with lemmatized words
    - uses `NRC-Emotion-Lexicon/emotionlex_justenglish.csv`
- **lemmatized_VAD.py**  
    - vad analysis with lemmatizing  
    - uses `NRC-VAD-Lexicon/NRC-VAD-Lexicon.tsv`  
- **vad_analysis.py**
    - vad analysis no lemmatizing
    - uses `NRC-VAD-Lexicon/NRC-VAD-Lexicon.tsv`
- **extremity_training.py**
    - train bert emotion models
- **extremityrun.py**
    - run bert emotion models

```bash
├── NRC-Emotion-Lexicon
│   ├── OneFilePerEmotion
│   │   ├── anger-NRC-Emotion-Lexicon.txt
│   │   └── ...
│   └── emotionlex_justenglish.csv
├── NRC-VAD-Lexicon
│   ├── NRC-VAD-Lexicon.tsvpdf
│   ├── Paper-VAD-ACL2018.pdf
│   └── README.txt
├── code
│   ├── emoanalysis.py
│   ├── extremity_training.py
│   ├── extremityrun.py
│   ├── fightingwords
│   │   ├── fightin_words_utils.py
│   │   ├── fighting_words_py3.py
│   │   └── fightingwordstext.txt
│   ├── get and clean data
│   │   ├── cleanNRCemotion.py
│   │   ├── clean_output.py
│   │   ├── cleantranscripts.py
│   │   ├── id_creation.py
│   │   ├── lexiconorg.py
│   │   ├── removewhite.py
│   │   ├── scrapetranscripts.py
│   │   ├── scrapeurls.py
│   │   ├── sentence_with_ID.py
│   │   └── sentencesplit.py
│   ├── lemmatized_VAD.py
│   ├── lemmatized_emo.py
│   └── vad_analysis.py
├── emotion models (contact me if you need these)
│   ├── angerextremitymodel
│   ├── data for emotion models
│   ├── fearextremitymodel
│   ├── joyextremitymodel
│   ├── sadnessextremitymodel
│   └── tokenizer for emotion models
│       └── ...
├── harris
│   ├── NRC emotion scores
│   │   ├── anger_totalscore.csv
│   │   ├── lemma per line
│   │   │   ├── S001_anger.csv
│   │   │   └── ...
│   │   ├── lemma per sentence
│   │   │   ├── S001_SPLIT_anger.csv
│   │   │   └── ...
│   │   ├── per line
│   │   │   ├── S001_anger.csv
│   │   │   └── ...
│   │   └── per sentence
│   │       ├── S001_SPLIT_anger.csv
│   │       └── ...
│   ├── VAD scores
│   │   ├── lemma per line
│   │   │   ├── S001_vad.csv
│   │   │   └── ...
│   │   ├── lemma per sentence
│   │   │   ├── S001_SPLIT_vad.csv
│   │   │   └── ...
│   │   ├── per line
│   │   │   ├── S001_vad.csv
│   │   │   └── ...
│   │   ├── per sentence
│   │   │   ├── S001_SPLIT_vad.csv
│   │   │   └── ...
│   │   └── vad_totalscore.csv
│   ├── all_lines.csv
│   ├── all_sentences.csv
│   ├── bert emotion scores
│   │   ├── per line
│   │   │   ├── S001_emotion.tsv
│   │   │   └── ...
│   │   └── per sent
│   │       ├── S001__emotion.tsv
│   │   │   └── ...
│   └── harrisspeeches
│       ├── all_speeches.csv
│       ├── kamala_only_csv
│       │   ├── Apr 9, 2024-VPHarris_KAMALA.csv
│       │   └── ...
│       ├── line_split_ID
│       │   ├── S001.csv
│       │   └── ...
│       ├── mult_speak_txtfile
│       │   ├── Apr 9, 2024-VPHarris.txt
│       │   └── ...
│       └── sentence_split_ID
│           ├── S001_SPLIT.csv
│           └── ...
└── howtorun.txt
```
***to do***
- ✅ assign speech and line and sentence ids 
- ✅ Combine all lines into one file (across speeches, but storing both speech id and line id)
- ✅ Combine all sentences into one file (across speeches, but storing both speech id and sentence id)
- Descriptive analysis of distribution of scores across methods 
    - min,max,mean,median, could also do a histogram or distribution plot
- Plot average scores for VAD and anger emotion over time (across speeches)
- Plot scores over the course of a speech (there’s a lot, so maybe just 2-3?) 
    - we’ll figure out a way to combine them to plot the “narrative arc” next week
- write one script which will run all of the cleaning
- ditto for running analysis more easily (gpt?)
- graph with average per line number in speech (percent of way through speech)
- better data for bert
- plot rolling average range? (percent of way through speech)
- slideshow with graphs for easier viewing
- LEARN PYTHON PLOTTING


