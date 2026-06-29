-- =====================================================================
-- Customer Journey Funnel Tracker — Star Schema DDL (v2)
-- Project 3: Power BI Dashboard & Conversational Analyst
--
-- Funnel chain:  fact_web_events -> fact_lead_events -> fact_orders
--   (Website Visit -> Lead Created -> Opportunity -> Order)
--
-- Grain notes:
--   fact_web_events  : one row per website visit/page-view event
--   fact_lead_events : one row per lead lifecycle event
--                      (lead_status: 'created' | 'qualified' | 'opportunity')
--   fact_orders      : one row per ORDER LINE (one product within one
--                      order) — order header totals are derived via
--                      GROUP BY order_id (see vw_order_headers below),
--                      not stored separately.
-- =====================================================================

-- DIMENSION: dim_date
CREATE TABLE IF NOT EXISTS dim_date (
    date_key        INT PRIMARY KEY,
    full_date       DATE NOT NULL,
    day_of_week     SMALLINT NOT NULL,
    day_name        VARCHAR(9) NOT NULL,
    week_of_year    SMALLINT NOT NULL,
    month           SMALLINT NOT NULL,
    month_name      VARCHAR(9) NOT NULL,
    quarter         SMALLINT NOT NULL,
    year            SMALLINT NOT NULL,
    is_weekend      BOOLEAN NOT NULL
);

-- DIMENSION: dim_customer
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key    SERIAL PRIMARY KEY,
    customer_id     VARCHAR(20) NOT NULL UNIQUE,
    customer_name   VARCHAR(120) NOT NULL,
    segment         VARCHAR(20)  NOT NULL,
    region          VARCHAR(50)  NOT NULL,
    signup_date     DATE         NOT NULL
);

-- DIMENSION: dim_channel
CREATE TABLE IF NOT EXISTS dim_channel (
    channel_key       SERIAL PRIMARY KEY,
    channel_name      VARCHAR(50) NOT NULL UNIQUE,
    channel_category  VARCHAR(20) NOT NULL
);

-- DIMENSION: dim_product
CREATE TABLE IF NOT EXISTS dim_product (
    product_key     SERIAL PRIMARY KEY,
    product_id      VARCHAR(20) NOT NULL UNIQUE,
    product_name    VARCHAR(120) NOT NULL,
    category        VARCHAR(50) NOT NULL,
    unit_price      NUMERIC(10,2) NOT NULL
);

-- FACT: fact_web_events
CREATE TABLE IF NOT EXISTS fact_web_events (
    web_event_key   BIGSERIAL PRIMARY KEY,
    date_key        INT NOT NULL REFERENCES dim_date(date_key),
    customer_key    INT NOT NULL REFERENCES dim_customer(customer_key),
    channel_key     INT NOT NULL REFERENCES dim_channel(channel_key),
    event_timestamp TIMESTAMP NOT NULL,
    session_id      VARCHAR(40) NOT NULL,
    page_url        VARCHAR(200)
);

CREATE INDEX IF NOT EXISTS idx_web_events_date     ON fact_web_events(date_key);
CREATE INDEX IF NOT EXISTS idx_web_events_customer ON fact_web_events(customer_key);

-- FACT: fact_lead_events
CREATE TABLE IF NOT EXISTS fact_lead_events (
    lead_event_key  BIGSERIAL PRIMARY KEY,
    lead_id         VARCHAR(20) NOT NULL,
    date_key        INT NOT NULL REFERENCES dim_date(date_key),
    customer_key    INT NOT NULL REFERENCES dim_customer(customer_key),
    channel_key     INT NOT NULL REFERENCES dim_channel(channel_key),
    event_timestamp TIMESTAMP NOT NULL,
    lead_status     VARCHAR(20) NOT NULL CHECK (lead_status IN ('created', 'qualified', 'opportunity'))
);

CREATE INDEX IF NOT EXISTS idx_lead_events_date     ON fact_lead_events(date_key);
CREATE INDEX IF NOT EXISTS idx_lead_events_customer ON fact_lead_events(customer_key);
CREATE INDEX IF NOT EXISTS idx_lead_events_status   ON fact_lead_events(lead_status);
CREATE INDEX IF NOT EXISTS idx_lead_events_lead_id  ON fact_lead_events(lead_id);

-- FACT: fact_orders
CREATE TABLE IF NOT EXISTS fact_orders (
    order_line_key  BIGSERIAL PRIMARY KEY,
    order_id        VARCHAR(20) NOT NULL,
    date_key        INT NOT NULL REFERENCES dim_date(date_key),
    customer_key    INT NOT NULL REFERENCES dim_customer(customer_key),
    channel_key     INT NOT NULL REFERENCES dim_channel(channel_key),
    product_key     INT NOT NULL REFERENCES dim_product(product_key),
    quantity        INT NOT NULL CHECK (quantity > 0),
    unit_price      NUMERIC(10,2) NOT NULL,
    revenue         NUMERIC(12,2) NOT NULL,
    order_status    VARCHAR(20) NOT NULL CHECK (order_status IN ('completed', 'cancelled', 'refunded'))
);

CREATE INDEX IF NOT EXISTS idx_orders_date     ON fact_orders(date_key);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON fact_orders(customer_key);
CREATE INDEX IF NOT EXISTS idx_orders_order_id ON fact_orders(order_id);

-- VIEW: order header totals derived from order-line grain
CREATE OR REPLACE VIEW vw_order_headers AS
SELECT
    order_id,
    date_key,
    customer_key,
    channel_key,
    SUM(revenue)      AS order_total_revenue,
    SUM(quantity)     AS total_items,
    MAX(order_status) AS order_status
FROM fact_orders
GROUP BY order_id, date_key, customer_key, channel_key;