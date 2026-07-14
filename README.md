# Customer Journey Funnel

Customer Journey Funnel is a full-stack analytics and AI assistant project that turns synthetic customer journey data into actionable funnel insights. The platform combines a data engineering pipeline, a conversational analytics agent, and a React-based frontend so users can explore metrics such as revenue, orders, running totals, week-over-week changes, and year-over-year comparisons.

## What this project does

- Generates synthetic customer, product, channel, and transaction data
- Loads that data into PostgreSQL
- Builds a Bronze → Silver → Gold data lakehouse flow with Apache Spark and Iceberg
- Exposes business metrics through a FastAPI backend
- Lets users ask questions in natural language through a chat UI powered by an analytics agent

## Architecture overview

- Data generation: synthetic CSV files under the data/raw folder
- Storage: PostgreSQL for operational loading and Spark/Iceberg for lakehouse tables
- Backend: FastAPI service with route-based chat and metrics endpoints
- AI layer: a rule-based analytics agent with optional LLM fallback
- Frontend: React + Vite chat application

## Tech stack

- Python
- Apache Spark
- Apache Iceberg
- PostgreSQL
- FastAPI
- React + Vite
- Groq / LangChain-based LLM integration

## Project structure

- backend/: FastAPI app, analytics agent, metric tools, and LLM service
- frontend/: Vite + React frontend for chatting with the analytics assistant
- src/: data ingestion, Spark config, and transformation scripts
- data/raw/: generated CSV files used for ingestion
- warehouse/: Iceberg warehouse for Bronze, Silver, and Gold tables
- docs/: project evolution notes and documentation

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+ installed
- Node.js and npm installed
- PostgreSQL running locally
- Java installed for Spark
- A Groq API key in a .env file

## Environment setup

1. Create and activate a Python virtual environment
   - python -m venv .venv
   - .venv\Scripts\Activate.ps1

2. Install Python dependencies
   - pip install -r backend/requirements.txt

3. Install frontend dependencies
   - cd frontend
   - npm install

4. Create a .env file in the project root with:
   - GROQ_API_KEY=your_key_here
   - MODEL_NAME=your_model_name_here

5. Make sure PostgreSQL has a database named customer_journey_funnel
   - The project currently expects the local PostgreSQL user postgres with password Sql123

## Data pipeline

### Partitioning in this project

Partitioning is used to organize large fact tables in Iceberg so Spark can read and write data more efficiently. Instead of treating the data as one big table, the project splits it by event date.

Why this helps:

- Faster queries when filtering by date
- Better pruning, so Spark reads only the relevant partitions
- Lower memory pressure during writes
- Improved scalability for larger datasets

In this repository, the Bronze fact tables such as fact_web_events, fact_lead_events, and fact_orders are partitioned by event_date. The loader processes one year at a time so the write workload stays manageable and avoids memory issues on smaller machines.

This is especially useful for analytics workloads like customer journey tracking, where most questions are time-based and only a limited date range is needed.

### 1) Generate synthetic data

Run:

- python -m src.ingestion.generate_synthetic_data

This creates CSV files in data/raw for dimensions and fact tables.

### 2) Load data into PostgreSQL

Run:

- python -m src.ingestion.load_to_postgres

This loads the generated CSVs into PostgreSQL and resolves business-key to surrogate-key relationships.

### 3) Build Bronze layer in Iceberg

Run:

- python -m src.ingestion.bronze_loader

### 4) Build Silver layer in Iceberg

Run:

- python -m src.transformations.silver_loader

### 5) Build Gold layer in Iceberg

Run:

- python -m src.transformations.gold_loader

## Run the application

### Start the backend

Run:

- uvicorn backend.app:app --reload

The backend will be available at http://127.0.0.1:8000.

### Start the frontend

Run:

- cd frontend
- npm run dev

The frontend will be available in the Vite dev server.

## Example questions

You can ask the assistant questions such as:

- What was revenue on 2024-01-15?
- Show me orders for 2024-01-15.
- What is the running total for 2024-01-15?
- Compare this week’s lead funnel to the same week last year.
- Show me week-over-week performance for 2024-01-15.

## Testing

Run the backend metrics tests with:

- python -m unittest backend.tests.test_metrics_tools

## Requirement proof: Iceberg partitioning and partition evolution

This project satisfies the requirement to:

1. load data into Iceberg with daily partitioning, and
2. evolve the partitioning scheme from daily to monthly while preserving historical data.

The implementation is in [src/ingestion/bronze_loader.py](src/ingestion/bronze_loader.py) and [src/iceberg/partition_evolution.py](src/iceberg/partition_evolution.py).

Verified evidence:

- The Bronze fact table was rebuilt with daily partitioning before the evolution step.
- The partition evolution script completed successfully and reported: “Performing partition evolution: DAY → MONTH” and “✓ Partition evolution complete.”
- The explain outputs were captured in [docs/explain_before_evolution.txt](docs/explain_before_evolution.txt) and [docs/explain_after_evolution.txt](docs/explain_after_evolution.txt).
- The snapshot history showed append-based Iceberg operations rather than a full rewrite, which is consistent with metadata-only partition evolution and confirms that historical files were not rewritten.

## Notes

- The project uses a local Spark session configured for a laptop-friendly setup with tuned memory settings.
- The Iceberg warehouse is stored under the warehouse folder.
- The analytics agent uses rule-based routing for common metrics and falls back to an LLM for broader questions.

## Summary

This repository demonstrates how to combine data engineering, analytics, and conversational AI in a single project. It is designed as a practical example of building a customer journey funnel intelligence system from synthetic data all the way through to a user-facing chat experience.
