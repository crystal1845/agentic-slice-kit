"""
Task 3 - Simple Sensor-Reading Risk Flag Dashboard
CEG Tech Forum - CTF/RECUR/04

What this app does:
- Every 1-2 seconds, it makes up a random sensor value (0-100).
- It checks the value against threshold rules and gives it a flag:
    below 40      -> Low
    40 to 70      -> Moderate
    above 70      -> High
- It shows the latest reading, the flag, and a short history on screen.
"""

import random
import time
from datetime import datetime

import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Sensor Risk Dashboard", page_icon="📡")
st.title("📡 Simple Sensor-Reading Risk Flag Dashboard")
st.caption("Generates a simulated sensor reading every 1-2 seconds and flags it Low / Moderate / High.")


# ---------- Step 2: classify a value into a flag ----------
def classify(value: float) -> str:
    """Turn a 0-100 sensor value into a Low / Moderate / High flag."""
    if value < 40:
        return "Low"
    elif value <= 70:
        return "Moderate"
    else:
        return "High"


# Colour + emoji shown next to each flag, just to make it easier to read.
FLAG_STYLE = {
    "Low": ("🟢", "green"),
    "Moderate": ("🟡", "orange"),
    "High": ("🔴", "red"),
}

# ---------- Sidebar controls ----------
st.sidebar.header("Settings")
refresh_seconds = st.sidebar.slider("Refresh interval (seconds)", 1.0, 2.0, 1.5, 0.5)
max_history = st.sidebar.slider("Readings to keep in history", 5, 50, 15)
running = st.sidebar.toggle("Start / Stop", value=True)

# ---------- Keep history between reruns ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Placeholders that we will keep overwriting ----------
reading_box = st.empty()
history_box = st.empty()

if running:
    # Step 1: make up a new sensor reading (0-100)
    value = round(random.uniform(0, 100), 1)
    flag = classify(value)
    timestamp = datetime.now().strftime("%H:%M:%S")

    # save it to history (newest first)
    st.session_state.history.insert(0, {"time": timestamp, "value": value, "flag": flag})
    st.session_state.history = st.session_state.history[:max_history]

    # ---------- Show the current reading ----------
    emoji, color = FLAG_STYLE[flag]
    with reading_box.container():
        st.metric("Latest sensor value", value)
        st.markdown(f"### {emoji} Status: :{color}[{flag}]")
        st.progress(min(int(value), 100) / 100)

    # ---------- Show recent history as a table ----------
    with history_box.container():
        st.subheader("Recent readings")
        st.table(st.session_state.history)

    # wait a bit, then rerun the script to get a fresh reading
    time.sleep(refresh_seconds)
    st.rerun()
else:
    st.info("Toggle 'Start / Stop' in the sidebar to begin generating readings.")
