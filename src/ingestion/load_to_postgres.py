"""
Load synthetic CSVs into Postgres — Customer Journey Funnel Tracker (Project 3)

Why this script exists (not just `psql \\copy`):
  The dimension tables use auto-incrementing SERIAL surrogate keys
  (customer_key, channel_key, product_key), but the generated CSVs only
  contain natural/business keys (customer_id, channel_name, product_id).
  Fact tables need the surrogate keys as foreign keys. So we load
  dimensions first, read back the surrogate keys Postgres assigned,
  build natural-key -> surrogate-key lookup maps in Python, then use
  those maps to populate the fact tables correctly.

Order of operations (matters — fact tables have FK constraints):
  1. dim_date      (no FK dependencies)
  2. dim_customer  (no FK dependencies)
  3. dim_channel   (no FK dependencies)
  4. dim_product   (no FK dependencies)
  5. fact_web_events   (needs date_key, customer_key, channel_key)
  6. fact_lead_events  (needs date_key, customer_key, channel_key)
  7. fact_orders       (needs date_key, customer_key, channel_key, product_key)

Connection settings: edit DB_CONFIG below, or set environment variables
PGHOST / PGPORT / PGDATABASE / PGUSER / PGPASSWORD before running.

Run:
    python -m src.ingestion.load_to_postgres
"""

import csv
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "customer_journey_funnel",
    "user": "postgres",
    "password": "Sql123"
}


def read_csv(filename):
    path = DATA_DIR / filename
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_dim_date(cur, rows):
    records = [
        (
            int(r["date_key"]), r["full_date"], int(r["day_of_week"]), r["day_name"],
            int(r["week_of_year"]), int(r["month"]), r["month_name"], int(r["quarter"]),
            int(r["year"]), r["is_weekend"].lower() == "true",
        )
        for r in rows
    ]
    execute_values(
        cur,
        """INSERT INTO dim_date
           (date_key, full_date, day_of_week, day_name, week_of_year,
            month, month_name, quarter, year, is_weekend)
           VALUES %s ON CONFLICT (date_key) DO NOTHING""",
        records,
    )
    print(f"  dim_date: inserted {len(records)} rows")


def load_dim_customer(cur, rows):
    records = [
        (r["customer_id"], r["customer_name"], r["segment"], r["region"], r["signup_date"])
        for r in rows
    ]
    execute_values(
        cur,
        """INSERT INTO dim_customer (customer_id, customer_name, segment, region, signup_date)
           VALUES %s ON CONFLICT (customer_id) DO NOTHING""",
        records,
    )
    print(f"  dim_customer: inserted {len(records)} rows")

    cur.execute("SELECT customer_id, customer_key FROM dim_customer")
    return {row[0]: row[1] for row in cur.fetchall()}


def load_dim_channel(cur, rows):
    records = [(r["channel_name"], r["channel_category"]) for r in rows]
    execute_values(
        cur,
        """INSERT INTO dim_channel (channel_name, channel_category)
           VALUES %s ON CONFLICT (channel_name) DO NOTHING""",
        records,
    )
    print(f"  dim_channel: inserted {len(records)} rows")

    cur.execute("SELECT channel_name, channel_key FROM dim_channel")
    return {row[0]: row[1] for row in cur.fetchall()}


def load_dim_product(cur, rows):
    records = [
        (r["product_id"], r["product_name"], r["category"], float(r["unit_price"]))
        for r in rows
    ]
    execute_values(
        cur,
        """INSERT INTO dim_product (product_id, product_name, category, unit_price)
           VALUES %s ON CONFLICT (product_id) DO NOTHING""",
        records,
    )
    print(f"  dim_product: inserted {len(records)} rows")

    cur.execute("SELECT product_id, product_key FROM dim_product")
    return {row[0]: row[1] for row in cur.fetchall()}


def load_fact_web_events(cur, rows, customer_map, channel_map):
    records = [
        (
            int(r["date_key"]),
            customer_map[r["customer_id"]],
            channel_map[r["channel_name"]],
            r["event_timestamp"],
            r["session_id"],
            r["page_url"],
        )
        for r in rows
    ]
    execute_values(
        cur,
        """INSERT INTO fact_web_events
           (date_key, customer_key, channel_key, event_timestamp, session_id, page_url)
           VALUES %s""",
        records,
    )
    print(f"  fact_web_events: inserted {len(records)} rows")


def load_fact_lead_events(cur, rows, customer_map, channel_map):
    records = [
        (
            r["lead_id"],
            int(r["date_key"]),
            customer_map[r["customer_id"]],
            channel_map[r["channel_name"]],
            r["event_timestamp"],
            r["lead_status"],
        )
        for r in rows
    ]
    execute_values(
        cur,
        """INSERT INTO fact_lead_events
           (lead_id, date_key, customer_key, channel_key, event_timestamp, lead_status)
           VALUES %s""",
        records,
    )
    print(f"  fact_lead_events: inserted {len(records)} rows")


def load_fact_orders(cur, rows, customer_map, channel_map, product_map):
    records = [
        (
            r["order_id"],
            int(r["date_key"]),
            customer_map[r["customer_id"]],
            channel_map[r["channel_name"]],
            product_map[r["product_id"]],
            int(r["quantity"]),
            float(r["unit_price"]),
            float(r["revenue"]),
            r["order_status"],
        )
        for r in rows
    ]
    execute_values(
        cur,
        """INSERT INTO fact_orders
           (order_id, date_key, customer_key, channel_key, product_key,
            quantity, unit_price, revenue, order_status)
           VALUES %s""",
        records,
    )
    print(f"  fact_orders: inserted {len(records)} rows")


def main():
    print(f"Connecting to Postgres database '{DB_CONFIG['dbname']}' at {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        print("\nLoading dimension tables...")
        load_dim_date(cur, read_csv("dim_date.csv"))
        customer_map = load_dim_customer(cur, read_csv("dim_customer.csv"))
        channel_map = load_dim_channel(cur, read_csv("dim_channel.csv"))
        product_map = load_dim_product(cur, read_csv("dim_product.csv"))

        print("\nLoading fact tables...")
        load_fact_web_events(cur, read_csv("fact_web_events.csv"), customer_map, channel_map)
        load_fact_lead_events(cur, read_csv("fact_lead_events.csv"), customer_map, channel_map)
        load_fact_orders(cur, read_csv("fact_orders.csv"), customer_map, channel_map, product_map)

        conn.commit()
        print("\nAll data loaded successfully and committed.")

    except Exception as e:
        conn.rollback()
        print(f"\nERROR — rolled back all changes. Nothing was partially loaded.\n{e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()