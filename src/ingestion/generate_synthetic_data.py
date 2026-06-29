"""
Synthetic data generator — Customer Journey Funnel Tracker (Project 3)

Generates realistic, internally-consistent CSV files for all 4 dimension
tables and 3 fact tables defined in src/sql/01_create_schema.sql.

Design notes:
- 50 customers, ~2 years of history (2024-07-01 to 2026-06-28)
- Each customer can generate MULTIPLE web visits over time, with a
  realistic drop-off funnel: not every visit becomes a lead, not every
  lead becomes an opportunity, not every opportunity becomes an order.
- Deliberate patterns are baked in on purpose, so WoW/YoY metrics and
  the funnel dashboard have real signal to show:
    * Seasonal bump in Nov/Dec (holiday shopping)
    * "Paid Search" and "Email" outperform "Referral" and "Social"
      in conversion rate
    * A mild year-over-year growth trend (Year 2 busier than Year 1)
    * A deliberate dip in one specific month of Year 2, for the
      "anomaly flag" stretch goal

Output: CSV files written to backend/data/raw/

Run:
    python -m src.ingestion.generate_synthetic_data
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_CUSTOMERS = 50
START_DATE = date(2024, 7, 1)
END_DATE = date(2026, 6, 28)
OUTPUT_DIR = Path(__file__).resolve().parents[2] /"data" / "raw"

CHANNELS = [
    {"name": "Paid Search", "category": "Paid",    "visit_weight": 25, "lead_conv": 0.35, "opp_conv": 0.45, "order_conv": 0.55},
    {"name": "Email",       "category": "Direct",  "visit_weight": 15, "lead_conv": 0.40, "opp_conv": 0.50, "order_conv": 0.60},
    {"name": "Organic",     "category": "Organic", "visit_weight": 30, "lead_conv": 0.20, "opp_conv": 0.35, "order_conv": 0.45},
    {"name": "Referral",    "category": "Organic", "visit_weight": 15, "lead_conv": 0.22, "opp_conv": 0.30, "order_conv": 0.40},
    {"name": "Social",      "category": "Paid",    "visit_weight": 15, "lead_conv": 0.15, "opp_conv": 0.25, "order_conv": 0.35},
]

PRODUCT_CATALOG = [
    {"name": "Wireless Mouse",        "category": "Accessories", "price": 24.99},
    {"name": "Mechanical Keyboard",   "category": "Accessories", "price": 89.99},
    {"name": "USB-C Hub",             "category": "Accessories", "price": 39.99},
    {"name": "27in Monitor",          "category": "Displays",    "price": 249.99},
    {"name": "Laptop Stand",          "category": "Accessories", "price": 34.99},
    {"name": "Noise Cancelling Headphones", "category": "Audio", "price": 179.99},
    {"name": "Webcam HD",             "category": "Accessories", "price": 59.99},
    {"name": "Desk Lamp LED",         "category": "Office",      "price": 29.99},
    {"name": "Ergonomic Chair",       "category": "Office",      "price": 329.99},
    {"name": "Standing Desk",         "category": "Office",      "price": 449.99},
]

SEGMENTS = ["SMB", "Enterprise", "Consumer"]
REGIONS = ["North America", "EMEA", "APAC", "LATAM"]

ANOMALY_DIP_MONTH = (2026, 3)
ANOMALY_DIP_FACTOR = 0.35


def daterange(start: date, end: date):
    days = (end - start).days
    for i in range(days + 1):
        yield start + timedelta(days=i)


def seasonal_activity_multiplier(d: date) -> float:
    multiplier = 1.0
    if d.month in (11, 12):
        multiplier *= 1.6
    if d >= START_DATE + timedelta(days=365):
        multiplier *= 1.15
    if (d.year, d.month) == ANOMALY_DIP_MONTH:
        multiplier *= ANOMALY_DIP_FACTOR
    if d.weekday() >= 5:
        multiplier *= 0.7
    return multiplier


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        signup_date = fake.date_between(start_date=START_DATE, end_date=END_DATE - timedelta(days=30))
        customers.append({
            "customer_id": f"CUST{i:04d}",
            "customer_name": fake.name(),
            "segment": random.choices(SEGMENTS, weights=[0.35, 0.25, 0.40])[0],
            "region": random.choice(REGIONS),
            "signup_date": signup_date.isoformat(),
        })

    with open(OUTPUT_DIR / "dim_customer.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)

    channels = [{"channel_name": c["name"], "channel_category": c["category"]} for c in CHANNELS]
    with open(OUTPUT_DIR / "dim_channel.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=channels[0].keys())
        writer.writeheader()
        writer.writerows(channels)

    products = []
    for i, p in enumerate(PRODUCT_CATALOG, start=1):
        products.append({
            "product_id": f"PROD{i:03d}",
            "product_name": p["name"],
            "category": p["category"],
            "unit_price": p["price"],
        })

    with open(OUTPUT_DIR / "dim_product.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)

    date_rows = []
    for d in daterange(START_DATE, END_DATE):
        date_rows.append({
            "date_key": int(d.strftime("%Y%m%d")),
            "full_date": d.isoformat(),
            "day_of_week": d.isoweekday(),
            "day_name": d.strftime("%A"),
            "week_of_year": int(d.strftime("%V")),
            "month": d.month,
            "month_name": d.strftime("%B"),
            "quarter": (d.month - 1) // 3 + 1,
            "year": d.year,
            "is_weekend": d.weekday() >= 5,
        })

    with open(OUTPUT_DIR / "dim_date.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=date_rows[0].keys())
        writer.writeheader()
        writer.writerows(date_rows)

    web_events, lead_events, orders = [], [], []
    lead_id_counter = 1
    order_id_counter = 1

    for cust in customers:
        signup = date.fromisoformat(cust["signup_date"])
        active_days = [d for d in daterange(signup, END_DATE)]

        engagement = random.uniform(0.3, 2.5)
        base_visits_per_month = 1.5 * engagement

        for d in active_days:
            multiplier = seasonal_activity_multiplier(d)
            daily_visit_prob = (base_visits_per_month / 30) * multiplier
            if random.random() > daily_visit_prob:
                continue

            channel = random.choices(CHANNELS, weights=[c["visit_weight"] for c in CHANNELS])[0]
            visit_time = datetime.combine(d, datetime.min.time()) + timedelta(
                hours=random.randint(7, 22), minutes=random.randint(0, 59)
            )
            session_id = fake.uuid4()

            web_events.append({
                "date_key": int(d.strftime("%Y%m%d")),
                "customer_id": cust["customer_id"],
                "channel_name": channel["name"],
                "event_timestamp": visit_time.isoformat(sep=" "),
                "session_id": session_id,
                "page_url": random.choice(["/", "/products", "/pricing", "/about", "/checkout"]),
            })

            if random.random() < channel["lead_conv"]:
                lead_id = f"LEAD{lead_id_counter:05d}"
                lead_id_counter += 1
                lead_created_time = visit_time + timedelta(hours=random.randint(1, 48))
                lead_events.append({
                    "lead_id": lead_id,
                    "date_key": int(lead_created_time.date().strftime("%Y%m%d")),
                    "customer_id": cust["customer_id"],
                    "channel_name": channel["name"],
                    "event_timestamp": lead_created_time.isoformat(sep=" "),
                    "lead_status": "created",
                })

                if random.random() < channel["opp_conv"]:
                    qualified_time = lead_created_time + timedelta(hours=random.randint(2, 72))
                    lead_events.append({
                        "lead_id": lead_id,
                        "date_key": int(qualified_time.date().strftime("%Y%m%d")),
                        "customer_id": cust["customer_id"],
                        "channel_name": channel["name"],
                        "event_timestamp": qualified_time.isoformat(sep=" "),
                        "lead_status": "qualified",
                    })

                    opp_time = qualified_time + timedelta(hours=random.randint(2, 96))
                    lead_events.append({
                        "lead_id": lead_id,
                        "date_key": int(opp_time.date().strftime("%Y%m%d")),
                        "customer_id": cust["customer_id"],
                        "channel_name": channel["name"],
                        "event_timestamp": opp_time.isoformat(sep=" "),
                        "lead_status": "opportunity",
                    })

                    if random.random() < channel["order_conv"]:
                        order_time = opp_time + timedelta(hours=random.randint(4, 120))
                        order_id = f"ORD{order_id_counter:05d}"
                        order_id_counter += 1

                        num_lines = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
                        chosen_products = random.sample(products, k=num_lines)
                        order_status = random.choices(
                            ["completed", "cancelled", "refunded"], weights=[0.88, 0.07, 0.05]
                        )[0]

                        for prod in chosen_products:
                            qty = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
                            unit_price = float(prod["unit_price"])
                            orders.append({
                                "order_id": order_id,
                                "date_key": int(order_time.date().strftime("%Y%m%d")),
                                "customer_id": cust["customer_id"],
                                "channel_name": channel["name"],
                                "product_id": prod["product_id"],
                                "quantity": qty,
                                "unit_price": unit_price,
                                "revenue": round(qty * unit_price, 2),
                                "order_status": order_status,
                            })

    with open(OUTPUT_DIR / "fact_web_events.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=web_events[0].keys())
        writer.writeheader()
        writer.writerows(web_events)

    with open(OUTPUT_DIR / "fact_lead_events.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=lead_events[0].keys())
        writer.writeheader()
        writer.writerows(lead_events)

    with open(OUTPUT_DIR / "fact_orders.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)

    print("Synthetic data generated:")
    print(f"  Customers:        {len(customers)}")
    print(f"  Channels:         {len(channels)}")
    print(f"  Products:         {len(products)}")
    print(f"  Date rows:        {len(date_rows)}")
    print(f"  Web events:       {len(web_events)}")
    print(f"  Lead events:      {len(lead_events)}")
    print(f"  Order lines:      {len(orders)}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Anomaly dip month (for stretch goal): {ANOMALY_DIP_MONTH}")


if __name__ == "__main__":
    main()