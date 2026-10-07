# NYC Mobility Intelligence 🚕

## Big Data Architecture & Strategy Capstone

NYC Mobility Intelligence is an end-to-end Big Data solution designed to transform large-scale New York City High Volume For-Hire Vehicle (FHVHV) trip data into actionable information for mobility and operational decision-making.

The project processes **15.86 GiB of raw Parquet data**, representing **684,376,551 trip records from January 2022 through December 2024**. The solution integrates Google Cloud Storage, Google Dataproc, PySpark, MariaDB, SQL, and Streamlit to demonstrate a scalable pipeline from raw ingestion to executive analytics.

---

## 1. Business Problem

High-volume mobility data can contain hundreds of millions of individual trip records, making conventional local databases, spreadsheets, and simple scripts inefficient for repeated large-scale analysis.

The project addresses the challenge of transforming this volume of historical trip data into a manageable analytical product that allows decision-makers to understand:

- How mobility demand changes over time.
- Which hours and days concentrate the highest trip volumes.
- How trip duration and average speed behave throughout the day.
- Which pickup and dropoff zones concentrate activity.
- How passenger base fares and driver payments evolve over time.

The objective is not only to process the data, but to convert it into information that can support operational planning and mobility analysis.

---

## 2. Solution Overview

The solution follows a simple distributed architecture:

```text
NYC TLC FHVHV Data
        ↓
Google Cloud Storage
      RAW Layer
        ↓
Google Dataproc
     + PySpark
        ↓
Cleaning + Transformation
        ↓
Google Cloud Storage
   CURATED Parquet
 (partitioned by year/month)
        ↓
Analytical Aggregations
        ↓
 ┌─────────────────┬─────────────────┐
 │                 │                 │
MariaDB         Analytical CSVs
SQL Layer            │
                     ↓
                  Streamlit
                     ↓
          Executive Dashboard
```

The architecture follows the **KISS principle**: the full dataset is processed with distributed computing, while the final dashboard consumes compact analytical outputs rather than repeatedly scanning hundreds of millions of records.

---

## 3. Data Source and Scale

**Source:** NYC Taxi & Limousine Commission (NYC TLC) – High Volume For-Hire Vehicle Trip Records.

**Period:** January 2022 – December 2024.

**Files:** 36 monthly Parquet files.

| Metric | Result |
|---|---:|
| Raw storage volume | 15.86 GiB |
| Original records | 684,376,551 |
| Clean records | 683,913,899 |
| Removed invalid records | 462,652 |
| Removed share | 0.0676% |
| Time coverage | 36 months |

Raw data is preserved separately from transformed data to maintain traceability and reproducibility.

---

## 4. Data Pipeline

### Ingestion

Monthly Parquet files were ingested into a Google Cloud Storage RAW layer.

### Cleaning and Transformation

PySpark on Google Dataproc was used to perform distributed validation and transformation.

Quality controls included:

- Invalid or non-positive trip distances.
- Invalid or non-positive trip durations.
- Negative passenger base fares.
- Negative driver payments.
- Invalid pickup/dropoff dates.
- Null analysis for relevant fields.
- Schema compatibility across monthly Parquet files.

Additional analytical variables were derived, including:

- `year`
- `month`
- `day_of_week`
- `pickup_hour`
- `trip_minutes`
- `avg_speed_mph`

### Storage Optimization

The cleaned dataset was stored as Parquet in the CURATED layer and partitioned by:

```text
year/
└── month/
```

All **36 year-month partitions** were validated successfully.

Partition pruning was also verified during Spark execution. A filtered query for December 2024 processed a partition containing **21,062,630 trips in approximately 0.69 seconds**.

---

## 5. Analytical Layer

Instead of sending the full curated dataset to the visualization layer, PySpark generates compact analytical datasets for executive consumption.

The project includes:

- Annual trip summary.
- Monthly demand summary.
- Hourly demand and operational indicators.
- Day-of-week demand.
- Top pickup zones.
- Top dropoff zones.
- Monthly passenger fare and driver pay indicators.

These analytical outputs are persisted and used by downstream SQL and visualization components.

---

## 6. MariaDB / SQL Layer

