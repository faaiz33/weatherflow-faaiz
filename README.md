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

**Author:** Mohammed Faaiz