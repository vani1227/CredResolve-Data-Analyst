
from pathlib import Path
import sqlite3
import pandas as pd

# Project folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

# Create processed folder if it does not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database location
DB_PATH = PROCESSED_DIR / "credresolve.db"

# Load all dataset CSV files, excluding the data dictionary
csv_files = [
    file for file in RAW_DIR.glob("*.csv")
    if file.name.lower() != "data_dictionary.csv"
]

if not csv_files:
    raise FileNotFoundError(
        f"No dataset CSV files found in: {RAW_DIR}"
    )

print("CredResolve SQLite Database Loader")
print("----------------------------------")

connection = sqlite3.connect(DB_PATH)

try:
    for file in sorted(csv_files):
        table_name = file.stem.lower()

        df = pd.read_csv(file)

        # Load the CSV into a SQLite table
        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

        print(
            f"Loaded {table_name}: "
            f"{len(df):,} rows, {len(df.columns)} columns"
        )

    print("\nDatabase created successfully!")
    print("Database location:", DB_PATH)

finally:
    connection.close()
