# dashboard.py
# Streamlit dashboard for visualizing BMS log data

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import time

# Load data
def load_data(uploaded_file=None):
  try:
      if uploaded_file:
          df = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
      else:
          df = pd.read_csv('bms_log.csv', parse_dates=['timestamp'])
      return df
  except Exception as e:
    st.error(f"Failed to load data: {e}")
    return pd.DataFrame()


# Display fault status with colors
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
            st.success("New BMS data generated.")
        except subprocess.TimeoutExpired:
                st.warning("Simulation timed out.")
        st.session_state.fault_filter = "All"
        st.rerun() #refresh dashboard with new data

# Upload file
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
data = load_data(uploaded_file)

if not data.empty:
# Fault Summary
    st.subheader("Filter Data")
    fault_types = sorted(set([s.split(':')[1].strip() for s in data['status'] if "FAULT" in s]))
    fault_options = ["All"] + fault_types
    
    if 'fault_filter' not in st.session_state:
        st.session_state.fault_filter = "All"

    selected_fault = st.sidebar.selectbox(
        "Filter by Fault Type",
        fault_options,
        key='fault_filter'
    )

    if selected_fault != "All":
        data = data[data['status'].str.contains(selected_fault)]

# Summary card
    if selected_fault != "All":
        fault_count = len(data)
        st.success(f" Showing {fault_count} faults of type: **{selected_fault}**")
    else:
        st.info("Showing all BMS log entries")

# Recent Faults (if any faults are present)
    recent_fault = data[data['status'].str.contains("FAULT")].tail(1)

    if not recent_fault.empty:
        ts = recent_fault.iloc[0]['timestamp']
        fault_msg = recent_fault.iloc[0]['status'].split(':')[1].strip()
        st.warning(f" Most recent fault: **{fault_msg}** at `{ts}`")

# Export filtered data
    st.subheader("Download Filtered Data")
    export_format = st.selectbox("Select export format", ["CSV", "JSON"], key="export_format")

    if export_format =="CSV":
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='filtered_bms_log.csv',
            mime='text/csv',
        )
    elif export_format == "JSON":
        json_data = data.to_json(orient='records')
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name='filtered_bms_log.json',
            mime='application/json',
        )
        

# Line chart 
    st.subheader("BMS Time-Series Data")
    st.line_chart(data[['soc', 'voltage', 'current', 'temperature']])

# Table with color-coded status
    st.subheader("Detailed Log Table")
    colored_status = data['status'].apply(lambda x: f"<span style='color:{status_color(x)}'>{x}</span>")
    styled_df = data.copy()
    styled_df['status'] = colored_status
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

    st.subheader("Fault Summary")
    fault_counts = data['status'].value_counts()
    st.bar_chart(fault_counts)