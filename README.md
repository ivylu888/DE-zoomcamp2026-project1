# 🏋️ Global Powerlifting Strength Analysis

> An end-to-end data pipeline analyzing **3M+ powerlifting records** from OpenPowerlifting — tracking global strength sport trends across countries, equipment categories, and weight classes.

## Problem Description

Powerlifting is one of the fastest-growing strength sports worldwide. This project ingests the full OpenPowerlifting dataset, loads it into a cloud data warehouse, transforms the raw data into analytics-ready tables using dbt, and visualizes trends in a Looker Studio dashboard.

**Questions answered:**
- How has global powerlifting participation grown year over year?
- What is the distribution of athletes across equipment categories (Raw, Single-ply, etc.)?
- Which weight classes and countries produce the strongest lifters?

## Dashboard

👉 [View Dashboard](https://datastudio.google.com/reporting/866cd12f-4849-4655-85dd-6ae0e4dbc411)

**Tile 1 — Distribution of Athletes by Equipment Category** (categorical): Bar chart showing how many athletes compete under each equipment type.

**Tile 2 — Global Powerlifting Participation Trend** (temporal): Line chart showing the growth of powerlifting participation year over year since 2000.

## Architecture
```
OpenPowerlifting (weekly CSV)
        │
        ▼
  Mage AI Pipeline
        │
        ├──► GCS Bucket ──────────────── Data Lake
        │    gs://power-lifting-data-lake-2026/
        │    raw_powerlifting_data.parquet
        │
        ├──► BigQuery Raw ─────────────── powerlifting_data.raw_powerlifting
        │
        └──► dbt transformations
                 │
                 ▼
             BigQuery Models ─────────── powerlifting_data
                 ├─ stg_powerlifting     (view)
                 └─ fct_powerlifting     (table)
                          │
                          ▼
                   Looker Studio Dashboard
```

## Technologies

| Layer | Tool | Purpose |
|-------|------|---------|
| Cloud | GCP | All infrastructure |
| IaC | Terraform | Provision GCS + BigQuery |
| Orchestration | Mage AI | Pipeline orchestration |
| Data Lake | GCP Cloud Storage | Store raw Parquet files |
| Data Warehouse | BigQuery | Store and query structured data |
| Transformation | dbt | Staging + fact models |
| Dashboard | Looker Studio | Visualization |

## Dataset

- **Source:** [OpenPowerlifting](https://openpowerlifting.gitlab.io/opl-csv/)
- **Size:** 3M+ records
- **Format:** CSV (downloaded as ZIP, stored as Parquet)
- **Update frequency:** Weekly

## Project Structure
```
.
├── main.tf                     # IaC: GCS bucket + BigQuery dataset
├── docker-compose.yml          # Mage AI orchestration
├── Dockerfile
├── requirements.txt
├── pipelines/                  # Mage pipeline block code
│   ├── download_powerlifting_data.py
│   ├── export_to_gcs.py
│   └── load_to_bigquery.py
└── powerlifting_dbt/           # dbt transformation models
    └── models/
        ├── sources.yml
        ├── stg_powerlifting.sql
        └── fct_powerlifting.sql
```

## Reproducing This Project

### Prerequisites
- GCP account with billing enabled
- `gcloud` CLI installed and authenticated
- Terraform installed
- Docker + Docker Compose installed
- `pip install dbt-bigquery`

### Step 1 — Clone and configure
```bash
git clone https://github.com/ivylu888/DE-zoomcamp2026-project1.git
cd DE-zoomcamp2026-project1
```

### Step 2 — GCP Auth
```bash
gcloud auth application-default login
gcloud config set project YOUR_GCP_PROJECT_ID
```

### Step 3 — Infrastructure
```bash
terraform init
terraform apply
```
Creates:
- GCS Bucket: `power-lifting-data-lake-2026`
- BigQuery Dataset: `powerlifting_data`

### Step 4 — Environment Setup
```bash
cp dev.env.template .env
# Edit .env and fill in:
# GCP_PROJECT_ID, GCP_GCS_BUCKET_NAME, GCP_KEYFILE_PATH

cp powerlifting_dbt/profiles.yml.template powerlifting_dbt/profiles.yml
```

### Step 5 — Run the Pipeline

Mage automatically loads the `powerlifting_ingestion` pipeline from the pre-configured metadata in `magic-zoomcamp/pipelines/`. No manual setup is required.

Start the services:
```bash
docker-compose up -d
```

Access the Mage UI at [http://localhost:6789](http://localhost:6789) to run the pipeline.

### Step 6 — dbt Transformation
```bash
cd powerlifting_dbt
dbt run
```
Creates:
- `stg_powerlifting` — cleaned view (cast types, filter nulls)
- `fct_powerlifting` — aggregated table (64k rows by year/sex/equipment/country)

### Step 7 — Dashboard
Open the [Looker Studio Dashboard](https://datastudio.google.com/reporting/866cd12f-4849-4655-85dd-6ae0e4dbc411).

## dbt Model Details

### `stg_powerlifting` (view)
Cleans and casts the raw table: converts numeric columns from string to FLOAT64, parses dates, filters out records with null totals or dates, and extracts meet year.

### `fct_powerlifting` (table)
Aggregates lifter counts and average/max lift weights by year, sex, weight class, country, and equipment. 64k rows covering competitions from 2000 onwards.

## 🛠️ Maintenance & Tips

### Schema changes (partitioning / clustering)

If you modify the `config()` block in any model — especially partitioning or clustering settings — a regular `dbt run` will fail because BigQuery cannot alter these physical table properties in place.

Run the following command to rebuild the table from scratch:

```bash
dbt run --select fct_powerlifting --full-refresh
```

The `--full-refresh` flag tells dbt to issue a `CREATE OR REPLACE TABLE` statement, dropping the existing table and recreating it with the new partition and cluster configuration. Without it, dbt will attempt an `ALTER TABLE` which BigQuery does not support for structural changes like these.
