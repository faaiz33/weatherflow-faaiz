# Reference critique: WeatherFlow

## Component table

| Component | Tool used | What it does in this project | Batch or streaming? |
|-----------|-----------|------------------------------|---------------------|
| Data source | WeatherAPI and OpenWeatherMap | A Python script (`scripts/weather_api.py`) calls both websites for each of the cities. It gets current weather for each one. | Batch (it runs on a schedule, not continuously) |
| Message broker | Kafka | Used only by the separate producer and consumer scripts (`kafka/scripts/`). The producer sends to `weather-raw-data`, and `scripts/config.py` and the Spark file use `weather-raw`. The hourly Airflow pipeline doesn't send or read any messages. | Streaming in design, but not part of the scheduled run |
| Processing | pandas (`scripts/process_weather_data.py`) | Reads the raw weather data, reshapes it into a table, and writes a CSV. Run by Airflow every hour. The docstring says it replaces Spark. | Batch |
| Orchestration | Airflow | Runs the pipeline every hour (`weather_pipeline_dag.py`, line 65). Its tasks are: fetch the weather data (PythonOperator), create folders, wait on a sensor, process the data, generate reports, and clean up (BashOperators). | Batch, scheduled hourly |
| Storage | Local folders (files, not a database): `data/raw`, `data/processed`, `data/reports`; PostgreSQL for Airflow metadata | Raw data is saved to `/opt/airflow/data/raw`. `process_weather_data.py` writes a CSV to `/opt/airflow/data/processed`. Reports are CSV and HTML files in `data/reports`. `.gitignore` keeps these out of Git. PostgreSQL 13 (`docker-compose.yml`) stores Airflow's metadata. | Batch |
| Serving | Flask/Dash web app (`dashboard/app.py`) | Reads the raw JSON files in `data/raw` (`data_access.py`, lines 191 and 293), not the processed CSV. Caches results for 5 minutes. Shows the data as charts on port 8051. A second dashboard (`streamlit_dashboard.py`) runs on port 8501 and calls WeatherAPI directly. | On demand (reads when a page loads, cached 5 min) |
| Packaging | Docker Compose | Starts all the services (Kafka, Spark, Airflow, the dashboard) with one command. | Not applicable |