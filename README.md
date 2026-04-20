# Global Powerlifting Strength Analysis 🏋️

## Problem Statement

This project analyzes the **OpenPowerlifting public dataset** (3M+ records) to understand global powerlifting trends:
- How has participation grown over the years?
- What is the distribution of athletes across equipment categories?

## Architecture
```
OpenPowerlifting (Source)
        ↓
   [Mage Pipeline]
        ↓
   [GCP Cloud Storage]  ← Data Lake (Parquet)
        ↓
   [BigQuery]           ← Data Warehouse
        ↓
   [dbt]                ← Transformation
        ↓
   [Looker Studio]      ← Dashboard
```

## Technologies

| Layer | Tool |
|-------|------|
| Cloud | GCP |
| IaC | Terraform |
| Orchestration | Mage AI |
| Data Lake | GCP Cloud Storage |
| Data Warehouse | BigQuery |
| Transformation | dbt |
| Dashboard | Looker Studio |

## Dashboard

👉 [View Dashboard](https://datastudio.google.com/reporting/866cd12f-4849-4655-85dd-6ae0e4dbc411)

- **Tile 1:** Distribution of Athletes by Equipment Category
- **Tile 2:** Global Powerlifting Participation Trend (2000–present)

## Reproducibility

### Prerequisites
- GCP account with billing enabled
- Terraform installed
- Docker + Docker Compose installed
- `pip install dbt-bigquery`

### Step 1: GCP Auth
```bash
gcloud auth application-default login
gcloud config set project zoomcamp-powerlifting
```

### Step 2: Infrastructure
```bash
cd terraform
terraform init
terraform apply
```
Creates:
- GCS Bucket: `power-lifting-data-lake-2026`
- BigQuery Dataset: `powerlifting_data`

### Step 3: Mage Pipeline
```bash
cp dev.env .env
# Edit .env: fill in GCP_PROJECT_ID and GCP_GCS_BUCKET_NAME
docker-compose up -d
```
Go to `http://localhost:6789` and run the `powerlifting_ingestion` pipeline.

### Step 4: dbt
```bash
cd powerlifting_dbt
dbt run
```

### Step 5: Dashboard
Open the [Looker Studio link](https://datastudio.google.com/reporting/866cd12f-4849-4655-85dd-6ae0e4dbc411).