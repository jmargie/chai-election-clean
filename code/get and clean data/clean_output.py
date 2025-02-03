"""
- Combine all lines into one file (across speeches, but storing both speech id and line id)


import pandas as pd
import os

#go through bert emotion scores, NRC emotion scores, and VAD scores
#make one file with all lines

#VAD: S%%%_vad.csv
#EMO: S%%%_anger.csv
#BERT: S%%%_emotion.tsv

all_lines = pd.DataFrame()
for filename in os.listdir("harris/VAD scores/lemma per line"):
    speech_id = filename[:-8]
    with open(f"harris/VAD scores/lemma per line/{filename}") as f:
        df3 = pd.read_csv(f)
    with open(f"harris/NRC emotion scores/lemma per line/{speech_id}_anger.csv") as f:
        df2 = pd.read_csv(f)
    with open(f"harris/bert emotion scores/per line/{speech_id}_emotion.tsv") as f:
        df1 = pd.read_csv(f, sep='\t')
    df_merged = pd.merge(df1[['speech_id', 'line_id', 'anger_score']], 
                      df2[['speech_id', 'line_id', 'anger']], 
                      on=['speech_id', 'line_id'], how='outer')
    df_final = pd.merge(df_merged, 
                     df3[['speech_id', 'line_id', 'valence', 'arousal', 'dominance']], 
                     on=['speech_id', 'line_id'], how='outer')
    all_lines = pd.concat([all_lines, df_final], ignore_index=False)

all_lines.to_csv("harris/all_lines", index = False)
    

- Combine all sentences into one file (across speeches, but storing both speech id and sentence id)
"""
import pandas as pd
import os

#go through bert emotion scores, NRC emotion scores, and VAD scores
#make one file with all lines

#lines
#VAD: S%%%_vad.csv
#EMO: S%%%_anger.csv
#BERT: S%%%_emotion.tsv

#sentences
#VAD: S%%%_SPLIT_vad.csv
#VAD: S%%%_SPLIT_anger.csv
#BERT: S%%%__emotion.tsv

all_lines = pd.DataFrame()
for filename in os.listdir("harris/VAD scores/lemma per sentence"):
    speech_id = filename[:-14]
    with open(f"harris/VAD scores/lemma per sentence/{filename}") as f:
        df3 = pd.read_csv(f)
    with open(f"harris/NRC emotion scores/lemma per sentence/{speech_id}_SPLIT_anger.csv") as f:
        df2 = pd.read_csv(f)
    with open(f"harris/bert emotion scores/per sent/{speech_id}__emotion.tsv") as f:
        df1 = pd.read_csv(f, sep='\t')
    df_merged = pd.merge(df1[['speech_id', 'line_id', 'sentence_id','anger_score']], 
                      df2[['speech_id', 'line_id',  'sentence_id','anger']], 
                      on=['speech_id', 'line_id', 'sentence_id'], how='outer')
    df_final = pd.merge(df_merged, 
                     df3[['speech_id', 'line_id', 'sentence_id', 'valence', 'arousal', 'dominance']], 
                     on=['speech_id', 'line_id', 'sentence_id'], how='outer')
    all_lines = pd.concat([all_lines, df_final], ignore_index=True)

all_lines.to_csv("harris/all_sentences", index = False)
    