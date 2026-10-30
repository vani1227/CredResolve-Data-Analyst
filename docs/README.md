# Synthetic Collections Analytics Dataset

Generated for a data-analyst challenge. Seed = 42.

The package contains 17 relational datasets and intentionally includes:
- Duplicates
- Missing values
- Conflicting timestamps
- UTC / Asia/Kolkata / Asia/Dubai timestamps
- Inconsistent identifiers
- Late-arriving events
- Schema versions
- Legacy disposition codes
- Duplicate payment references/events
- Overwritten-style status history
- Multiple agent identifiers
- Inconsistent campaign definitions

**Important:** Event-table row counts are intentionally different. Some tables exceed their nominal size because duplicate rows were injected.

---

# CredResolve – Collections Recovery Analytics

## Project Overview

This project analyzes collections and recovery operations using the 17 relational datasets provided in the challenge.

The objective is to understand payment recovery trends, outstanding balances, call performance, agent performance, campaign effectiveness and data quality issues.

## Project Objectives

- Analyze outstanding loan balances.
- Understand payment success and failure patterns.
- Evaluate call outcomes and agent performance.
- Compare collection campaign performance.
- Identify missing values and duplicate records.
- Build an interactive business intelligence dashboard.
- Provide data-driven business recommendations.

## Technology Stack

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- SQL (SQLite)
- Streamlit
- Jupyter Notebook

## Project Structure

```text
CredResolve_Data_Analyst/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
│   └── 01_data_inspection.ipynb
├── reports/
├── sql/
│   └── 01_analysis_queries.sql
├── src/
│   ├── load_data_to_sqlite.py
│   └── run_sql_analysis.py
├── README.md
└── requirements.txt
```

## Analysis Performed

1. Data inspection and quality assessment
2. Payment recovery analysis
3. Outstanding balance by risk segment
4. Call outcome and answer-rate analysis
5. Agent performance analysis
6. Campaign performance comparison
7. SQL-based business analysis
8. Interactive Streamlit dashboard

## Key Dataset Observations

- 30,000 account records
- 30,600 borrower records
- 25,500 payment records
- 91,350 call records
- 120 campaign records
- 30,000 agent records

The analysis identified missing borrower IDs, repeated payment IDs and other data quality issues.

## Dashboard

The Streamlit dashboard presents:
- Overall business performance
- Payment status distribution
- Monthly successful payment trends
- Outstanding amounts by risk segment
- Call outcomes and direction
- Campaign performance
- Data quality overview

Run the dashboard using:

```bash
streamlit run dashboard/app.py
```

## SQL Database

Create the SQLite database:

```bash
python src/load_data_to_sqlite.py
```

Run the SQL analysis:

```bash
python src/run_sql_analysis.py
```

The SQL results are exported to an Excel workbook in the reports folder.

## Data Quality Considerations

Exact duplicate payment rows are excluded from dashboard payment totals. Conflicting payment IDs still require investigation.

The available payment dates cover January to August 2026, with August representing a partial month. Therefore, month-on-month comparisons should account for the incomplete August period.

## Conclusion

This project demonstrates how Python, SQL and Streamlit can be used to analyze collections operations, identify data quality issues and communicate business performance through an interactive dashboard.