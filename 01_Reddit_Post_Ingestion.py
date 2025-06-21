import praw
import pandas as pd
from datetime import datetime
import sqlite3
#Sentiment Scoring
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# -- AUTHENTICATION --
reddit = praw.Reddit(
    client_id="7LObKBHdXPJngdU2mcNhxg",
    client_secret="1PjklYZ-OmoiiTbauPFE1o3Yyntmwg",
    user_agent="MarketSentimentScript by /u/TaxsisStargas"
)

# -- CONFIGURATION --
subreddits = ["stocks", "investing", "cryptocurrency"]
tickers = ["AAPL", "GOOG", "BTC", "SPY"]
limit = 500  # posts per subreddit

# -- COLLECTION --
records = []
for sub in subreddits:
    for post in reddit.subreddit(sub).new(limit=limit):
        title = post.title
        created = datetime.fromtimestamp(post.created_utc)
        for ticker in tickers:
            if ticker in title:
                records.append({
                    "datetime": created,
                    "subreddit": sub,
                    "ticker": ticker,
                    "title": title,
                    "body": post.selftext,
                    "num_comments": post.num_comments,
                    "upvotes": post.score,
                    "url": post.url
                })
# -- DF CONVERSION --
df_reddit = pd.DataFrame(records)
df_reddit["title_clean"] = df_reddit["title"].str.replace(
    r"[^\w\s]", "", regex=True).str.lower()

# -- SENTIMENT SCORING --
analyzer = SentimentIntensityAnalyzer()
# Apply to cleaned text
df_reddit["sentiment"] = (df_reddit["title"].apply(
    lambda x: analyzer.polarity_scores(x)["compound"]))

#Scoring Defined
def label_sentiment(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"
df_reddit["sentiment_label"] = df_reddit["sentiment"].apply(label_sentiment)


print(df_reddit.head())

#SQLite Bridge
conn = sqlite3.connect('market_data.db')

#DataFrame --> SQL
df_reddit.to_sql(
    'reddit_posts', conn, if_exists='replace', index=False)


conn.close()
