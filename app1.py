# app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(page_title="Family Health Tracker", page_icon="❤️", layout="wide")
st.title("👨‍👩‍👧‍👦 Family Health Tracker Dashboard")

# Function to simulate historical health data
def generate_history(days=7):
    data = {"Date": [], "Heart Rate": [], "Body Temp": [], "Activity Level": []}
    for i in range(days):
        data["Date"].append((datetime.now() - timedelta(days=days-i)).strftime("%Y-%m-%d"))
        data["Heart Rate"].append(random.randint(55, 120))
        data["Body Temp"].append(round(random.uniform(36, 38.5), 1))
        data["Activity Level"].append(random.randint(10, 100))
    return pd.DataFrame(data)

# Function to check for alerts
def check_alerts(hr, temp, activity):
    alerts = []
    if hr < 60 or hr > 100:
        alerts.append("⚠️ Heart Rate Abnormal")
    if temp < 36 or temp > 37.5:
        alerts.append("⚠️ Body Temperature Abnormal")
    if activity < 20:
        alerts.append("⚠️ Low Activity Level")
    return alerts

# Family members
family_members = ["Alice", "Bob", "Charlie", "Daisy"]

for member in family_members:
    st.subheader(f"{member}'s Health Data")
    
    # Simulate current readings (or use sliders to make interactive)
    hr = st.slider(f"❤️ Heart Rate (bpm) - {member}", 40, 140, random.randint(60, 100))
    temp = st.slider(f"🌡️ Body Temperature (°C) - {member}", 35.0, 40.0, round(random.uniform(36, 37), 1), 0.1)
    activity = st.slider(f"🚶 Activity Level (%) - {member}", 0, 100, random.randint(30, 80))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("❤️ Heart Rate (bpm)", hr)
    col2.metric("🌡️ Body Temp (°C)", temp)
    col3.metric("🚶 Activity Level (%)", activity)
    
    # Alerts
    alerts = check_alerts(hr, temp, activity)
    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("All readings normal ✅")
    
    # Doctors notes
    note = st.text_area(f"📝 Doctor's Note - {member}", placeholder="Enter notes here...")
    
    # Show historical graph
    st.markdown("**📊 Health History (last 7 days)**")
    df = generate_history()
    df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d"), hr, temp, activity]  # add today
    
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(df["Date"], df["Heart Rate"], marker='o', label='Heart Rate')
    ax.plot(df["Date"], df["Body Temp"], marker='o', label='Body Temp')
    ax.plot(df["Date"], df["Activity Level"], marker='o', label='Activity Level')
    ax.set_xticklabels(df["Date"], rotation=45)
    ax.set_ylabel("Values")
    ax.set_xlabel("Date")
    ax.legend()
    st.pyplot(fig)
    
    st.markdown("---")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")