# Data dictionary: WeatherFlow hourly weather

- **Source:** Open-Meteo forecast API (https://api.open-meteo.com/v1/forecast)
- **Licence:** CC BY 4.0
- **Refresh:** hourly, via the Airflow DAG, or manually by running `extract.py`
- **Grain:** one row per city per hour
- **Coverage:** 240 rows (5 cities × 48 hours) from 6 to 7 November 2026, after duplicates are removed

| Column | Type | Unit | Description | Example | Nullable? | Source |
|---|---|---|---|---|---|---|
| `time` | Text (datetime after `pd.to_datetime`) | Europe/London local time | The start of the hour the record covers. | `2026-11-06T00:00` | No | Open-Meteo `hourly.time` |
| `temperature_2m` | Float | °C | Modelled air temperature at 2 metres above ground level. | 9.1 | No | Open-Meteo `hourly.temperature_2m` |
| `relative_humidity_2m` | Integer | % | Moisture in the air as a percentage of the maximum the air can hold at that temperature. | 77 | No | Open-Meteo `hourly.relative_humidity_2m` |
| `apparent_temperature` | Float | °C | Feels-like temperature, accounting for wind chill, humidity and solar radiation. | 7.0 | No | Open-Meteo `hourly.apparent_temperature` |
| `precipitation` | Float | mm | Modelled total precipitation (rain, showers and snow) for the hour starting at `time`. | 0.0 | No | Open-Meteo `hourly.precipitation` |
| `wind_speed_10m` | Float | km/h | Modelled wind speed at 10 metres above ground level. | 6.1 | No | Open-Meteo `hourly.wind_speed_10m` |
| `weather_code` | Integer | WMO code | Modelled weather condition, using WMO weather interpretation codes. | 3 | No | Open-Meteo `hourly.weather_code` |
| `city` | Text | None | City the record belongs to. | London | No | Added by `extract.py` from the file name |
| `latitude` | Float | Degrees | Latitude of the grid point the API used, not the requested coordinates. | 51.51147 | No | Open-Meteo API response |
| `longitude` | Float | Degrees | Longitude of the grid point the API used, not the requested coordinates. | -0.130783 | No | Open-Meteo API response |