#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

# Updated color palette with professional blue accent
COLOR_PALETTE = {
    "primary": "#2A2E45",       # Deep Space Blue
    "secondary": "#111111",     # Jet Black
    "accent1": "#242124",       # Raisin (Metrics & Titles)
    "accent2": "#FF2079",       # Neon Pink (Alerts/Highlights)
    "accent3": "#FF6C11",       # Safety Orange (Temperature Line)
    "complementary": "#50C878"  # Emerald Green (Positive Indicators / Pressure Line)
}

# Load the saved model
model = joblib.load(
    '/Altamash/Excelr code/PROJECTS/PROJECT_ ENERGY_PRODUCTION/energy_model.pkl'
)

# Configure page
st.set_page_config(
    page_title="Energy Production Predictor",
    page_icon="⚡",
    layout="wide"
)

# Styling function
def set_background_image(image_url):
    st.markdown(f"""
    <style>
    ::-webkit-scrollbar {{ width:10px; height:10px; }}
    ::-webkit-scrollbar-track {{ background:{COLOR_PALETTE['primary']}; }}
    ::-webkit-scrollbar-thumb {{ background:#FFF; border-radius:5px; }}
    ::-webkit-scrollbar-thumb:hover {{ background:#CCC; }}
    h1 {{ color:{COLOR_PALETTE['accent1']} !important; font-weight:700 !important; font-size:2.5rem !important; }}
    h2,h3 {{ color:{COLOR_PALETTE['accent1']} !important; border-bottom:2px solid {COLOR_PALETTE['accent1']}40; }}
    [data-testid="stSidebar"] h2 {{ color:#FFF !important; border-bottom:2px solid {COLOR_PALETTE['accent1']}; }}
    [data-testid="stSlider"] label {{ color:#FFF !important; font-weight:500; }}
    [data-testid="stAppViewContainer"] {{ background:url({image_url}); background-size:cover; background-attachment:fixed; }}
    [data-testid="stSidebar"] {{ background-color:{COLOR_PALETTE['primary']}CC; color:#EEE; }}
    .card {{ background-color:{COLOR_PALETTE['primary']}EE; border-radius:12px; padding:20px; box-shadow:0 6px 20px rgba(0,0,0,0.3); }}
    </style>
    """, unsafe_allow_html=True)

set_background_image("https://wallpapersmug.com/download/1366x768/46b360/lake-night-huts-lanterns.jpg")

# Header and banner
st.markdown("<h1>⚡ Energy Production Predictor ⚡</h1>", unsafe_allow_html=True)
st.image("https://cdn.pixabay.com/photo/2016/04/01/09/59/robot-1302102_1280.png", caption="Robo-Energy at your service!", use_column_width=True)

# Sidebar inputs
with st.sidebar:
    st.header("🔧 Input Parameters")
    temp = st.slider('🌡️ Temperature (°C)', -50.0, 100.0, 25.0, step=0.1)
    vac = st.slider('🌀 Exhaust Vacuum (cm Hg)', 0.0, 100.0, 50.0, step=0.1)
    ap = st.slider('🌬️ Ambient Pressure (mbar)', 0.0, 1100.0, 1013.0, step=0.1)
    rh = st.slider('💧 Relative Humidity (%)', 0.0, 100.0, 50.0, step=0.1)
    st.markdown("---")
    predict_btn = st.button('⚡ Predict')

