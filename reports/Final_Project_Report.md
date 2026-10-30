# Collections Recovery Analytics: Data Quality, Performance Analysis and Investment Optimization

## 1. Abstract

This project analyzes a synthetic collections recovery dataset containing 17 relational datasets. The main goal is to understand collection performance, identify data quality issues, analyze payment and call activities, and provide useful business recommendations.

Python, Pandas, SQL, SQLite, and Streamlit were used to clean, analyze, and visualize the data. A dashboard was developed to present important business metrics and trends.

## 2. Project Objectives

- Understand the structure of the collections datasets.
- Identify missing values, duplicate records, and inconsistent identifiers.
- Analyze account outstanding amounts and risk segments.
- Evaluate payment status and monthly payment trends.
- Analyze call outcomes and campaign performance.
- Create SQL queries for business analysis.
- Develop an interactive dashboard.
- Provide recommendations to improve collections performance.

## 3. Dataset Description

The project uses 17 CSV datasets related to collections operations.

The datasets include information about:

- Accounts and borrowers
- Agents and agent sessions
- Campaigns and daily targeting
- Calls and call attempts
- Call dispositions
- WhatsApp and SMS events
- Field visits
- Promises to pay
- Payments
- Vendor telephony
- Complaints
- Account status history

The dataset contains intentionally introduced data quality issues, including missing values, duplicate records, conflicting identifiers, and inconsistent timestamps.

## 4. Tools and Technologies Used

| Tool | Purpose |
|---|---|
| Python | Data analysis |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| SQL | Data analysis queries |
| SQLite | Database storage |
| Streamlit | Interactive dashboard |
| Jupyter Notebook | Exploratory data analysis |
| VS Code | Development environment |

## 5. Project Methodology

### Step 1: Data Inspection

Loaded the CSV files and examined their structure, number of rows and columns, data types, missing values, and duplicate records.

### Step 2: Data Quality Analysis

Identified missing values, exact duplicate records, repeated identifiers, and conflicting records.

### Step 3: Data Analysis

Performed exploratory analysis on accounts, payments, calls, campaigns, and risk segments.

### Step 4: SQL Analysis

Loaded all 17 datasets into SQLite and created SQL queries to analyze account details, payment performance, call outcomes, campaign performance, and data quality.

### Step 5: Dashboard Development

Created an interactive Streamlit dashboard to display important collection metrics and visualizations.

## 6. Data Quality Findings

The analysis identified the following issues:

| Dataset | Finding |
|---|---|
| Payments | 486 exact duplicate rows |
| Payments | 382 missing payment references |
| Payments | 500 payment IDs appear more than once |
| Payments | 14 repeated payment ID groups contain conflicting records |
| Accounts | 455 missing borrower IDs |
| Borrowers | 614 missing phone numbers |
| Borrowers | 895 missing email addresses |
| Calls | 1,827 missing agent IDs |

These findings show why data validation and cleaning are important before using the data for business decisions.

Repeated identifiers should not automatically be deleted because some records contain conflicting information and require further investigation.

## 7. Key Analysis Results

### 7.1 Account Analysis

- Total accounts: 30,000
- Total outstanding amount: approximately ₹1,048.90 crore
- Average days past due (DPD): approximately 56.51 days
- Average outstanding amount per account: approximately ₹3,49,635

### 7.2 Risk Segment Analysis

The accounts are divided into four risk segments:

- HIGH
- MEDIUM
- LOW
- NPA

The outstanding amounts are distributed across all four segments. This indicates that collection strategies should consider the risk category of each account.

### 7.3 Payment Analysis

The payment dataset contains 25,500 records.

Payment status distribution:

- SUCCESS: 17,880
- FAILED: 3,744
- PENDING: 2,592
- REVERSED: 1,284

The analysis also examined monthly successful payment trends and payment methods.

August contains data only through August 8, 2026, so it should not be directly compared with complete months.

### 7.4 Call Analysis

- Total call records: 91,350
- Answered calls: 18,146
- Overall call answer rate: approximately 19.86%

The analysis examined call direction and outcomes to understand calling performance.

### 7.5 Campaign Analysis

Campaign performance was evaluated using total calls and answered calls.

The highest answer rate among the analyzed campaigns was approximately 22.51%.

This analysis can help identify campaigns that may be worth studying for future collection activities.

## 8. Dashboard

An interactive dashboard was developed using Streamlit.

The dashboard displays:

- Total accounts
- Outstanding amount
- Successful payment amount
- Call answer rate
- Payment status distribution
- Monthly payment trends
- Risk segment distribution
- Call outcomes
- Campaign performance
- Data quality overview

The dashboard helps users understand collection performance through visual representations of the data.

## 9. SQL Analysis

All 17 CSV datasets were loaded into an SQLite database.

A collection of SQL queries was created to analyze:

1. Total accounts and outstanding amount
2. Outstanding amount by risk segment
3. Payment status distribution
4. Successful payments
5. Monthly payment trends
6. Payment methods
7. Call outcomes
8. Agent call performance
9. Campaign performance
10. Missing borrower IDs
11. Duplicate payment IDs
12. Account status distribution

The query results were exported to an Excel workbook.

## 10. Business Recommendations

1. Improve data validation to reduce missing and incorrect records.
2. Investigate conflicting payment IDs before removing or modifying records.
3. Improve borrower contact information to support collection activities.
4. Review call outcomes to identify opportunities to improve the answer rate.
5. Evaluate successful campaigns and use their findings to improve future campaigns.
6. Develop different collection strategies for different risk segments.
7. Monitor payment trends regularly and account for incomplete months when comparing performance.

## 11. Limitations

- The dataset is synthetic and does not represent actual customer or company operations.
- Some records contain missing and conflicting information.
- Repeated payment identifiers require additional investigation.
- August 2026 contains only partial-month data.
- The analysis is based on the available dataset and does not establish the actual causes of collection performance.

## 12. Conclusion

The project demonstrates how data analytics can support collections recovery operations.

By using Python, SQL, SQLite, and Streamlit, the project identifies data quality issues, analyzes account and payment information, evaluates call and campaign performance, and presents key findings through an interactive dashboard.

The analysis provides a foundation for better data quality management, improved collection strategies, and more informed business decisions.