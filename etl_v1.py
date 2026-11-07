
import requests
import pandas as pd
import sqlite3

from datetime import datetime, timezone
from extract import CITIES, fetch_city, save_raw


# 1. CREATE DATABASE TABLE

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS weather_hourly (
    city              TEXT    NOT NULL,
    observed_at       TEXT    NOT NULL,
    temperature_c     REAL,
    feels_like_c      REAL,
    humidity_pct      INTEGER,
    precipitation_mm  REAL,
    wind_speed_kmh    REAL,
    weather_code      INTEGER,
    ingested_at_utc   TEXT    NOT NULL,
    PRIMARY KEY (city, observed_at)
);
"""


# 2. EXTRACT DATA

def extract() -> list[tuple[str, dict]]:
    results = []

    for city in CITIES:
        try:
            payload = fetch_city(city)

            path = save_raw(city["name"], payload)

            print(f"{city['name']}: saved to {path}")

            results.append((city["name"], payload))

        except requests.RequestException as e:
            print(f"{city['name']}: failed - {e}")

    return results


# 3. FLATTEN DATA

def flatten(payload: dict, city_name: str) -> pd.DataFrame:
    df = pd.DataFrame(payload["hourly"])

    df["city"] = city_name

    return df


# 4. TRANSFORM DATA

def transform(results: list[tuple[str, dict]]) -> pd.DataFrame:
    frames = []

    for city_name, payload in results:
        df = flatten(payload, city_name)
        frames.append(df)

    if not frames:
        raise ValueError("No city data available for transformation.")

    df = pd.concat(frames, ignore_index=True)

    # Convert timestamps
    df["time"] = pd.to_datetime(df["time"])

    # Rename columns to match database schema
    df = df.rename(columns={
        "time": "observed_at",
        "temperature_2m": "temperature_c",
        "relative_humidity_2m": "humidity_pct",
        "apparent_temperature": "feels_like_c",
        "precipitation": "precipitation_mm",
        "wind_speed_10m": "wind_speed_kmh",
        "weather_code": "weather_code"
    })

    # Record when the data was ingested
    df["ingested_at_utc"] = datetime.now(timezone.utc)

    # Remove duplicate city-hour records
    df = df.drop_duplicates(
        subset=["city", "observed_at"],
        keep="last"
    )

    # Arrange columns to match SQLite table
    column_order = [
        "city",
        "observed_at",
        "temperature_c",
        "feels_like_c",
        "humidity_pct",
        "precipitation_mm",
        "wind_speed_kmh",
        "weather_code",
        "ingested_at_utc"
    ]

    df = df[column_order]

    return df


# 5. LOAD DATA INTO SQLITE

def load(df: pd.DataFrame, db_path: str = "weather.db") -> int:

    df = df.copy()

    # Convert timestamps into strings for SQLite
    df["observed_at"] = (
        pd.to_datetime(df["observed_at"])
        .dt.strftime("%Y-%m-%dT%H:%M")
    )

    df["ingested_at_utc"] = df["ingested_at_utc"].apply(
        lambda x: x.isoformat()
        if isinstance(x, datetime)
        else str(x)
    )

    columns = [
        "city",
        "observed_at",
        "temperature_c",
        "feels_like_c",
        "humidity_pct",
        "precipitation_mm",
        "wind_speed_kmh",
        "weather_code",
        "ingested_at_utc"
    ]

    # Convert DataFrame rows into SQLite-compatible tuples
    rows = [
        tuple(
            value.item() if hasattr(value, "item") else value
            for value in row
        )
        for row in df[columns].itertuples(index=False, name=None)
    ]

    placeholders = ", ".join(["?"] * len(columns))

    insert_sql = f"""
        INSERT OR REPLACE INTO weather_hourly
        ({", ".join(columns)})
        VALUES ({placeholders})
    """

    with sqlite3.connect(db_path) as conn:

        # Create the table if it does not exist
        conn.execute(CREATE_SQL)

        # Insert or update records
        conn.executemany(insert_sql, rows)

    return len(rows)


# 6. RUN THE COMPLETE ETL PIPELINE

def main():

    print("\nStarting weather ETL pipeline...\n")

    # Extract
    results = extract()

    # Transform
    weather_df = transform(results)

    # Load
    rows_loaded = load(weather_df)

    # Display results
    print("\nFirst five records:")
    print(weather_df.head())

    print("\nDataset shape:")
    print(weather_df.shape)

    print("\nRows loaded into SQLite:")
    print(rows_loaded)

    print("\nData types:")
    print(weather_df.dtypes)

    print("\nDuplicate records:")
    print(
        weather_df.duplicated(
            subset=["city", "observed_at"]
        ).sum()
    )

    print("\nMissing values:")
    print(weather_df.isna().sum())

    print("\nETL pipeline completed successfully!")


if __name__ == "__main__":
    main()
