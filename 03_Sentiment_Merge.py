import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#SQLite
conn = sqlite3.connect("market_data.db")

#DataFrame
df_prices = pd.read_sql("SELECT * FROM daily_prices", conn)
df_sentiment = pd.read_sql("SELECT * FROM reddit_posts", conn)

# -- FORMAT COLUMNS --
df_prices.rename(columns={"Ticker": "ticker"}, inplace=True)
df_prices["date"] = pd.to_datetime(df_prices["Date"]).dt.date
df_sentiment["date"] = pd.to_datetime(df_sentiment["datetime"]).dt.date

# -- MAP TICKERS --
ticker_map = {
    "AAPL": "AAPL",
    "GOOG": "GOOG",
    "SPY": "SPY",
    "BTC": "BTC-USD"
}
df_sentiment["ticker"] = df_sentiment["ticker"].map(ticker_map)

# -- SENTIMENT FILTER --
trading_days = df_prices["date"].unique()
df_sentiment = df_sentiment[df_sentiment["date"].isin(trading_days)]

# --- PER DAY TICKER ---
agg_sentiment = df_sentiment.groupby(["date", "ticker"]).agg({
    "sentiment": "mean",
    "sentiment_label": lambda x: x.mode()[0] if not x.mode().empty else "neutral"
}).reset_index()
agg_sentiment.rename(columns={"sentiment": "avg_sentiment", "sentiment_label": "dominant_label"}, inplace=True)

# -- NORMALIZE DATES --
df_prices["date"] = pd.to_datetime(df_prices["date"]).dt.date
agg_sentiment["date"] = pd.to_datetime(agg_sentiment["date"]).dt.date

# -- NORMALIZE TICKER --
df_prices["ticker"] = df_prices["ticker"].str.upper()
agg_sentiment["ticker"] = agg_sentiment["ticker"].str.upper()

#Bug Fix
matches = pd.merge(
    df_prices[["date", "ticker"]],
    agg_sentiment[["date", "ticker"]],
    on=["date", "ticker"],
    how="inner"
)
print("✅ Matching rows after normalization:", len(matches))

# -- MARKET PRICE MERGE --
df_merged = pd.merge(
    df_prices,
    agg_sentiment,
    on=["date", "ticker"],
    how="left"
)

# -- REMOVE DUPLICATION --
if "Date" in df_merged.columns:
    df_merged.drop(columns=["Date"], inplace=True)
df_merged = df_merged.loc[:, ~df_merged.columns.duplicated()]

# -- SAVE TABLE --
df_merged.to_sql("sentiment_prices", conn, if_exists="replace", index=False)
conn.close()

# -- PREVIEW --
preview = df_merged[df_merged["avg_sentiment"].notna()]
print(preview[["date", "ticker", "Close", "avg_sentiment", "dominant_label"]].head(10))

# -- PLOT --
btc = df_merged[df_merged["ticker"] == "BTC-USD"].copy()
btc["date"] = pd.to_datetime(btc["date"])
btc["sentiment_roll"] = btc["avg_sentiment"].rolling(window=3).mean()
plt.plot(btc["date"], btc["avg_sentiment"], label="Avg Sentiment")
plt.plot(btc["date"], btc["Close"] / btc["Close"].max(), label="Normalized Price")
plt.legend()
plt.title("BTC Sentiment vs Price")
plt.show()

# -- EXPORT --
df_merged.to_csv("sentiment_prices_final.csv", index=False)
