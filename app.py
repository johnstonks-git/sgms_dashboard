import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SGMS · Smart Greenhouse Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS: Dark sci-fi / biopunk aesthetic ---
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {
    background-color: #080d10 !important;
    color: #c8e6c9 !important;
    font-family: 'Inter', sans-serif;
  }
  .stApp { background: #080d10; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: #0d1a12; }
  ::-webkit-scrollbar-thumb { background: #1de076; border-radius: 2px; }

  /* ── Header block ── */
  .sgms-header {
    position: relative;
    padding: 3rem 2.5rem 2rem;
    margin-bottom: 2rem;
    background: linear-gradient(135deg, #0a1a0f 0%, #061008 100%);
    border: 1px solid #1a3a20;
    border-radius: 16px;
    overflow: hidden;
  }
  .sgms-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(29,224,118,0.12) 0%, transparent 70%);
    border-radius: 50%;
  }
  .sgms-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 40%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(0,200,255,0.07) 0%, transparent 70%);
    border-radius: 50%;
  }
  .sgms-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #1de076;
    text-shadow: 0 0 30px rgba(29,224,118,0.5);
    margin: 0;
  }
  .sgms-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #4a8a5a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.4rem;
  }
  .sgms-chapter {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #2a6a3a;
    margin-top: 0.8rem;
    border-left: 2px solid #1de076;
    padding-left: 0.8rem;
    letter-spacing: 1px;
  }
  .status-live {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #1de076;
    background: rgba(29,224,118,0.1);
    border: 1px solid rgba(29,224,118,0.3);
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 2px;
    margin-top: 1rem;
  }
  .status-dot {
    width: 7px; height: 7px;
    background: #1de076;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(29,224,118,0.6); }
    50% { opacity: 0.7; box-shadow: 0 0 0 5px rgba(29,224,118,0); }
  }

  /* ── KPI Cards ── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
  }
  .kpi-card {
    background: linear-gradient(145deg, #0d1a12, #081008);
    border: 1px solid #1a3a20;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.2s;
  }
  .kpi-card:hover {
    border-color: #1de076;
    transform: translateY(-2px);
  }
  .kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #1de076, transparent);
  }
  .kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    display: block;
  }
  .kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3a6a4a;
    margin-bottom: 0.4rem;
  }
  .kpi-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #1de076;
    line-height: 1;
    text-shadow: 0 0 20px rgba(29,224,118,0.4);
  }
  .kpi-unit {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #4a8a5a;
    margin-top: 0.2rem;
  }
  .kpi-accent-red::before { background: linear-gradient(90deg, transparent, #ff4757, transparent); }
  .kpi-accent-red .kpi-value { color: #ff6b81; text-shadow: 0 0 20px rgba(255,71,87,0.4); }
  .kpi-accent-blue::before { background: linear-gradient(90deg, transparent, #00c8ff, transparent); }
  .kpi-accent-blue .kpi-value { color: #00c8ff; text-shadow: 0 0 20px rgba(0,200,255,0.4); }
  .kpi-accent-amber::before { background: linear-gradient(90deg, transparent, #ffd32a, transparent); }
  .kpi-accent-amber .kpi-value { color: #ffd32a; text-shadow: 0 0 20px rgba(255,211,42,0.4); }

  /* ── Section headers ── */
  .section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #1de076;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1a3a20, transparent);
  }

  /* ── Chart wrapper ── */
  .chart-card {
    background: #0a1510;
    border: 1px solid #142a1a;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1.5rem;
  }

  /* ── Divider ── */
  .sgms-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1a3a20 30%, #1de076 50%, #1a3a20 70%, transparent);
    margin: 1.5rem 0;
  }

  /* ── Data table expander ── */
  .streamlit-expanderHeader {
    background: #0d1a12 !important;
    border: 1px solid #1a3a20 !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #4a8a5a !important;
    letter-spacing: 1px !important;
  }
  .streamlit-expanderContent {
    background: #080d10 !important;
    border: 1px solid #1a3a20 !important;
    border-top: none !important;
  }

  /* ── Hide default Streamlit elements ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1.5rem !important; max-width: 1400px; }
</style>
""", unsafe_allow_html=True)


# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("sgms_simulated_data.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

df = load_data()

# --- CALCULATE METRICS ---
interval_minutes = 5
fan_on_count = len(df[df['Fan_Status'] == 'ON'])
fan_uptime_hours = round((fan_on_count * interval_minutes) / 60, 2)
electricity_saved = round(24 - fan_uptime_hours, 2)
max_temp = df['Temperature_C'].max()
min_temp = df['Temperature_C'].min()
avg_humidity = round(df['Humidity_percent'].mean(), 1)
avg_light = round(df['Light_Level'].mean(), 0)


# ── HEADER ──────────────────────────────────────────────
st.markdown("""
<div class="sgms-header">
  <p class="sgms-title">⬡ SGMS</p>
  <p class="sgms-subtitle">Smart Greenhouse Monitoring System &nbsp;·&nbsp; Automated Logic Validation</p>
  <p class="sgms-chapter">▸ THESIS CHAPTER 4 &nbsp;·&nbsp; 24-HOUR SENSOR LOG ANALYSIS &nbsp;·&nbsp; SIMULATED ENVIRONMENT DATA</p>
  <div class="status-live"><span class="status-dot"></span> SYSTEM ACTIVE &nbsp;·&nbsp; ALL SENSORS NOMINAL</div>
</div>
""", unsafe_allow_html=True)


# ── KPI CARDS ───────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-accent-red">
    <span class="kpi-icon">🌡</span>
    <div class="kpi-label">Peak Temperature</div>
    <div class="kpi-value">{max_temp}</div>
    <div class="kpi-unit">°C · Maximum recorded</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">❄</span>
    <div class="kpi-label">Min Temperature</div>
    <div class="kpi-value">{min_temp}</div>
    <div class="kpi-unit">°C · Minimum recorded</div>
  </div>
  <div class="kpi-card kpi-accent-blue">
    <span class="kpi-icon">💨</span>
    <div class="kpi-label">Fan Uptime</div>
    <div class="kpi-value">{fan_uptime_hours}</div>
    <div class="kpi-unit">Hours · Active cooling</div>
  </div>
  <div class="kpi-card kpi-accent-amber">
    <span class="kpi-icon">⚡</span>
    <div class="kpi-label">Energy Saved</div>
    <div class="kpi-value">{electricity_saved}</div>
    <div class="kpi-unit">Hours · vs. 24/7 operation</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── PLOTLY THEME CONFIG ──────────────────────────────────
PLOTLY_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8,20,12,0.6)",
    font=dict(family="Space Mono, monospace", color="#4a8a5a", size=11),
    xaxis=dict(
        gridcolor="rgba(29,224,118,0.06)", linecolor="#1a3a20",
        tickfont=dict(color="#3a6a4a", size=10)
    ),
    yaxis=dict(
        gridcolor="rgba(29,224,118,0.06)", linecolor="#1a3a20",
        tickfont=dict(color="#3a6a4a", size=10)
    ),
    margin=dict(l=50, r=30, t=30, b=50),
    hoverlabel=dict(
        bgcolor="#0d1a12", bordercolor="#1de076",
        font=dict(family="Space Mono", color="#1de076", size=11)
    ),
    legend=dict(
        bgcolor="rgba(8,13,16,0.8)", bordercolor="#1a3a20",
        borderwidth=1, font=dict(color="#4a8a5a", size=10)
    )
)


# ── GRAPH 1: TEMPERATURE ─────────────────────────────────
st.markdown('<div class="section-header">🌡&nbsp; Temperature Curve &amp; Automated Cooling Logic</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)

fig_temp = go.Figure()

# Shaded fan-ON regions
fan_on_blocks = df[df['Fan_Status'] == 'ON']
for i, row in fan_on_blocks.iterrows():
    fig_temp.add_vrect(
        x0=row['Timestamp'],
        x1=row['Timestamp'] + pd.Timedelta(minutes=5),
        fillcolor="rgba(29,224,118,0.08)", layer="below", line_width=0
    )

# Temperature line with glow effect (double-layered)
fig_temp.add_trace(go.Scatter(
    x=df['Timestamp'], y=df['Temperature_C'],
    mode='lines', name='Ambient Temp (°C)',
    line=dict(color='rgba(255,107,129,0.25)', width=8),
    showlegend=False, hoverinfo='skip'
))
fig_temp.add_trace(go.Scatter(
    x=df['Timestamp'], y=df['Temperature_C'],
    mode='lines', name='Ambient Temp (°C)',
    line=dict(color='#ff6b81', width=2.5),
    fill='tozeroy', fillcolor='rgba(255,107,129,0.04)',
    hovertemplate='<b>%{y:.1f} °C</b><br>%{x|%H:%M}<extra></extra>'
))

# 30°C threshold
fig_temp.add_hline(
    y=30.0, line_dash="dot", line_color="rgba(255,71,87,0.7)", line_width=1.5,
    annotation_text="▸ 30.0 °C  FAN TRIGGER",
    annotation_font=dict(color="#ff4757", size=10, family="Space Mono"),
    annotation_position="top left"
)

# Fan ON indicator trace
fan_indicator = df.copy()
fan_indicator['Fan_Y'] = fan_indicator['Fan_Status'].apply(lambda x: 28.5 if x == 'ON' else None)
fig_temp.add_trace(go.Scatter(
    x=fan_indicator['Timestamp'], y=fan_indicator['Fan_Y'],
    mode='markers', name='Fan Active',
    marker=dict(color='#1de076', size=4, opacity=0.7,
                symbol='circle', line=dict(width=0)),
    hovertemplate='Fan ON<br>%{x|%H:%M}<extra></extra>'
))

fig_temp.update_layout(**PLOTLY_BASE,
    xaxis_title="TIME  (24-HOUR LOG)",
    yaxis_title="TEMPERATURE  (°C)",
    height=360,
    hovermode="x unified"
)
st.plotly_chart(fig_temp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── GRAPHS 2 & 3 ─────────────────────────────────────────
colA, colB = st.columns(2)

with colA:
    st.markdown('<div class="section-header">💧&nbsp; Relative Humidity</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(
        x=df['Timestamp'], y=df['Humidity_percent'],
        mode='lines', name='Humidity',
        line=dict(color='rgba(0,200,255,0.3)', width=7),
        showlegend=False, hoverinfo='skip'
    ))
    fig_hum.add_trace(go.Scatter(
        x=df['Timestamp'], y=df['Humidity_percent'],
        mode='lines', name='Humidity (%)',
        line=dict(color='#00c8ff', width=2),
        fill='tozeroy', fillcolor='rgba(0,200,255,0.05)',
        hovertemplate='<b>%{y:.1f}%</b><br>%{x|%H:%M}<extra></extra>'
    ))
    # Average line
    fig_hum.add_hline(
        y=avg_humidity, line_dash="dot", line_color="rgba(0,200,255,0.4)", line_width=1,
        annotation_text=f"avg {avg_humidity}%",
        annotation_font=dict(color="#00c8ff", size=9, family="Space Mono"),
        annotation_position="bottom right"
    )
    fig_hum.update_layout(**PLOTLY_BASE,
        xaxis_title="TIME", yaxis_title="HUMIDITY  (%)", height=300, showlegend=False
    )
    st.plotly_chart(fig_hum, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="section-header">☀&nbsp; Light Intensity (LDR Sensor)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    fig_light = go.Figure()
    fig_light.add_trace(go.Scatter(
        x=df['Timestamp'], y=df['Light_Level'],
        mode='lines', name='Light Level',
        line=dict(color='rgba(255,211,42,0.3)', width=7),
        showlegend=False, hoverinfo='skip'
    ))
    fig_light.add_trace(go.Scatter(
        x=df['Timestamp'], y=df['Light_Level'],
        mode='lines', name='Light Level',
        line=dict(color='#ffd32a', width=2),
        fill='tozeroy', fillcolor='rgba(255,211,42,0.06)',
        hovertemplate='<b>%{y:.0f}</b><br>%{x|%H:%M}<extra></extra>'
    ))
    fig_light.update_layout(**PLOTLY_BASE,
        xaxis_title="TIME", yaxis_title="LIGHT LEVEL  (ANALOG)", height=300, showlegend=False
    )
    st.plotly_chart(fig_light, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── GRAPH 4: FAN DUTY CYCLE BAR ──────────────────────────
st.markdown('<div class="section-header">⚙&nbsp; Fan Activation Pattern (Hourly)</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)

df['Hour'] = df['Timestamp'].dt.hour
hourly_fan = df.groupby('Hour')['Fan_Status'].apply(
    lambda x: (x == 'ON').sum() * interval_minutes / 60
).reset_index()
hourly_fan.columns = ['Hour', 'Fan_Hours']

fig_fan = go.Figure()
fig_fan.add_trace(go.Bar(
    x=hourly_fan['Hour'], y=hourly_fan['Fan_Hours'],
    marker=dict(
        color=hourly_fan['Fan_Hours'],
        colorscale=[[0, '#0d3a1a'], [0.5, '#1de076'], [1.0, '#7dffb3']],
        showscale=False,
        line=dict(color='rgba(29,224,118,0.3)', width=1)
    ),
    hovertemplate='Hour %{x}:00<br>Fan on for <b>%{y:.2f} hrs</b><extra></extra>'
))
fig_fan.update_layout(**PLOTLY_BASE,
    xaxis_title="HOUR OF DAY",
    yaxis_title="FAN ACTIVE  (HRS)",
    height=240,
    bargap=0.2
)
st.plotly_chart(fig_fan, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── DIVIDER ──────────────────────────────────────────────
st.markdown('<div class="sgms-divider"></div>', unsafe_allow_html=True)


# ── RAW DATA TABLE ───────────────────────────────────────
with st.expander("▸  VIEW RAW SENSOR DATASET"):
    st.dataframe(
        df.drop(columns=['Hour'], errors='ignore'),
        use_container_width=True,
        hide_index=True
    )

# ── FOOTER ───────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem; font-family: 'Space Mono', monospace;
     font-size: 0.6rem; color: #1a3a20; letter-spacing: 3px; text-transform: uppercase;">
  SGMS &nbsp;·&nbsp; Smart Greenhouse Monitoring System &nbsp;·&nbsp; Thesis Research Dashboard &nbsp;·&nbsp; Chapter 4
</div>
""", unsafe_allow_html=True)
