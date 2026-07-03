"""
Synthetic data generator — Customer Journey Funnel Tracker (Project 3)
v3: expanded dataset matching target volumes

Target:
  Customers:   150
  Products:     50
  Channels:      8
  Date range:  2018-01-01 to 2025-12-31 (~2,942 days)
  Web events:  ~60,000
  Lead events: ~20,000
  Orders:       ~7,000

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

NUM_CUSTOMERS = 150
START_DATE = date(2018, 1, 1)
END_DATE = date(2025, 12, 31)

DATE_DIM_BUFFER_DAYS = 20
DIM_DATE_END = END_DATE + timedelta(days=DATE_DIM_BUFFER_DAYS)

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

CHANNELS = [
    {"name": "Paid Search",    "category": "Paid",     "visit_weight": 20, "lead_conv": 0.38, "opp_conv": 0.45, "order_conv": 0.65},
    {"name": "Email",          "category": "Direct",   "visit_weight": 12, "lead_conv": 0.42, "opp_conv": 0.50, "order_conv": 0.70},
    {"name": "Organic",        "category": "Organic",  "visit_weight": 22, "lead_conv": 0.28, "opp_conv": 0.35, "order_conv": 0.58},
    {"name": "Referral",       "category": "Organic",  "visit_weight": 12, "lead_conv": 0.30, "opp_conv": 0.38, "order_conv": 0.60},
    {"name": "Social",         "category": "Paid",     "visit_weight": 14, "lead_conv": 0.24, "opp_conv": 0.28, "order_conv": 0.50},
    {"name": "Direct",         "category": "Direct",   "visit_weight": 10, "lead_conv": 0.32, "opp_conv": 0.40, "order_conv": 0.62},
    {"name": "Display Ads",    "category": "Paid",     "visit_weight":  6, "lead_conv": 0.20, "opp_conv": 0.22, "order_conv": 0.45},
    {"name": "Partner",        "category": "Organic",  "visit_weight":  4, "lead_conv": 0.35, "opp_conv": 0.42, "order_conv": 0.63},
]

PRODUCT_CATALOG = [
    # Accessories (15)
    {"name": "Wireless Mouse",            "category": "Accessories", "price": 24.99},
    {"name": "Mechanical Keyboard",       "category": "Accessories", "price": 89.99},
    {"name": "USB-C Hub",                 "category": "Accessories", "price": 39.99},
    {"name": "Laptop Stand",              "category": "Accessories", "price": 34.99},
    {"name": "Webcam HD",                 "category": "Accessories", "price": 59.99},
    {"name": "Wrist Rest",                "category": "Accessories", "price": 19.99},
    {"name": "Cable Management Kit",      "category": "Accessories", "price": 14.99},
    {"name": "USB-A Hub 4-Port",          "category": "Accessories", "price": 22.99},
    {"name": "Laptop Sleeve 15in",        "category": "Accessories", "price": 29.99},
    {"name": "Wireless Numpad",           "category": "Accessories", "price": 32.99},
    {"name": "Screen Cleaner Kit",        "category": "Accessories", "price": 9.99},
    {"name": "Magnetic Cable Clips",      "category": "Accessories", "price": 12.99},
    {"name": "Monitor Arm Single",        "category": "Accessories", "price": 49.99},
    {"name": "Keyboard Tray",             "category": "Accessories", "price": 44.99},
    {"name": "Docking Station",           "category": "Accessories", "price": 129.99},
    # Displays (6)
    {"name": "27in Monitor",              "category": "Displays",    "price": 249.99},
    {"name": "32in 4K Monitor",           "category": "Displays",    "price": 449.99},
    {"name": "24in IPS Monitor",          "category": "Displays",    "price": 189.99},
    {"name": "Portable Monitor 15in",     "category": "Displays",    "price": 159.99},
    {"name": "Ultrawide 34in Monitor",    "category": "Displays",    "price": 549.99},
    {"name": "Privacy Screen Filter",     "category": "Displays",    "price": 39.99},
    # Audio (7)
    {"name": "Noise Cancelling Headphones", "category": "Audio",    "price": 179.99},
    {"name": "USB Microphone",            "category": "Audio",       "price": 89.99},
    {"name": "Desk Speaker Pair",         "category": "Audio",       "price": 119.99},
    {"name": "Headphone Stand",           "category": "Audio",       "price": 24.99},
    {"name": "Bluetooth Earbuds",         "category": "Audio",       "price": 79.99},
    {"name": "Audio Mixer 4-Channel",     "category": "Audio",       "price": 149.99},
    {"name": "Soundbar Compact",          "category": "Audio",       "price": 99.99},
    # Office (10)
    {"name": "Desk Lamp LED",             "category": "Office",      "price": 29.99},
    {"name": "Ergonomic Chair",           "category": "Office",      "price": 329.99},
    {"name": "Standing Desk",             "category": "Office",      "price": 449.99},
    {"name": "Whiteboard 36x24",          "category": "Office",      "price": 59.99},
    {"name": "Cable Trunking 2m",         "category": "Office",      "price": 17.99},
    {"name": "Under-Desk Drawer",         "category": "Office",      "price": 39.99},
    {"name": "Monitor Riser",             "category": "Office",      "price": 27.99},
    {"name": "Footrest Adjustable",       "category": "Office",      "price": 34.99},
    {"name": "Desk Organiser Set",        "category": "Office",      "price": 22.99},
    {"name": "Anti-Fatigue Mat",          "category": "Office",      "price": 49.99},
    # Networking (6)
    {"name": "WiFi 6 Router",             "category": "Networking",  "price": 129.99},
    {"name": "Network Switch 8-Port",     "category": "Networking",  "price": 44.99},
    {"name": "Ethernet Cable 5m",         "category": "Networking",  "price": 8.99},
    {"name": "Powerline Adapter Kit",     "category": "Networking",  "price": 59.99},
    {"name": "WiFi Range Extender",       "category": "Networking",  "price": 39.99},
    {"name": "NAS Drive 4TB",             "category": "Networking",  "price": 199.99},
    # Power (6)
    {"name": "UPS Battery Backup",        "category": "Power",       "price": 89.99},
    {"name": "Surge Protector 6-Outlet",  "category": "Power",       "price": 24.99},
    {"name": "GaN Charger 65W",           "category": "Power",       "price": 44.99},
    {"name": "Wireless Charging Pad",     "category": "Power",       "price": 19.99},
    {"name": "Power Strip Tower",         "category": "Power",       "price": 34.99},
    {"name": "Solar Charging Panel",      "category": "Power",       "price": 79.99},
]

SEGMENTS = ["SMB", "Enterprise", "Consumer"]
REGIONS = ["North America", "EMEA", "APAC", "LATAM"]

# Deliberate anomaly dip for stretch goal (anomaly detection)
ANOMALY_DIP_MONTH = (2024, 3)
ANOMALY_DIP_FACTOR = 0.30

# YoY growth trend — Year 2 onward grows slightly
GROWTH_PER_YEAR = 0.08  # 8% more activity each year


def daterange(start: date, end: date):
    days = (end - start).days
    for i in range(days + 1):
        yield start + timedelta(days=i)


def seasonal_activity_multiplier(d: date) -> float:
    multiplier = 1.0
    # Holiday season bump Nov-Dec
    if d.month in (11, 12):
        multiplier *= 1.7
    # Q4 back-to-school bump (Sep)
    if d.month == 9:
        multiplier *= 1.2
    # Year-over-year growth
    years_since_start = (d.year - START_DATE.year)
    multiplier *= (1 + GROWTH_PER_YEAR) ** years_since_start
    # Deliberate anomaly dip
    if (d.year, d.month) == ANOMALY_DIP_MONTH:
        multiplier *= ANOMALY_DIP_FACTOR
    # Weekend dip
    if d.weekday() >= 5:
        multiplier *= 0.65
    return multiplier


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # dim_customer
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        signup_date = fake.date_between(start_date=START_DATE, end_date=END_DATE - timedelta(days=90))
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

    # dim_channel
    channels = [{"channel_name": c["name"], "channel_category": c["category"]} for c in CHANNELS]
    with open(OUTPUT_DIR / "dim_channel.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=channels[0].keys())
        writer.writeheader()
        writer.writerows(channels)

    # dim_product
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

    # dim_date
    date_rows = []
    for d in daterange(START_DATE, DIM_DATE_END):
        date_rows.append({
            "date_key":    int(d.strftime("%Y%m%d")),
            "full_date":   d.isoformat(),
            "day_of_week": d.isoweekday(),
            "day_name":    d.strftime("%A"),
            "week_of_year": int(d.strftime("%V")),
            "month":       d.month,
            "month_name":  d.strftime("%B"),
            "quarter":     (d.month - 1) // 3 + 1,
            "year":        d.year,
            "is_weekend":  d.weekday() >= 5,
        })

    with open(OUTPUT_DIR / "dim_date.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=date_rows[0].keys())
        writer.writeheader()
        writer.writerows(date_rows)

    # Fact tables
    web_events, lead_events, orders = [], [], []
    lead_id_counter = 1
    order_id_counter = 1

    for cust in customers:
        signup = date.fromisoformat(cust["signup_date"])
        active_days = [d for d in daterange(signup, END_DATE)]

        engagement = random.uniform(0.3, 2.0)
        base_visits_per_month = 5.0 * engagement

        for d in active_days:
            multiplier = seasonal_activity_multiplier(d)
            daily_visit_prob = min(0.92, (base_visits_per_month / 30) * multiplier)
            if random.random() > daily_visit_prob:
                continue

            channel = random.choices(CHANNELS, weights=[c["visit_weight"] for c in CHANNELS])[0]
            visit_time = datetime.combine(d, datetime.min.time()) + timedelta(
                hours=random.randint(7, 22), minutes=random.randint(0, 59)
            )
            session_id = fake.uuid4()

            web_events.append({
                "date_key":        int(d.strftime("%Y%m%d")),
                "customer_id":     cust["customer_id"],
                "channel_name":    channel["name"],
                "event_timestamp": visit_time.isoformat(sep=" "),
                "session_id":      session_id,
                "page_url":        random.choice(["/", "/products", "/pricing", "/about", "/checkout"]),
            })

            if random.random() < channel["lead_conv"]:
                lead_id = f"LEAD{lead_id_counter:05d}"
                lead_id_counter += 1
                lead_created_time = visit_time + timedelta(hours=random.randint(1, 48))
                lead_events.append({
                    "lead_id":         lead_id,
                    "date_key":        int(lead_created_time.date().strftime("%Y%m%d")),
                    "customer_id":     cust["customer_id"],
                    "channel_name":    channel["name"],
                    "event_timestamp": lead_created_time.isoformat(sep=" "),
                    "lead_status":     "created",
                })

                if random.random() < channel["opp_conv"]:
                    qualified_time = lead_created_time + timedelta(hours=random.randint(2, 72))
                    lead_events.append({
                        "lead_id":         lead_id,
                        "date_key":        int(qualified_time.date().strftime("%Y%m%d")),
                        "customer_id":     cust["customer_id"],
                        "channel_name":    channel["name"],
                        "event_timestamp": qualified_time.isoformat(sep=" "),
                        "lead_status":     "qualified",
                    })

                    opp_time = qualified_time + timedelta(hours=random.randint(2, 96))
                    lead_events.append({
                        "lead_id":         lead_id,
                        "date_key":        int(opp_time.date().strftime("%Y%m%d")),
                        "customer_id":     cust["customer_id"],
                        "channel_name":    channel["name"],
                        "event_timestamp": opp_time.isoformat(sep=" "),
                        "lead_status":     "opportunity",
                    })

                    if random.random() < channel["order_conv"]:
                        order_time = opp_time + timedelta(hours=random.randint(4, 120))
                        order_id = f"ORD{order_id_counter:05d}"
                        order_id_counter += 1

                        num_lines = random.choices([1, 2, 3], weights=[0.55, 0.35, 0.10])[0]
                        chosen_products = random.sample(products, k=num_lines)
                        order_status = random.choices(
                            ["completed", "cancelled", "refunded"],
                            weights=[0.87, 0.08, 0.05]
                        )[0]

                        for prod in chosen_products:
                            qty = random.choices([1, 2, 3], weights=[0.70, 0.22, 0.08])[0]
                            unit_price = float(prod["unit_price"])
                            orders.append({
                                "order_id":     order_id,
                                "date_key":     int(order_time.date().strftime("%Y%m%d")),
                                "customer_id":  cust["customer_id"],
                                "channel_name": channel["name"],
                                "product_id":   prod["product_id"],
                                "quantity":     qty,
                                "unit_price":   unit_price,
                                "revenue":      round(qty * unit_price, 2),
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
    print(f"  Anomaly dip:      {ANOMALY_DIP_MONTH} (factor {ANOMALY_DIP_FACTOR})")
    print(f"  YoY growth rate:  {GROWTH_PER_YEAR*100:.0f}% per year")


if __name__ == "__main__":
    main()