# After prediction
if predict_btn:
    # Predict
    arr = np.array([[temp, vac, ap, rh]])
    pred = model.predict(arr)[0]

    # Metrics
    cols = st.columns(5)
    cols[0].metric("Temperature (°C)", f"{temp:.1f}")
    cols[1].metric("Exhaust Vacuum", f"{vac:.1f}")
    cols[2].metric("Ambient Pressure", f"{ap:.1f}")
    cols[3].metric("Humidity (%)", f"{rh:.1f}")
    cols[4].metric("Predicted Energy (MW)", f"{pred:.2f}")

    # Polar chart + legend
    fig_p = go.Figure(
        go.Barpolar(
            r=[temp, vac, ap, rh],
            theta=['Temp','Vac','Pres','Hum'],
            marker=dict(
                color=[temp, vac, ap, rh],
                colorscale=[COLOR_PALETTE['primary'], COLOR_PALETTE['complementary']],
                line=dict(color=COLOR_PALETTE['secondary'], width=2)
            )
        )
    )
    fig_p.update_layout(
        template='plotly_dark',
        polar=dict(radialaxis=dict(range=[0, max([temp, vac, ap, rh]) * 1.3])),
        showlegend=False
    )
    c1, c2 = st.columns([4,1])
    c1.plotly_chart(fig_p, use_container_width=True)
    legend_html = f"""
    <div style='font-size:14px;'>
      <div><span style='display:inline-block;width:12px;height:12px;background:{COLOR_PALETTE['primary']};margin-right:5px;'></span>Primary (Start)</div>
      <div><span style='display:inline-block;width:12px;height:12px;background:{COLOR_PALETTE['complementary']};margin-right:5px;'></span>Complementary (End)</div>
      <div><span style='display:inline-block;width:12px;height:12px;border:2px solid {COLOR_PALETTE['secondary']};margin-right:5px;'></span>Border</div>
    </div>"""
    c2.markdown(legend_html, unsafe_allow_html=True)

    # Gauge + legend
    fig_g = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=pred,
            delta={
                'reference': 100,
                'increasing': {'color': COLOR_PALETTE['complementary']},
                'decreasing': {'color': COLOR_PALETTE['accent2']}
            },
            gauge={
                'axis': {'range': [0, max(200, pred * 1.5)]},
                'bar': {'color': COLOR_PALETTE['accent2']},
                'steps': [
                    {'range': [0, pred * 0.4], 'color': COLOR_PALETTE['accent2']},
                    {'range': [pred * 0.4, pred * 0.8], 'color': COLOR_PALETTE['accent3']},
                    {'range': [pred * 0.8, max(200, pred * 1.5)], 'color': COLOR_PALETTE['complementary']}
                ]
            },
            title={'text': 'Energy (MW)', 'font': {'color': COLOR_PALETTE['accent1']}}
        )
    )
    fig_g.update_layout(template='plotly_dark')
    g1, g2 = st.columns([4,1])
    g1.plotly_chart(fig_g, use_container_width=True)
    legend_g = f"""
    <div style='font-size:14px;'>
      <div><span style='display:inline-block;width:12px;height:12px;background:{COLOR_PALETTE['accent2']};margin-right:5px;'></span>Bar & 0-40%</div>
      <div><span style='display:inline-block;width:12px;height:12px;background:{COLOR_PALETTE['accent3']};margin-right:5px;'></span>40-80%</div>
      <div><span style='display:inline-block;width:12px;height:12px;background:{COLOR_PALETTE['complementary']};margin-right:5px;'></span>80-100%</div>
      <div><span style='display:inline-block;width:12px;height:12px;border:2px solid {COLOR_PALETTE['accent1']};margin-right:5px;'></span>Threshold</div>
    </div>"""
    g2.markdown(legend_g, unsafe_allow_html=True)

    # Sensitivity analysis
    st.subheader("🔍 Sensitivity Analysis")
    factors = {
        'Temperature': COLOR_PALETTE['accent3'],
        'Vacuum': COLOR_PALETTE['secondary'],
        'Pressure': COLOR_PALETTE['complementary'],
        'Humidity': COLOR_PALETTE['accent2']
    }
    for fac, col in factors.items():
        arr = np.linspace(-50, 100, 150) if fac == 'Temperature' else (
            np.linspace(0, 100, 150) if fac == 'Vacuum' else (
            np.linspace(0, 1100, 150) if fac == 'Pressure' else np.linspace(0, 100, 150)
        ))
        sim = np.column_stack([
            arr if fac == 'Temperature' else np.full_like(arr, temp),
            arr if fac == 'Vacuum' else np.full_like(arr, vac),
            arr if fac == 'Pressure' else np.full_like(arr, ap),
            arr if fac == 'Humidity' else np.full_like(arr, rh)
        ])
        df = pd.DataFrame({fac: arr, 'Energy': model.predict(sim)})
        fig_s = px.line(
            df, x=fac, y='Energy', template='plotly_dark', color_discrete_sequence=[col]
        )
        s1, s2 = st.columns([4, 1])
        s1.plotly_chart(fig_s, use_container_width=True)
        legend_s = f"""
        <div style='font-size:14px;'><span style='display:inline-block;width:12px;height:12px;background:{col};margin-right:5px;'></span>{fac} Line ({col})</div>
        """
        s2.markdown(legend_s, unsafe_allow_html=True)

    # Scatter matrix + legend
    st.subheader("🔗 Feature Relationships & Prediction")
    df_samp = pd.DataFrame({
        k: np.random.uniform(-50, 100, 200) if k == 'Temperature' else np.random.uniform(0, 100, 200) if k == 'Vacuum' else np.random.uniform(0, 1100, 200) if k == 'Pressure' else np.random.uniform(0, 100, 200)
        for k in ['Temperature', 'Vacuum', 'Pressure', 'Humidity']
    })
    df_samp['Energy'] = model.predict(df_samp.values)
    fig_m = px.scatter_matrix(
        df_samp,
        dimensions=['Temperature', 'Vacuum', 'Pressure', 'Humidity'],
        color='Energy',
        color_continuous_scale=[COLOR_PALETTE['primary'], COLOR_PALETTE['complementary']],
        template='plotly_dark'
    )
    m1, m2 = st.columns([4, 1])
    m1.plotly_chart(fig_m, use_container_width=True)
    legend_m = f"""
    <div style='font-size:14px;'>
      <div><span style='display:inline-block;width:12px;height:12px;background:{COLOR_PALETTE['primary']};margin-right:5px;'></span>Low Energy</div>
      <div><span style='display:inline-block;width:12px;height:12px;background:{COLOR_PALETTE['complementary']};margin-right:5px;'></span>High Energy</div>
    </div>"""
    m2.markdown(legend_m, unsafe_allow_html=True)

    # Suggestions with typewriter effect
    st.subheader("💡 Suggestions")
    suggestions = [
        "Stay cool between 20–30°C for best performance.",
        "Maintain exhaust vacuum around 50–60 cm Hg.",
        "Keep ambient pressure within 1010–1020 mbar.",
        "Ensure humidity stays below 70%."
    ]
    placeholder = st.empty()
    text = ""
    for line in suggestions:
        for char in line:
            text += char
            placeholder.markdown(text)
            time.sleep(0.02)
        text += "\n"
        time.sleep(0.3)

    # Robo Tips and footer
    st.markdown("<h3 style='font-family:\"Comic Sans MS\",cursive;color:#000;'>💡 Robo Tips to Supercharge Energy ⚡</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background-color:#FFF8DC;border:2px dashed {COLOR_PALETTE['accent3']};padding:15px;border-radius:8px;">
      <ul>
        <li>❄️ <strong>Stay Cool:</strong> 20–30°C is ideal.</li>
        <li>🌪️ <strong>Vacuum Vibes:</strong> 50–60 cm Hg sweet spot.</li>
        <li>🌬️ <strong>Pressure Perfect:</strong> 1010–1020 mbar.</li>
        <li>💧 <strong>Humidity Hack:</strong> Below 70%.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='card' style='text-align:center;background:{COLOR_PALETTE['accent1']};color:{COLOR_PALETTE['primary']};'>Powered by ML ⚙️</div>", unsafe_allow_html=True)


# In[ ]:




