import yfinance as yf
import sqlite3

#Tickers and Date Range
tickers = ["AAPL", "SPY", "BTC-USD", "GOOG"]
start_date = "2024-06-01"
end_date = "2025-06-01"

# -- DATA PULL --
df = yf.download(tickers, start=start_date, end=end_date, interval="1d", auto_adjust=True)

#Flatten multi-index columns
df.columns.names = ['Metric', 'Ticker']
df = df.stack(level=1, future_stack=True).reset_index()

#Rename and reorder
df = df.rename(columns={"level_1": "Ticker"})
df = df[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]]

#Derived features
df['Return'] = df.groupby('Ticker')['Close'].pct_change(fill_method=None)

# Preview
print(df.head())

#SQLite Bridge
conn = sqlite3.connect('market_data.db')

#DataFrame --> SQL
df.to_sql('daily prices', conn, if_exists='replace', index=False)

conn.close() 