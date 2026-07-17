# 🧭 Customer Journey Funnel

## 📌 Project Overview

Customer Journey Funnel is a full-stack analytics and AI assistant project that turns synthetic customer journey data into actionable funnel insights. The project combines data engineering, analytics, and conversational AI so that users can explore business performance through natural-language questions instead of writing SQL manually.

The workflow begins with synthetic data representing customers, products, channels, dates, orders, web events, and lead events. This data is ingested into PostgreSQL and transformed into a lakehouse-style architecture using Apache Spark and Apache Iceberg. The result is a layered data model with Bronze, Silver, and Gold tables that supports reporting and advanced funnel analysis.

This repository demonstrates how raw event data can be cleaned, structured, and exposed through an interactive interface for everyday business analysis.

---

# 🎯 Objectives

The main objectives of this project are:

- Build a complete data pipeline for customer journey analytics
- Generate synthetic customer, product, channel, and transaction data
- Load data into PostgreSQL and Apache Iceberg tables
- Create Bronze, Silver, and Gold layers for analytics
- Expose business metrics through a conversational analytics assistant
- Support questions about revenue, orders, running totals, and trend comparisons

---

# 🏗️ System Architecture

![Customer Journey Funnel Architecture](image/archi.png)

The project follows a layered analytics architecture with the following components:

- Data generation and ingestion from raw CSV files stored in the data folder
- PostgreSQL for relational storage and initial loading of business data
- Apache Spark and Apache Iceberg for lakehouse-style table storage and transformation
- Partitioned Iceberg tables to improve query performance and support efficient time-based analytics
- A FastAPI backend for serving analytics endpoints and agent logic
- A React + Vite frontend for interacting with the assistant and viewing results
- A Power BI page for visualizing funnel performance, running trends, and year-over-year / week-over-week comparisons

This architecture makes it possible to move from raw source data to business-ready metrics in a structured and extendable way.

---

# 🔄 Data Pipeline

The project works through the following flow:

1. Generate synthetic datasets for dimensions and fact events.
2. Load the data into PostgreSQL for relational processing.
3. Create Bronze tables in Apache Iceberg for raw and lightly processed data.
4. Transform those tables into Silver and Gold layers for analytics.
5. Expose the resulting metrics through a FastAPI backend and a chat-based interface.

This pipeline allows the project to simulate the full lifecycle of an analytics platform, from ingestion to insight.

---

# 📁 Project Structure

The repository is organized into the main components below:

- backend/: FastAPI application, analytics agent, metric tools, and LLM-related services
- frontend/: React + Vite frontend for the chat experience
- src/: ingestion scripts, transformation scripts, Spark configuration, and Iceberg utilities
- data/raw/: generated CSV files used as the source datasets
- warehouse/: Iceberg warehouse containing Bronze, Silver, and Gold tables

---

# 🛠️ Technology Stack

- Python
- FastAPI
- Apache Spark
- Apache Iceberg
- PostgreSQL
- React + Vite
- Groq / LLM-based integration

---

# ✨ Features

- Generate synthetic customer journey data across customers, products, channels, orders, and events
- Load data into PostgreSQL for initial processing and relational storage
- Create Bronze, Silver, and Gold layers for analytics and reporting
- Use partitioned Iceberg tables for efficient time-based analysis of funnel events
- Support analytics queries for revenue, orders, funnel metrics, and trend analysis
- Provide a chat-based assistant for natural language questions about funnel performance
- Display metrics such as running totals, week-over-week changes, and year-over-year comparisons
- Include a Power BI page for funnel progression, running trends, and YoY/WoW insights

---

# 📊 Power BI Dashboard

The Power BI dashboard is built on top of the Gold Layer of the lakehouse using PostgreSQL as the semantic model source. It provides an interactive view of the customer journey funnel and revenue performance through KPI cards, trend analysis, and business visualizations.

## Features

- Interactive filters for year, month, channel, product, and region
- Funnel performance dashboard covering website sessions, total leads, total orders, conversion rate, and funnel progression from visit to order
- Running total revenue dashboard showing current-year revenue, last-year revenue, YoY change, YoY growth percentage, monthly comparison, top products, and regional revenue distribution

## DAX Measures

The semantic model includes analytical measures such as:

- Total Revenue
- Running Revenue (Current Year)
- Running Revenue (Previous Year)
- Revenue LY
- YoY Revenue Change
- YoY Growth Percentage
- Total Orders
- Website Sessions
- Total Leads
- Conversion Rate

## Data Model

The report follows a star schema with fact tables for orders, lead events, and web events, and dimension tables for date, customer, product, and channel. These relationships support efficient filtering, time intelligence calculations, and interactive reporting.

### Star Schema Explanation

In this model:

- Fact tables store measurable business events such as web visits, lead events, and completed orders.
- Dimension tables store descriptive attributes such as date, customer, product, and channel.
- The dimensions connect to the facts to enable slicing and dicing by time, customer segment, product, and acquisition channel.
- This structure makes it easier to build dashboards, calculate running totals, and compare performance over time using Power BI and DAX.

## Technologies Used

- Microsoft Power BI Desktop
- DAX (Data Analysis Expressions)
- PostgreSQL as the semantic model source
- Star schema data model

## Dashboard Highlights

- Interactive slicers for dynamic filtering
- Running total and year-over-year revenue analysis
- Funnel analytics from website session to order completion
- Product and regional performance insights
- Clean executive-style dashboard layout with KPI indicators

---

# 🧩 ER Diagram

The data model is organized around a set of core entities and transactional fact tables that describe the customer journey:

- Date: stores calendar information such as year, month, and day to support time-based reporting and trend analysis.
- Customer: represents each customer and includes business attributes such as region and segment.
- Product: captures product-related details used for sales and funnel analysis.
- Channel: represents the traffic or acquisition source such as web, email, or paid campaigns.
- Fact Web Events: records website interactions such as sessions and event types performed by customers.
- Fact Lead Events: stores lead-related events such as lead creation and lead status changes.
- Fact Orders: captures completed orders with revenue, quantity, and order status.

These entities are connected through relationships that allow the system to trace the customer journey from initial web interaction to lead generation and final purchase. The structure supports funnel analysis, revenue reporting, and time-based comparison across channels, products, and customer segments.

---

# � Future Improvements

Possible enhancements for this project include:

- Add more real-world customer and transaction datasets for richer analysis
- Extend the analytics assistant to support more complex funnel and cohort questions
- Improve the Power BI dashboard with additional executive and operational views
- Add automated alerts and monitoring for data quality and pipeline health
- Support deployment to cloud storage and containerized environments
- Expand the project with more advanced forecasting and anomaly detection features

---

# �💬 Example Questions

Users can ask the assistant questions such as:

- What was revenue on a specific date?
- Show me orders for a given day or period.
- What is the running total for the selected range?
- Compare this week’s performance with the same week last year.
- Explain the funnel trend from lead to order.

---

# 👨‍💻 Author

Nishan Duwal
