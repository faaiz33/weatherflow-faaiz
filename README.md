# WeatherFlow

A data pipeline that pulls live weather for five UK cities from a public API, saves the raw responses with a timestamp, cleans them, and loads them into a SQLite database that can be queried with SQL. 
The aim is to show, in the simplest form, the three steps every data pipeline performs: Extract the data, Transform it into a useful shape, and Load it where people can use it.

## How to set up

```bash
git clone <your-repo-url>
cd weatherflow-<yourname>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```


## How to run the pipeline

```bash
python etl_v1.py
```

This fetches hourly weather for five UK cities for yesterday and today (`past_days=1`, `forecast_days=1`), saves the raw JSON to `data/raw/<date>/`, and loads it into `weather.db`. No API key is needed. Running it again replaces existing rows for the same city and hour, so the row count stays the same.

Example output (last lines):
Rows loaded into SQLite: 240
ETL pipeline completed successfully!

**Tested on:** macOS (Apple Silicon), Python 3.13. The pinned packages in `requirements.txt` are macOS builds, so on other platforms you may need to adjust them.

**Author:** Mohammed Faaiz
