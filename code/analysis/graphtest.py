import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("harris/all_sentences.csv")


# Sort by line_id (or sentence_id if preferred)
df = df.sort_values(by=["sentence_id"])

# Compute percentage progress of speech
df["progress"] = df.groupby("speech_id").cumcount() / df.groupby("speech_id")["sentence_id"].transform("count")


# Set Seaborn style
sns.set_theme(style="whitegrid")

# Plot layered speeches
plt.figure(figsize=(10, 6))
"""sns.lineplot(x="progress", y="valence", hue="speech_id", data=df, alpha=0.5, legend=False)

# Labels and title
plt.xlabel("Speech Progress (%)")
plt.ylabel("Valence Score")
plt.title("Valence Progression Across Speeches")
plt.xticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
"""

# Scatter plot for valence progression
"""sns.scatterplot(x="progress", y="dominance", hue="speech_id", data=df, alpha=0.2, legend=False)

# Add trend lines for each speech
for speech_id in df["speech_id"].unique():
    speech_df = df[df["speech_id"] == speech_id]
    sns.regplot(x="progress", y="dominance", data=speech_df, scatter=False, ci=None, line_kws={"linewidth": 1.5, "alpha": 0.75})

# Labels and title
plt.xlabel("Speech Progress (%)")
plt.ylabel("Dominance Score")
plt.title("Dominance Progression Across Speeches (with Trend Lines)")
plt.xticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])

plt.show()"""

window_size = 50  

for speech_id in df["speech_id"].unique():
    speech_df = df[df["speech_id"] == speech_id].sort_values("progress")

    # Compute rolling mean and standard deviation
    speech_df["rolling_mean"] = speech_df["valence"].rolling(window=window_size, min_periods=1).mean()
    speech_df["rolling_std"] = speech_df["valence"].rolling(window=window_size, min_periods=1).std()

    # Define upper and lower bounds for shading
    speech_df["upper"] = speech_df["rolling_mean"] + speech_df["rolling_std"]
    speech_df["lower"] = speech_df["rolling_mean"] - speech_df["rolling_std"]

    # Plot rolling mean
    sns.lineplot(x="progress", y="rolling_mean", data=speech_df, label=f"Speech {speech_id}")

    # Plot shaded range
    plt.fill_between(speech_df["progress"], speech_df["lower"], speech_df["upper"], alpha=0.2)

# Labels and title
plt.xlabel("Speech Progress (%)")
plt.ylabel("Valence Score")
plt.title("Valence Progression with Rolling Range Across Speeches")
plt.xticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
plt.legend(title="Speech ID", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.show()