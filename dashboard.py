# dashboard.py
# Streamlit dashboard for visualizing BMS log data

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import time

#Load data
def load_data(uploaded_file=None):
  try:
    if uploaded_file
        df = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
  else:
      df = pd.read_csv('bms_log.csv'), parse_dates=['timestamp'])
  return df
except Exception as e:
    st.error(f"Failed to load data: {e}")
    return pd.DataFrame()

#Display fault status with colors
def status_color(status):
        return 'red' if "FAULT" in status else 'green'

# Streamlit config
st.set_page_config(page_title="Smart BMS Dashboard", layout="wide")
st.title("Smart BMS Diagnostic Dashboard")
# Side controls
st.sidebar.subheader("Controls")

if st.sidebar.button("Generate New BMS Data"):
    with st.spinner("Running BMS simulator..."):
        try:
            subprocess.run(["python", "bms_simulator.py"], timeout=5)
            time.sleep(1)   #slight delay to ensure CSV file finishes writing
            st.success("new BMS data generated.")
            except subprocess.TimeoutExpired:
                st.warning("Simulation timed out.")
            st.experimental_rerun() #refresh dashboard with new data

# Upload file
uploaded_file = st.file_uploader("Upload a BMS log file (.csv)", type="csv")
data = load_data(uploaded_file)

if not data.empty:
  #Optional filter by fault
  st.subheader("Filter Data")
  fault_options = ["All"] + sorted(set)[s.split(':')[1].strip() for s in data['status'] if "FAULT" in s]))
  unique_statuses = data['status'].unique().tolist()
  selected_fault = st.selectbox.("Filter by Fault Type", fault_options)

  if selected_status != "All":
      data = data[data['status'].str.contains(selected_fault)]

  # Line chart 

  st.subheader("BMS Time-Series Data")
  st.line_chart(data[['soc', 'voltage', 'current', 'temperature']])

  # Table with color-coded status
  st.subheader("Detailed Log Table")
  colored_status = data['status'].apply(lamba x: f"<span style='color:{status_color(x)}'>{x}</span>")
  styled_df = data.copy()
  styled_df['status'] = colored_status
  st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

  #Fault Summary
  st.subheader("Fault Summary")
  st.bar_chart(data['status'].value_counts()