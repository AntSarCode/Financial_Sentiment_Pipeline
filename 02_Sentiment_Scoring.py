import sqlite3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#SQLite Bridge
conn = sqlite3.connect("market_data.db")

#DataFrame
df = pd.read_sql("SELECT * FROM reddit_posts", conn)

# --- INITIALIZE ANALYZER ---
analyzer = SentimentIntensityAnalyzer()

# --- APPLY SCORING ---
df["sentiment"] = df["title"].apply(lambda x: analyzer.polarity_scores(x)["compound"])

def label_sentiment(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df["sentiment_label"] = df["sentiment"].apply(label_sentiment)

# --- OVERWRITE TABLE ---
df.to_sql("reddit_posts", conn, if_exists="replace", index=False)
print(df[["datetime", "ticker", "sentiment", "sentiment_label"]].head())

conn.close()