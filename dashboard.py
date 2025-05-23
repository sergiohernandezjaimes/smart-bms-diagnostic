# dashboard.py
# Streamlit dashboard for visualizing BMS log data

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Load data from CSV
def load_data(csv_file='bms_log.csv'):
  try:
    df = pd.read_csv(csv_file, parse_dates=['timestamp'])
    return df
  except FileNotFoundError:
    st.error("Log file not found. Please run the simulate first.")
    return pd.DataFrame()

#Display fault status with colors
def status_color(status):
  if "FAULT" in status:
      return 'red'
    return 'green'

# Main app
st.set_page_config(page_title="Smart BMS Dashboard", layout="wide")
st.title("🔋 Smart BMS Diagnostic Dashboard")

data = load_data()

if not data.empty:
st.subheader("📊 BMS Time-Series Data")
st.line_chart(data[['soc, 'voltage', 'current', 'temperature']])

st.subheader(📋 Detailed Log Table")
colored_status = data['status].apply(lamba x: f"<span style='color:{status_color(x)}'>{x}</span>")
styled_df = data.copy()
styled_df['status] = colored_status
st.write(styled_df.tohtml(escape=False), unsafe_allow_html=True)

st.subheader("⚠️ Fault Summary")
fault_counts = data['status'].value_counts()
st.bar_chart(faults_counts)
                    
