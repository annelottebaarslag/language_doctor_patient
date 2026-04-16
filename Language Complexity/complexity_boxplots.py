import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Level_Analysis\IBIS_colon_Level_Scores.csv')
df[df.duplicated(['filename', 'label'], keep=False)]


df_doc = df[df["label"]=="Doctor"].reset_index(drop=True).drop(df.columns[0], axis=1)
df_patient = df[df["label"]=="Patient"].reset_index(drop=True).drop(df.columns[0], axis=1)

df_doc = df_doc.rename(columns={"avg_sent_length": "Average words per sentence", "avg_syllables": "Average syllables per word", "fres": "Flesch Reading Ease Score", "pass_pct": "Percentage of passive sentences", "ttr": "Type-Token Ratio"})
df_patient = df_patient.rename(columns={"avg_sent_length": "Average words per sentence", "avg_syllables": "Average syllables per word", "fres": "Flesch Reading Ease Score", "pass_pct": "Percentage of passive sentences", "ttr": "Type-Token Ratio"})

metrics = ['Average words per sentence', 'Average syllables per word', 'Flesch Reading Ease Score', 'Percentage of passive sentences', 'Type-Token Ratio']

fig, axes = plt.subplots(1, len(metrics), figsize=(18, 4), sharey=False)

for ax, metric in zip(axes, metrics):
    ax.boxplot([df_doc[metric], df_patient[metric]],labels=['Doctor', 'Patient'])
    ax.set_title(metric)

plt.tight_layout()
plt.show()