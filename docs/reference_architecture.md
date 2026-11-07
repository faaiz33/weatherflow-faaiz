# Reference architecture: WeatherFlow

Labels: E = extract, T = transform, L = load. Each arrow is labelled from the code.

## Scheduled pipeline (Airflow, every hour)

```mermaid
flowchart LR
  A[Airflow DAG: hourly] -->|E: fetch_weather_data| API[WeatherAPI + OpenWeatherMap]
  API --> RAW[(data/raw: JSON)]
  RAW -->|T: process_weather_data.py, pandas| PROC[(data/processed: CSV)]
  PROC -->|L: generate_reports.py| REP[(data/reports: CSV + HTML)]
  RAW -->|L: dashboard reads, cached 5 min| DASH[Dashboard :8051]
```

## Separate path (not run by Airflow)

```mermaid
flowchart LR
  API2[Weather APIs] -->|E: producer.py| K[Kafka: weather-raw-data]
  K -->|consumer.py| X[No downstream step]
  SP[Spark: weather_processor.py] -.->|commented out in main| K
```