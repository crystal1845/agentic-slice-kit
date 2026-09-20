# Simple Sensor-Reading Risk Flag Dashboard

Task 3 for CEG Tech Forum (CTF/RECUR/04). A Streamlit app that simulates a
sensor value every 1-2 seconds and flags it Low / Moderate / High.

## Run it

```bash
pip install -r sensor_dashboard/requirements.txt
streamlit run sensor_dashboard/app.py
```

## How it works

- `classify(value)` in `app.py` applies the threshold rules:
  - below 40 -> Low
  - 40-70 -> Moderate
  - above 70 -> High
- The sidebar lets you set the refresh interval (1-2s), how many past
  readings to keep, and a Start/Stop toggle.
- Each rerun generates one new random value (0-100), classifies it, and
  appends it to a history table.
