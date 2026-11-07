import json
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_VARS = "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m,weather_code"
CITIES = [
    {"name": "London", "latitude": 51.5085, "longitude": -0.1257},
    {"name": "Manchester", "latitude": 53.48095, "longitude": -2.23743},
    {"name": "Birmingham", "latitude": 52.48142, "longitude": -1.89983},
    {"name": "Edinburgh", "latitude": 55.95206, "longitude": -3.19648},
    {"name": "Cardiff", "latitude": 51.48, "longitude": -3.18},
]

def fetch_city(city: dict) -> dict:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": HOURLY_VARS,
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Europe/London",
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def save_raw(city_name: str, payload: dict) -> Path:
    now = datetime.now(timezone.utc)
    folder = Path("data") / "raw" / now.strftime("%Y-%m-%d")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{city_name.lower()}_{now.strftime('%Y%m%dT%H%M%S')}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path

if __name__ == "__main__":
    for city in CITIES:
        try:
            payload = fetch_city(city)
            path = save_raw(city["name"], payload)
            records = len(payload["hourly"]["time"])
            print(f"{city['name']}: {records} hourly records saved to {path}")
        except requests.RequestException as e:
            print(f"{city['name']}: failed - {e}")
