# Financial Sentiment Pipeline

A robust data engineering pipeline that collects, processes, and analyzes sentiment from financial news and social media to inform market insights.

## Project Overview

This pipeline ingests data from multiple sources (e.g., news APIs, social feeds), processes it through natural language and sentiment analysis, and stores the results for visualization and further modeling. Designed for flexibility, it can run on a schedule or on-demand to monitor market sentiment trends in near real-time.

## Architecture

- Ingestion Layer: Pulls articles and social posts from APIs (e.g., NewsAPI, Twitter/X)
- Preprocessing: Cleans and tokenizes text, removes stopwords, and standardizes input
- Sentiment Analysis: Uses TextBlob, VADER, or transformer-based models to extract sentiment scores
- Storage: Saves cleaned and scored data in a structured database (SQLite by default, compatible with PostgreSQL)
- Reporting/Export: Outputs .csv files and dashboards summarizing trends by ticker, keyword, or topic

## Key Features

- Real-time or batched sentiment tracking  
- Modular preprocessing pipeline  
- Clean exports ready for modeling or visualization  
- Easily extendable to use custom NLP models  
- Designed with scalability in mind (Airflow or Cron-ready)

## Technologies Used

| Layer            | Tools / Libraries                  |
|------------------|------------------------------------|
| Language         | Python 3.10+                       |
| NLP / Sentiment  | nltk, TextBlob, VADER, transformers |
| Storage          | SQLite, PostgreSQL                 |
| Scheduling       | Airflow, schedule, or cron         |
| Visualization    | matplotlib, seaborn, Plotly        |

## Directory Structure

Financial_Sentiment_Pipeline/
├── data/
│   └── raw/
│   └── processed/
├── database/
│   └── sentiment.db
├── src/
│   ├── ingest.py
│   ├── clean.py
│   ├── sentiment.py
│   ├── store.py
│   ├── analyze.py
│   └── config.py
├── notebooks/
│   └── exploratory_analysis.ipynb
├── README.md
└── requirements.txt

## Getting Started

1. Install dependecies
   - pip isntall -r requirements.txt

2. Run full pipeline
   - python src/ingest.py
   - python src/clean.py
   - python src/sentiment.py
   - python src/store.py

3. Explore sentiment database
   - Query manually via SQLite/Postgres
   - Visualize trends using the included notebook
  
## Future Enhancements

  - Integrate live Twitter/X stream ingestion

  - Use transformer-based models (e.g., FinBERT)

  - Schedule daily runs via Airflow

  - Add economic/market outcome correlation models

Author
AntSarCode
Data Engineering and Analytics Portfolio
GitHub: https://github.com/AntSarCode