A MariaDB analytical layer was implemented to demonstrate relational consumption of the processed Big Data outputs.

Seven analytical tables were created and validated:

| Table | Rows |
|---|---:|
| `annual_sql_summary` | 3 |
| `daily_summary` | 7 |
| `hourly_summary` | 24 |
| `monthly_economics` | 36 |
| `monthly_summary` | 36 |
| `top_dropoff_zones` | 264 |
| `top_pickup_zones` | 263 |

The repository includes reproducible SQL scripts for schema creation and data loading.

---

## 7. Executive Dashboard

The processed analytical results are presented through an interactive Streamlit application.

The dashboard currently provides:

- Executive KPIs.
- Annual and monthly demand evolution.
- Demand by hour.
- Demand by day of week.
- Average operating speed by hour.
- Top pickup and dropoff zones.
- Passenger base fare and driver pay trends.

### Live Application

https://nyc-mobility-big-data-cpfpwpukkxthk22kkzkpet.streamlit.app/

The final application is designed around two perspectives:

**Project Strategy**  
Explains the business problem, architecture, CDO framework and expected strategic impact.

**Mobility Intelligence**  
Represents the operational product that a decision-maker would use to explore mobility patterns and support planning decisions.

---

## 8. Key Findings

Initial analysis identifies several relevant patterns:

- Annual trip volume increased from approximately **212.1 million trips in 2022** to **239.4 million in 2024**.
- The highest cumulative hourly demand occurs around **18:00**.
- **Saturday** presents the highest cumulative trip volume by day of week.
- Average operating speed declines substantially during high-demand daytime and afternoon periods.
- Passenger base fare and driver pay indicators show an upward trend over the analyzed period.

These findings provide the foundation for the project's strategic recommendations and executive decision-support layer.

---

## 9. Technology Stack

| Layer | Technology |
|---|---|
| Source | NYC TLC |
| Cloud Storage | Google Cloud Storage |
| Distributed Processing | Google Dataproc |
| Big Data Engine | Apache Spark / PySpark |
| Optimized Storage | Partitioned Parquet |
| SQL Layer | MariaDB |
| Visualization | Streamlit |
| Version Control | GitHub |

---

## 10. Repository Structure

```text
nyc-mobility-big-data/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── annual_sql_summary.csv
│   ├── daily_summary.csv
│   ├── hourly_summary.csv
│   ├── monthly_economics.csv
│   ├── monthly_summary.csv
│   ├── top_dropoff_zones.csv
│   └── top_pickup_zones.csv
│
├── ipynb/
│   └── NYC_Mobility_Big_Data.ipynb
│
└── sql/
    ├── 01_schema_mariadb.sql
    └── 02_load_data.sql
```

Large RAW and CURATED datasets are intentionally not stored in GitHub.

---

## 11. CDO Strategic Framework

The project is structured around four strategic questions:

### What are we building?

A scalable mobility intelligence product that transforms hundreds of millions of NYC for-hire vehicle trip records into operational and executive indicators.

### Why are we building it?

To reduce the complexity of analyzing large historical mobility datasets and provide decision-makers with accessible information about demand, operational behavior, geographic concentration and economic trends.

### How are we solving it?

Through a distributed Big Data architecture using GCS for storage, Dataproc and PySpark for large-scale ETL, partitioned Parquet for optimized persistence, MariaDB for relational analytical consumption, and Streamlit for executive visualization.

### Who benefits and what is the ROI?

The primary users are mobility operations and planning decision-makers who need rapid access to historical demand and operating patterns.

The ROI component will be evaluated through explicit operational scenarios and measurable assumptions rather than unsupported claims of realized financial savings.

---

## 12. Current Project Status

- [x] 15+ GB data ingestion
- [x] Distributed PySpark processing
- [x] Data cleaning and transformation
- [x] Partitioned Parquet storage
- [x] Data quality validation
- [x] Analytical aggregations
- [x] MariaDB / SQL implementation
- [x] Streamlit dashboard deployment
- [ ] Final strategic ROI model
- [ ] Final architecture diagram
- [ ] Technical-executive report
- [ ] Executive pitch
