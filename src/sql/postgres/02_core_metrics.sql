-- =====================================================================
-- Customer Journey Funnel Tracker — Core Metrics (Window Functions) v2
-- Project 3 Learning Objective:
--   "Apply window-function SQL (running totals, period-over-period
--    comparisons) inside a proper star schema."
--
-- Schema: 3 separate fact tables — fact_web_events, fact_lead_events,
-- fact_orders — chained by customer_key + date_key.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. FUNNEL STAGE COUNTS PER WEEK (across all 3 fact tables)
-- ---------------------------------------------------------------------
WITH stage_events AS (
    SELECT date_key, customer_key, 'web_visit' AS stage
    FROM fact_web_events

    UNION ALL

    SELECT date_key, customer_key, 'lead_created' AS stage
    FROM fact_lead_events
    WHERE lead_status = 'created'

    UNION ALL

    SELECT date_key, customer_key, 'opportunity' AS stage
    FROM fact_lead_events
    WHERE lead_status = 'opportunity'

    UNION ALL

    SELECT date_key, customer_key, 'order' AS stage
    FROM fact_orders
    WHERE order_status = 'completed'
),
weekly_funnel AS (
    SELECT
        d.year,
        d.week_of_year,
        MIN(d.full_date) AS week_start_date,
        se.stage,
        COUNT(DISTINCT se.customer_key) AS distinct_customers
    FROM stage_events se
    JOIN dim_date d ON se.date_key = d.date_key
    GROUP BY d.year, d.week_of_year, se.stage
)
SELECT * FROM weekly_funnel
ORDER BY year, week_of_year, stage;


-- ---------------------------------------------------------------------
-- 2. RUNNING TOTAL OF ORDER REVENUE WITHIN A YEAR
-- ---------------------------------------------------------------------
WITH daily_revenue AS (
    SELECT
        d.full_date,
        d.year,
        SUM(fo.revenue) AS daily_revenue
    FROM fact_orders fo
    JOIN dim_date d ON fo.date_key = d.date_key
    WHERE fo.order_status = 'completed'
    GROUP BY d.full_date, d.year
)
SELECT
    full_date,
    year,
    daily_revenue,
    SUM(daily_revenue) OVER (
        PARTITION BY year
        ORDER BY full_date
        ROWS UNBOUNDED PRECEDING
    ) AS running_total_revenue
FROM daily_revenue
ORDER BY full_date;


-- ---------------------------------------------------------------------
-- 3. WEEK-OVER-WEEK (WoW) DELTA — funnel stage counts
-- ---------------------------------------------------------------------
WITH stage_events AS (
    SELECT date_key, customer_key, 'web_visit' AS stage FROM fact_web_events
    UNION ALL
    SELECT date_key, customer_key, 'lead_created' FROM fact_lead_events WHERE lead_status = 'created'
    UNION ALL
    SELECT date_key, customer_key, 'opportunity' FROM fact_lead_events WHERE lead_status = 'opportunity'
    UNION ALL
    SELECT date_key, customer_key, 'order' FROM fact_orders WHERE order_status = 'completed'
),
weekly_funnel AS (
    SELECT
        d.year,
        d.week_of_year,
        MIN(d.full_date) AS week_start_date,
        se.stage,
        COUNT(DISTINCT se.customer_key) AS distinct_customers
    FROM stage_events se
    JOIN dim_date d ON se.date_key = d.date_key
    GROUP BY d.year, d.week_of_year, se.stage
)
SELECT
    year,
    week_of_year,
    week_start_date,
    stage,
    distinct_customers,
    LAG(distinct_customers) OVER (
        PARTITION BY stage ORDER BY year, week_of_year
    ) AS prior_week_customers,
    distinct_customers - LAG(distinct_customers) OVER (
        PARTITION BY stage ORDER BY year, week_of_year
    ) AS wow_delta,
    ROUND(
        100.0 * (
            distinct_customers - LAG(distinct_customers) OVER (
                PARTITION BY stage ORDER BY year, week_of_year
            )
        ) / NULLIF(LAG(distinct_customers) OVER (
                PARTITION BY stage ORDER BY year, week_of_year
            ), 0),
        1
    ) AS wow_pct_change
FROM weekly_funnel
ORDER BY stage, year, week_of_year;


-- ---------------------------------------------------------------------
-- 4. YEAR-OVER-YEAR (YoY) DELTA — order revenue, by ISO week
-- ---------------------------------------------------------------------
WITH weekly_revenue AS (
    SELECT
        d.year,
        d.week_of_year,
        MIN(d.full_date) AS week_start_date,
        SUM(fo.revenue)  AS weekly_revenue
    FROM fact_orders fo
    JOIN dim_date d ON fo.date_key = d.date_key
    WHERE fo.order_status = 'completed'
    GROUP BY d.year, d.week_of_year
)
SELECT
    year,
    week_of_year,
    week_start_date,
    weekly_revenue,
    LAG(weekly_revenue) OVER (
        PARTITION BY week_of_year ORDER BY year
    ) AS prior_year_same_week_revenue,
    weekly_revenue - LAG(weekly_revenue) OVER (
        PARTITION BY week_of_year ORDER BY year
    ) AS yoy_delta,
    ROUND(
        100.0 * (
            weekly_revenue - LAG(weekly_revenue) OVER (
                PARTITION BY week_of_year ORDER BY year
            )
        ) / NULLIF(LAG(weekly_revenue) OVER (
                PARTITION BY week_of_year ORDER BY year
            ), 0),
        1
    ) AS yoy_pct_change
FROM weekly_revenue
ORDER BY week_of_year, year;


-- ---------------------------------------------------------------------
-- 5. FUNNEL CONVERSION RATE BETWEEN STAGES (per week)
-- ---------------------------------------------------------------------
WITH stage_events AS (
    SELECT date_key, customer_key, 'web_visit' AS stage FROM fact_web_events
    UNION ALL
    SELECT date_key, customer_key, 'lead_created' FROM fact_lead_events WHERE lead_status = 'created'
    UNION ALL
    SELECT date_key, customer_key, 'opportunity' FROM fact_lead_events WHERE lead_status = 'opportunity'
    UNION ALL
    SELECT date_key, customer_key, 'order' FROM fact_orders WHERE order_status = 'completed'
),
weekly_funnel AS (
    SELECT
        d.year,
        d.week_of_year,
        MIN(d.full_date) AS week_start_date,
        se.stage,
        COUNT(DISTINCT se.customer_key) AS distinct_customers
    FROM stage_events se
    JOIN dim_date d ON se.date_key = d.date_key
    GROUP BY d.year, d.week_of_year, se.stage
),
pivoted AS (
    SELECT
        year,
        week_of_year,
        week_start_date,
        MAX(CASE WHEN stage = 'web_visit'    THEN distinct_customers END) AS web_visits,
        MAX(CASE WHEN stage = 'lead_created' THEN distinct_customers END) AS leads,
        MAX(CASE WHEN stage = 'opportunity'  THEN distinct_customers END) AS opportunities,
        MAX(CASE WHEN stage = 'order'        THEN distinct_customers END) AS order_count
    FROM weekly_funnel
    GROUP BY year, week_of_year, week_start_date
)
SELECT
    *,
    ROUND(100.0 * leads         / NULLIF(web_visits, 0), 1) AS visit_to_lead_pct,
    ROUND(100.0 * opportunities / NULLIF(leads, 0), 1)       AS lead_to_opportunity_pct,
    ROUND(100.0 * order_count   / NULLIF(opportunities, 0), 1) AS opportunity_to_order_pct
FROM pivoted
ORDER BY year, week_of_year;