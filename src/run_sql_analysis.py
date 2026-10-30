
from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_DIR / "data" / "processed" / "credresolve.db"
SQL_PATH = PROJECT_DIR / "sql" / "01_analysis_queries.sql"
OUTPUT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DB_PATH.exists():
    raise FileNotFoundError("SQLite database not found.")

if not SQL_PATH.exists():
    raise FileNotFoundError("SQL query file not found.")

# Read SQL queries
sql_text = SQL_PATH.read_text(encoding="utf-8")
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

connection = sqlite3.connect(DB_PATH)

results = []

try:
    print("CREDRESOLVE SQL ANALYSIS")
    print("=" * 45)

    for number, query in enumerate(queries, start=1):
        result = pd.read_sql_query(query, connection)

        results.append({
            "query_number": number,
            "result": result
        })

        print(f"\nQUERY {number}")
        print("-" * 45)
        print(result.to_string(index=False))

    # Save all query outputs in one Excel workbook
    excel_path = OUTPUT_DIR / "sql_analysis_results.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for item in results:
            sheet_name = f"Query_{item['query_number']}"
            item["result"].to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    print("\nSQL ANALYSIS COMPLETED SUCCESSFULLY!")
    print("Results saved to:", excel_path)

finally:
    connection.close()
