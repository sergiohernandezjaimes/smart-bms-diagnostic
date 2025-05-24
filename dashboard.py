# dashboard.py
# Streamlit dashboard for visualizing BMS log data

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Load data from uploaded file or default CSV
def load_data(uploaded_file=None, default_file='bms_log.csv'):
  try:
    if uploaded_file is not None:
      df = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
  else:
      df = pd.read_csv(defualt_file, parse_dates=['timestamp'])
  return df
except FileNotFoundError:
    st.error("Log file not found. Please run the simulate or upload a log file.")
    return pd.DataFrame()

#Display fault status with colors
def status_color(status):
    if "FAULT" in status:
        return 'red'
    return 'green'

# Main app
st.set_page_config(page_title="Smart BMS Dashboard", layout="wide")
st.title("Smart BMS Diagnostic Dashboard")

st.sidebar.header("Data Options")
uploaded_file = st.sidebar.file_uploader("Upload a BMS log file (CSV)", type="csv")
data = load_data(uploaded_file)

if not data.empty:
  #Optional: Filter by fault type
  unique_statuses = data['status'].unique().tolist()
  selected_status = st.sidebar.selectbar.selectbox("Filter by Status", ["All"] + unique_statuses)

  if selected_status != "All":
      data = data[data['status'] == selected_status]

  st.subheader("📊 BMS Time-Series Data")
  st.line_chart(data[['soc', 'voltage', 'current', 'temperature']])

  st.subheader("📋 Detailed Log Table")
  colored_status = data['status'].apply(lamba x: f"<span style='color:{status_color(x)}'>{x}</span>")
  styled_df = data.copy()
  styled_df['status] = colored_status
  st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

  st.subheader("Fault Summary")
  fault_counts = data['status'].value_counts()
  st.bar_chart(faults_counts)
else:
  st.info("Please upload a log file or run the simulator to generate data.")

                    
