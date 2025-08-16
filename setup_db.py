#!/usr/bin/env python3
"""
Setup SQLite database 'food.db' and load CSVs.

Expected CSVs in the current directory:
- providers_data.csv
- receivers_data.csv
- food_listings_data.csv
- claims_data.csv
"""

import os
import sqlite3
import pandas as pd

DB_PATH = "food.db"

def create_schema(conn: sqlite3.Connection):
    cur = conn.cursor()
    # Enable FK
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS providers (
        provider_id    INTEGER PRIMARY KEY,
        name           TEXT NOT NULL,
        type           TEXT,
        address        TEXT,
        city           TEXT,
        contact        TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS receivers (
        receiver_id INTEGER PRIMARY KEY,
        name        TEXT NOT NULL,
        type        TEXT,
        city        TEXT,
        contact     TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS food_listings (
        food_id       INTEGER PRIMARY KEY,
        food_name     TEXT NOT NULL,
        quantity      INTEGER,
        expiry_date   TEXT,
        provider_id   INTEGER,
        provider_type TEXT,
        location      TEXT,
        food_type     TEXT,
        meal_type     TEXT,
        FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        claim_id   INTEGER PRIMARY KEY,
        food_id    INTEGER,
        receiver_id INTEGER,
        status     TEXT,
        timestamp  TEXT,
        FOREIGN KEY (food_id) REFERENCES food_listings(food_id),
        FOREIGN KEY (receiver_id) REFERENCES receivers(receiver_id)
    );
    """)
    conn.commit()

def load_csv_to_table(conn: sqlite3.Connection, csv_path: str, table_name: str):
    if not os.path.exists(csv_path):
        print(f"[WARN] CSV not found: {csv_path}. Skipping.")
        return
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]

    # Basic cleanup: strip strings, unify city casing
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    if "city" in df.columns:
        df["city"] = df["city"].str.title()

    # Write
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"[OK] Loaded {len(df)} rows into {table_name}")

def add_indexes(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_providers_city ON providers(city);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_receivers_city ON receivers(city);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_food_provider ON food_listings(provider_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_food_location ON food_listings(location);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_claims_food ON claims(food_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_claims_receiver ON claims(receiver_id);")
    conn.commit()

def main():
    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)

    load_csv_to_table(conn, "providers_data.csv", "providers")
    load_csv_to_table(conn, "receivers_data.csv", "receivers")
    load_csv_to_table(conn, "food_listings_data.csv", "food_listings")
    load_csv_to_table(conn, "claims_data.csv", "claims")

    add_indexes(conn)
    conn.close()
    print("[DONE] Database ready at food.db")

if __name__ == "__main__":
    main()
