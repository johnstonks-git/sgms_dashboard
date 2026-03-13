import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SGMS Thesis Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
    background-color: #f5f4f0 !important;
    color: #1a1a1a !important;
    font-family: 'DM Sans', sans-serif;
  }
  .stApp { background: #f5f4f0; }
  .block-container { padding-top: 2rem !important; max-width: 1300px; }
  #MainMenu, footer, header { visibility: hidden; }

  .dash-header {
    background: #1c2b1e;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }
  .dash-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.8rem;
    font-weight: 600;
    color: #ffffff;
    margin: 0 0 0.3rem 0;
  }
  .dash-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #7a9b7e;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }
  .dash-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #a8c5a0;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 6px 14px;
    border-radius: 6px;
    letter-spacing: 1px;
  }

  .kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
  }
  .kpi-card {
    background: #ffffff;
    border: 1px solid #e2e0da;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    border-top: 3px solid #1c2b1e;
  }
  .kpi-card.accent-red  { border-top-color: #c0392b; }
  .kpi-card.accent-blue { border-top-color: #2471a3; }
  .kpi-card.accent-gold { border-top-color: #b7950b; }
  .kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.5rem;
  }
  .kpi-value {
    font-size: 2rem;
    font-weight: 600;
    color: #1a1a1a;
    line-height: 1;
  }
  .kpi-unit {
    font-size: 0.78rem;
    color: #888;
    margin-top: 0.35rem;
  }

  .section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.6rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #e2e0da;
  }
  .chart-wrap {
    background: #ffffff;
    border: 1px solid #e2e0da;
    border-radius: 10px;
    padding: 1.2rem 1rem 0.5rem;
    margin-bottom: 1.5rem;
  }
  hr.sgms { border: none; border-top: 1px solid #e2e0da; margin: 1.5rem 0; }

  .streamlit-expanderHeader {
    background: #ffffff !important;
    border: 1px solid #e2e0da !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #555 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
  }
</style>
""", unsafe_allow_html=True)


# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("sgms_simulated_data.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

df = load_data()

interval_minutes  = 5
fan_on_count      = len(df[df['Fan_Status'] == 'ON'])
fan_uptime_hours  = round((fan_on_count * interval_minutes) / 60, 2)
electricity_saved = round(24 - fan_uptime_hours, 2)
max_temp          = df['Temperature_C'].max()
min_temp          = df['Temperature_C'].min()

# ── HEADER ────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
  <div>
    <div class="dash-title">🌱 Smart Greenhouse Monitoring System</div>
    <div class="dash-sub">Chapter 4 &nbsp;·&nbsp; 24-Hour Automated Logic Validation</div>
  </div>
  <div class="dash-badge">SIMULATION REPORT &nbsp;·&nbsp; {len(df):,} DATA POINTS</div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card accent-red">
    <div class="kpi-label">Max Temperature</div>
    <div class="kpi-value">{max_temp} °C</div>
    <div class="kpi-unit">Peak over 24 hours</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Min Temperature</div>
    <div class="kpi-value">{min_temp} °C</div>
    <div class="kpi-unit">Lowest over 24 hours</div>
  </div>
  <div class="kpi-card accent-blue">
    <div class="kpi-label">Fan Uptime</div>
    <div class="kpi-value">{fan_uptime_hours} hrs</div>
    <div class="kpi-unit">Active cooling time</div>
  </div>
  <div class="kpi-card accent-gold">
    <div class="kpi-label">Electricity Saved</div>
    <div class="kpi-value">{electricity_saved} hrs</div>
    <div class="kpi-unit">vs. 24/7 fan operation</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── SHARED LAYOUT ─────────────────────────────────────────
def base_layout(**kwargs):
    return dict(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#fafaf8",
        font=dict(family="DM Sans, sans-serif", color="#555", size=12),
        xaxis=dict(gridcolor="#eeede8", linecolor="#ddddd8", showline=True,
                   tickfont=dict(color="#888", size=11)),
        yaxis=dict(gridcolor="#eeede8", linecolor="#ddddd8", showline=True,
                   tickfont=dict(color="#888", size=11)),
        margin=dict(l=55, r=20, t=20, b=50),
        hoverlabel=dict(bgcolor="#1c2b1e", bordercolor="#1c2b1e",
                        font=dict(family="DM Mono, monospace", color="#fff", size=11)),
        legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#e2e0da",
                    borderwidth=1, font=dict(color="#555", size=11)),
        **kwargs
    )


# ── TEMPERATURE ───────────────────────────────────────────
st.markdown('<div class="section-label">Temperature Curve &amp; Cooling Logic</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)

fig_temp = go.Figure()
for _, row in df[df['Fan_Status'] == 'ON'].iterrows():
    fig_temp.add_vrect(
        x0=row['Timestamp'],
        x1=row['Timestamp'] + pd.Timedelta(minutes=5),
        fillcolor="rgba(36,113,163,0.07)", layer="below", line_width=0
    )
fig_temp.add_trace(go.Scatter(
    x=df['Timestamp'], y=df['Temperature_C'],
    mode='lines', name='Temperature (°C)',
    line=dict(color='#c0392b', width=2.5),
    fill='tozeroy', fillcolor='rgba(192,57,43,0.06)',
    hovertemplate='<b>%{y:.1f} °C</b>  —  %{x|%H:%M}<extra></extra>'
))
fig_temp.add_hline(
    y=30.0, line_dash="dash", line_color="#c0392b", line_width=1.2, opacity=0.5,
    annotation_text="30.0 °C  —  Fan Trigger",
    annotation_font=dict(color="#c0392b", size=11, family="DM Mono"),
    annotation_position="top left"
)
fig_temp.update_layout(**base_layout(
    xaxis_title="Time (24-Hour Log)", yaxis_title="Temperature (°C)",
    height=320, hovermode="x unified"
))
st.plotly_chart(fig_temp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── HUMIDITY & LIGHT ──────────────────────────────────────
colA, colB = st.columns(2)

with colA:
    st.markdown('<div class="section-label">Relative Humidity</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(
        x=df['Timestamp'], y=df['Humidity_percent'],
        mode='lines', line=dict(color='#2471a3', width=2.2),
        fill='tozeroy', fillcolor='rgba(36,113,163,0.07)',
        hovertemplate='<b>%{y:.1f}%</b>  —  %{x|%H:%M}<extra></extra>'
    ))
    fig_hum.update_layout(**base_layout(
        xaxis_title="Time", yaxis_title="Humidity (%)", height=280, showlegend=False
    ))
    st.plotly_chart(fig_hum, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="section-label">Light Intensity (LDR Sensor)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    fig_light = go.Figure()
    fig_light.add_trace(go.Scatter(
        x=df['Timestamp'], y=df['Light_Level'],
        mode='lines', line=dict(color='#b7950b', width=2.2),
        fill='tozeroy', fillcolor='rgba(183,149,11,0.07)',
        hovertemplate='<b>%{y:.0f}</b>  —  %{x|%H:%M}<extra></extra>'
    ))
    fig_light.update_layout(**base_layout(
        xaxis_title="Time", yaxis_title="Light Level (Analog)", height=280, showlegend=False
    ))
    st.plotly_chart(fig_light, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── FAN DUTY CYCLE ────────────────────────────────────────
st.markdown('<div class="section-label">Fan Activation — Hourly Breakdown</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)

df['Hour'] = df['Timestamp'].dt.hour
hourly_fan = df.groupby('Hour')['Fan_Status'].apply(
    lambda x: (x == 'ON').sum() * interval_minutes / 60
).reset_index()
hourly_fan.columns = ['Hour', 'Fan_Hours']

fig_fan = go.Figure()
fig_fan.add_trace(go.Bar(
    x=hourly_fan['Hour'], y=hourly_fan['Fan_Hours'],
    marker_color='#1c2b1e',
    hovertemplate='Hour %{x}:00 — <b>%{y:.2f} hrs</b><extra></extra>'
))
fig_fan.update_layout(**base_layout(
    xaxis_title="Hour of Day", yaxis_title="Fan Active (hrs)",
    height=240, bargap=0.25
))
st.plotly_chart(fig_fan, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── RAW DATA ──────────────────────────────────────────────
st.markdown('<hr class="sgms">', unsafe_allow_html=True)
with st.expander("View Raw Sensor Dataset"):
    st.dataframe(
        df.drop(columns=['Hour'], errors='ignore'),
        use_container_width=True,
        hide_index=True
    )
