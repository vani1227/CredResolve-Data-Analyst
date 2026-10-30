
from pathlib import Path

import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CredResolve Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CredResolve – Collections Recovery Analytics")
st.caption(
    "Data quality | Payment recovery | Risk analysis | "
    "Call performance | Campaign analysis"
)

# ==========================================
# 2. LOAD DATASETS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "raw"


@st.cache_data
def load_data(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return pd.DataFrame()

    return pd.read_csv(file_path)


accounts = load_data("accounts.csv")
payments = load_data("payments.csv")
calls = load_data("calls.csv")
campaigns = load_data("campaigns.csv")
agents = load_data("agents.csv")

datasets = {
    "Accounts": accounts,
    "Payments": payments,
    "Calls": calls,
    "Campaigns": campaigns,
    "Agents": agents
}

missing_files = [
    name for name, df in datasets.items() if df.empty
]

if missing_files:
    st.error("Some required datasets are missing or empty.")
    st.write("Please check the data/raw folder:", missing_files)
    st.stop()


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def find_column(df, possible_names):
    """Find a column without depending on capitalization."""
    lookup = {col.lower(): col for col in df.columns}

    for name in possible_names:
        if name.lower() in lookup:
            return lookup[name.lower()]

    return None


def money_in_crore(value):
    return f"₹{value / 10000000:,.2f} Cr"


# ==========================================
# 4. PREPARE PAYMENT DATA
# ==========================================

payments = payments.drop_duplicates().copy()

payment_status_col = find_column(
    payments,
    [
        "status",
        "payment_status",
        "payment_status_code",
        "transaction_status",
        "payment_state"
    ]
)

amount_col = find_column(
    payments,
    ["amount", "payment_amount", "transaction_amount"]
)

payment_date_col = find_column(
    payments,
    ["event_at", "payment_date", "created_at", "transaction_date"]
)

if payment_status_col is None:
    st.error("Payment status column could not be identified.")
    st.write("Available payment columns:", payments.columns.tolist())
    st.stop()

if amount_col is None:
    st.error("Payment amount column could not be identified.")
    st.write("Available payment columns:", payments.columns.tolist())
    st.stop()

payments[amount_col] = pd.to_numeric(
    payments[amount_col], errors="coerce"
)

successful_payments = payments[
    payments[payment_status_col]
    .astype(str)
    .str.strip()
    .str.upper()
    == "SUCCESS"
].copy()

if payment_date_col:
    successful_payments[payment_date_col] = pd.to_datetime(
        successful_payments[payment_date_col],
        errors="coerce",
        utc=True
    )


# ==========================================
# 5. PREPARE CALL DATA
# ==========================================

call_status_col = find_column(
    calls,
    ["call_status", "status"]
)

call_direction_col = find_column(
    calls,
    ["direction", "call_direction"]
)

call_id_col = find_column(
    calls,
    ["call_id"]
)

if call_status_col is None:
    st.error("Call status column could not be identified.")
    st.write("Available call columns:", calls.columns.tolist())
    st.stop()

total_calls = len(calls)

answered_calls = (
    calls[call_status_col]
    .astype(str)
    .str.strip()
    .str.upper()
    == "ANSWERED"
).sum()

answer_rate = (
    answered_calls / total_calls * 100
    if total_calls > 0 else 0
)


# ==========================================
# 6. KPI METRICS
# ==========================================

total_accounts = len(accounts)

outstanding_col = find_column(
    accounts,
    ["outstanding_amount"]
)

if outstanding_col is None:
    st.error("Outstanding amount column not found.")
    st.stop()

accounts[outstanding_col] = pd.to_numeric(
    accounts[outstanding_col], errors="coerce"
)

total_outstanding = accounts[outstanding_col].sum()

total_recovered = successful_payments[amount_col].sum()

st.subheader("Overall Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Accounts",
    f"{total_accounts:,}"
)

col2.metric(
    "Outstanding Amount",
    money_in_crore(total_outstanding)
)

col3.metric(
    "Successful Payment Amount",
    money_in_crore(total_recovered)
)

col4.metric(
    "Call Answer Rate",
    f"{answer_rate:.2f}%"
)

st.divider()


# ==========================================
# 7. PAYMENT PERFORMANCE
# ==========================================

st.header("1. Payment Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Payment Status Distribution")

    payment_status = (
        payments[payment_status_col]
        .fillna("Missing")
        .astype(str)
        .value_counts()
    )

    st.bar_chart(payment_status)

with col2:
    st.subheader("Monthly Successful Payments")

    if payment_date_col:
        monthly_data = successful_payments.dropna(
            subset=[payment_date_col]
        ).copy()

        if not monthly_data.empty:
            monthly_data["month"] = (
                monthly_data[payment_date_col]
                .dt.strftime("%Y-%m")
            )

            monthly_recovery = (
                monthly_data.groupby("month")[amount_col]
                .sum()
                .sort_index()
            )

            st.line_chart(monthly_recovery)
        else:
            st.info("No valid payment dates are available.")
    else:
        st.info("Payment date column is unavailable.")

st.divider()


# ==========================================
# 8. RISK ANALYSIS
# ==========================================

st.header("2. Risk Segment Analysis")

risk_col = find_column(
    accounts,
    ["risk_segment"]
)

if risk_col:
    risk_summary = (
        accounts.groupby(risk_col)[outstanding_col]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("Outstanding Amount by Risk Segment")
    st.bar_chart(risk_summary)

    risk_accounts = (
        accounts.groupby(risk_col)
        .size()
        .reset_index(name="Number of Accounts")
    )

    st.subheader("Accounts by Risk Segment")
    st.dataframe(risk_accounts, use_container_width=True)
else:
    st.info("Risk segment column is unavailable.")

st.divider()


# ==========================================
# 9. CALL PERFORMANCE
# ==========================================

st.header("3. Call Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Call Outcomes")

    call_outcomes = (
        calls[call_status_col]
        .fillna("Missing")
        .astype(str)
        .value_counts()
    )

    st.bar_chart(call_outcomes)

with col2:
    st.subheader("Call Direction")

    if call_direction_col:
        direction_summary = (
            calls[call_direction_col]
            .fillna("Missing")
            .astype(str)
            .value_counts()
        )

        st.bar_chart(direction_summary)
    else:
        st.info("Call direction column is unavailable.")

st.metric("Answered Calls", f"{answered_calls:,}")
st.metric("Total Calls", f"{total_calls:,}")

st.divider()


# ==========================================
# 10. CAMPAIGN PERFORMANCE
# ==========================================

st.header("4. Campaign Performance")

campaign_id_col = find_column(calls, ["campaign_id"])
campaign_master_id_col = find_column(campaigns, ["campaign_id"])

if campaign_id_col and campaign_master_id_col:

    campaign_calls = (
        calls.groupby(campaign_id_col)
        .agg(
            total_calls=(call_status_col, "size"),
            answered_calls=(
                call_status_col,
                lambda x: (
                    x.astype(str).str.upper() == "ANSWERED"
                ).sum()
            )
        )
        .reset_index()
    )

    campaign_calls["answer_rate_pct"] = (
        campaign_calls["answered_calls"]
        / campaign_calls["total_calls"] * 100
    )

    campaign_report = campaign_calls.merge(
        campaigns,
        left_on=campaign_id_col,
        right_on=campaign_master_id_col,
        how="left"
    )

    st.subheader("Campaign Answer Rate")

    st.bar_chart(
        campaign_report.set_index(campaign_id_col)[
            "answer_rate_pct"
        ].sort_values(ascending=False).head(15)
    )

    st.subheader("Campaign Details")

    st.dataframe(
        campaign_report.sort_values(
            "answer_rate_pct",
            ascending=False
        ),
        use_container_width=True
    )

else:
    st.info("Campaign ID column is unavailable.")

st.divider()


# ==========================================
# 11. DATA QUALITY OVERVIEW
# ==========================================

st.header("5. Data Quality Overview")

quality_rows = []

for name, df in datasets.items():
    quality_rows.append({
        "Dataset": name,
        "Total Rows": len(df),
        "Total Columns": len(df.columns),
        "Missing Values": int(df.isna().sum().sum()),
        "Exact Duplicate Rows": int(df.duplicated().sum())
    })

quality_report = pd.DataFrame(quality_rows)

st.dataframe(
    quality_report,
    use_container_width=True
)

st.divider()


# ==========================================
# 12. PROJECT SUMMARY
# ==========================================

st.header("6. Project Summary")

st.write(
    """
    This dashboard presents an overview of collections operations
    using account, payment, call, campaign and agent datasets.

    The analysis covers:
    - Outstanding balances and risk segments
    - Successful payment amounts and monthly trends
    - Call outcomes and answer rates
    - Campaign performance
    - Missing values and duplicate records
    """
)

st.warning(
    """
    Data interpretation note: Exact duplicate payment rows are excluded
    from the displayed payment totals. Conflicting records with the same
    payment ID may still require investigation. Payment totals should
    therefore be treated as preliminary, not as fully reconciled figures.
    """
)

st.success("CredResolve Analytics dashboard loaded successfully.")
