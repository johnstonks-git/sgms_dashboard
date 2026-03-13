import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SGMS Thesis Dashboard", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Make sure this matches the exact name of your generated CSV file
    df = pd.read_csv("sgms_simulated_data.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

df = load_data()

# --- HEADER ---
st.title("🌱 Smart Greenhouse Monitoring System (SGMS)")
st.markdown("### Chapter 4: 24-Hour Automated Logic Validation")
st.markdown("---")

# --- CALCULATE METRICS (KPIs) ---
interval_minutes = 5
fan_on_count = len(df[df['Fan_Status'] == 'ON'])
fan_uptime_hours = round((fan_on_count * interval_minutes) / 60, 2)
electricity_saved = round(24 - fan_uptime_hours, 2)

max_temp = df['Temperature_C'].max()
min_temp = df['Temperature_C'].min()

# --- METRICS DISPLAY ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Max Temperature Recorded", f"{max_temp} °C")
col2.metric("Min Temperature Recorded", f"{min_temp} °C")
col3.metric("Total Fan Uptime", f"{fan_uptime_hours} Hours", delta="Active Cooling", delta_color="inverse")
col4.metric("Electricity Saved", f"{electricity_saved} Hours", delta="vs. 24/7 Fan", delta_color="normal")

st.markdown("---")

# --- GRAPH 1: TEMPERATURE & THRESHOLD ANALYSIS ---
st.subheader("🌡️ Temperature Curve vs. Automated Cooling Logic")

# Create a Plotly figure
fig_temp = go.Figure()

# Add the Temperature Line
fig_temp.add_trace(go.Scatter(
    x=df['Timestamp'], y=df['Temperature_C'],
    mode='lines', name='Ambient Temp (°C)', line=dict(color='#e74c3c', width=3)
))

# Add the 30.0 °C Critical Threshold Line (The "Thesis Magic" line)
fig_temp.add_hline(
    y=30.0, line_dash="dash", line_color="red", 
    annotation_text="30.0 °C Threshold (Fan ON)", annotation_position="top left"
)

# Highlight when the fan is ON using green shaded rectangles
fan_on_blocks = df[df['Fan_Status'] == 'ON']
for i, row in fan_on_blocks.iterrows():
    fig_temp.add_vrect(
        x0=row['Timestamp'], x1=row['Timestamp'] + pd.Timedelta(minutes=5),
        fillcolor="green", opacity=0.1, layer="below", line_width=0
    )

fig_temp.update_layout(
    xaxis_title="Time (24 Hours)", yaxis_title="Temperature (°C)",
    hovermode="x unified", template="plotly_white"
)
st.plotly_chart(fig_temp, use_container_width=True)

# --- LAYOUT FOR REMAINING GRAPHS ---
colA, colB = st.columns(2)

# --- GRAPH 2: HUMIDITY ---
with colA:
    st.subheader("💧 Relative Humidity")
    fig_hum = px.line(df, x='Timestamp', y='Humidity_percent', color_discrete_sequence=['#3498db'])
    fig_hum.update_layout(xaxis_title="Time", yaxis_title="Humidity (%)", template="plotly_white")
    st.plotly_chart(fig_hum, use_container_width=True)

# --- GRAPH 3: LIGHT LEVEL ---
with colB:
    st.subheader("☀️ Light Intensity (LDR)")
    fig_light = px.area(df, x='Timestamp', y='Light_Level', color_discrete_sequence=['#f1c40f'])
    fig_light.update_layout(xaxis_title="Time", yaxis_title="Light Level (Analog)", template="plotly_white")
    st.plotly_chart(fig_light, use_container_width=True)

# --- RAW DATA TABLE ---
with st.expander("View Raw Simulated Dataset"):
    st.dataframe(df, use_container_width=True)
