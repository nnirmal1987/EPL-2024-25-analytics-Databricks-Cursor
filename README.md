 # ⚽ Premier League 2024-25 Analytics Pipeline

> End-to-end data engineering project — Kaggle → AWS S3 → Databricks Unity Catalog → Delta Lake → Power BI

## 📌 Overview

A production-style data pipeline that ingests **Premier League 2024-25** football data, processes it through **Medallion Architecture** (Bronze → Silver → Gold), and delivers a **Power BI dashboard** with KPI cards, xG analysis, player rankings, and EPL table.

## 🏗️ Architecture

```
Kaggle Dataset (matches · players · standings)
        │
        ▼
┌─────────────────────────────┐
│   01_kaggle_download.py     │  Download & standardise CSVs locally
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│   02_upload_to_s3.py        │  Upload to AWS S3 Free Tier
└─────────────────────────────┘
        │
        ▼
  s3://football-analytics-nirmal/bronze/premier-league/2024-25/
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│              Databricks Unity Catalog                    │
│                                                          │
│  BRONZE   →   SILVER   →   GOLD                         │
│  Raw CSVs,     Cleaned,       Aggregated KPIs             │
│  + lineage    + typed        + rankings                 │
│              + derived       + home/away split          │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│   Power BI Desktop  .PBIT        │  EPL Table and a few player/team stats
│   (DAX + Direct Query)      │
└─────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| Language | Python 3.10+ | Data ingestion & transformation |
| Big Data | Apache Spark / PySpark | Distributed processing |
| Platform | Databricks Community Edition | Managed Spark clusters |
| Catalog | Unity Catalog | Data governance & table registry |
| Storage Format | Delta Lake | ACID transactions, time travel |
| Cloud Storage | AWS S3 Free Tier | Bronze layer data lake |
| Analytics | Spark SQL | SQL dashboards & aggregations |
| Visualisation | Power BI Desktop | Interactive dashboard |
| Measures | DAX | KPI calculations |

## 🗃️ Delta Tables

```
football.pl_2024_25
│
├── BRONZE   bronze_standings · bronze_matches · bronze_players
├── SILVER   silver_standings · silver_matches · silver_players
└── GOLD     gold_team_performance · gold_player_rankings 
| Source Data | Kaggle API | Premier League 2024-25 datasets |
```
## 🚀Setup Instructions

### Prerequisites
- Python 3.10+, Cursor
- [Databricks Community Edition](https://community.cloud.databricks.com) — free
- [AWS Free Tier](https://aws.amazon.com/free) account
- [Kaggle](https://kaggle.com) account
- Power BI Desktop (Windows)

## Step 1 — Install dependencies. Have Cursor installed**
pip install kaggle pandas boto3 requests beautifulsoup4 lxml

### Step 2 — Kaggle API credentials
1. [kaggle.com/settings](https://kaggle.com/settings) → **API** → **Create Legacy API Token**
2. Move `kaggle.json` to `C:\Users\YourName\.kaggle\` (Windows) or `~/.kaggle/` (Mac/Linux)

### Step 3 — AWS S3 setup
1. Create S3 bucket: `football-analytics-yourname` in `us-east-1`
2. IAM → Create User → attach `AmazonS3FullAccess` → create Access Key
3. Fill credentials into `src/02_upload_to_s3.py` CONFIG section

### Step 4 — Download & upload data ### Step 5 — Run Databricks pipeline
```bash
python src/01_kaggle_download.py
python src/02_upload_to_s3.py
```

### Step 5 — Run Databricks pipeline
1. Import `notebooks/03_databricks_pipeline_uc.py` into Databricks
2. Create a cluster (Runtime 13.x+) and attach
3. Fill in your S3 bucket name in the CONFIG cell
4. Click **Run All**

### Step 6 — Connect Power BI
1. Databricks → SQL Warehouses → copy **Server hostname** and **HTTP Path**
2. Settings → Developer → **Generate Access Token**
3. Power BI → **Get Data → Azure Databricks** → paste connection details
4. Load: `gold_player_rankings`, `gold_team_performance`, `gold_goalkeeper_rankings`
5. Add DAX measures from `powerbi/` folder via **Modeling → New Measure**
## 📈 Key Metrics Engineered

## ⚠️ Security

Never commit real credentials — replace with placeholder text before pushing. `.gitignore` blocks `kaggle.json` and `.env` files automatically.
