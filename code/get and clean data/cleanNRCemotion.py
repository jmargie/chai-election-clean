import pandas as pd

def load_valfile(tsv_path):
    valfile = pd.read_csv(tsv_path, sep='\t')
    return valfile

f = load_valfile("NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-ForVariousLanguages.txt")

fnew = f[["English Word","anger","anticipation","disgust","fear","joy","negative","positive","sadness","surprise","trust"]]

fnew.to_csv("NRC-Emotion-Lexicon/emotionlex_justenglish")