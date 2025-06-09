"""
ingest.py

Module: Data Ingestion
Author: Corey Leath

Loads historical market data from Snowflake and live tick data from Kafka,
then writes raw data to Parquet files for downstream processing.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from kafka import KafkaConsumer

def ingest_snowflake():
    """Ingest historical OHLCV data from Snowflake."""
    sf_url = os.getenv("SNOWFLAKE_URL")
    engine = create_engine(sf_url)
    query = "SELECT timestamp, open, high, low, close, volume FROM market_data.spy"
    df = pd.read_sql(query, engine)
    os.makedirs("data/raw", exist_ok=True)
    df.to_parquet("data/raw/spy.parquet", index=False)
    print(f"[Snowflake] Ingested {len(df)} rows.")

def ingest_kafka():
    """Ingest live tick data from Kafka and append to CSV."""
    consumer = KafkaConsumer(
        "market-ticks",
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        auto_offset_reset="latest",
        value_deserializer=lambda m: pd.read_json(m, lines=True)
    )
    os.makedirs("data/raw", exist_ok=True)
    for message in consumer:
        df = message.value
        df.to_parquet("data/raw/tick.parquet", index=False, append=True)
        print(f"[Kafka] Ingested {len(df)} tick rows.")
        break  # remove break for continuous ingestion

def main():
    ingest_snowflake()
    ingest_kafka()

if __name__ == "__main__":
    main()

git add src/ingestion/ingest.py
git commit -m "Add data ingestion module (Snowflake & Kafka)"
git push
