Q1: How many hourly records does each city have, and what date range do they cover?
SELECT city, COUNT(*) AS rows, MIN(observed_at) AS first_hour, MAX(observed_at) AS last_hour
FROM weather_hourly
GROUP BY city;

Q2: What was the average temperature per city on 6 November 2026?
SELECT city, ROUND(AVG(temperature_c), 2) AS avg_temp_c
FROM weather_hourly
WHERE observed_at LIKE '2026-11-06%'
GROUP BY city;

Q3: Which five hours across all cities had the highest wind speed?
SELECT city, observed_at, wind_speed_kmh
FROM weather_hourly
ORDER BY wind_speed_kmh DESC
LIMIT 5;