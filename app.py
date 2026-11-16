# =========================================
# IMPORT LIBRARIES
# =========================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import joblib

# =========================================
# PAGE TITLE
# =========================================

st.set_page_config(
    page_title="Threat Classification Dashboard",
    layout="wide"
)

st.title("THREAT CLASSIFICATION DASHBOARD")

st.write("Machine Learning Based Cyber Threat Detection System")

st.markdown("---")

# =========================================
# LOAD MODEL
# =========================================

model = joblib.load("best_model.pkl")

scaler = joblib.load("scaler.pkl")

# =========================================
# SIDEBAR INPUTS
# =========================================

st.sidebar.header("ENTER NETWORK VALUES")

flow_packets = st.sidebar.number_input(
    "Flow Packets/s",
    value=100.0
)

flow_iat = st.sidebar.number_input(
    "Flow IAT Mean",
    value=50.0
)

packet_length = st.sidebar.number_input(
    "Packet Length Mean",
    value=200.0
)

avg_packet = st.sidebar.number_input(
    "Average Packet Size",
    value=300.0
)

flow_bytes = st.sidebar.number_input(
    "Flow Bytes/s",
    value=400.0
)

# =========================================
# INPUT DATA
# =========================================

input_data = np.array([[
    flow_packets,
    flow_iat,
    packet_length,
    avg_packet,
    flow_bytes
]])

# =========================================
# SCALE DATA
# =========================================

scaled_data = scaler.transform(input_data)

# =========================================
# PREDICT BUTTON
# =========================================

if st.button("PREDICT THREAT"):

    prediction = model.predict(scaled_data)

    st.subheader("PREDICTION RESULT")

    if prediction[0] == 1:
        st.error("ATTACK DETECTED")
    else:
        st.success("BENIGN TRAFFIC")

    # =====================================
    # DOWNLOAD REPORT
    # =====================================

    report = f"""
THREAT CLASSIFICATION REPORT
============================

Flow Packets/s      : {flow_packets}
Flow IAT Mean       : {flow_iat}
Packet Length Mean  : {packet_length}
Average Packet Size : {avg_packet}
Flow Bytes/s        : {flow_bytes}

Prediction Result   : {"ATTACK DETECTED" if prediction[0] == 1 else "BENIGN TRAFFIC"}
"""

    st.download_button(
        label="DOWNLOAD REPORT",
        data=report,
        file_name="threat_report.txt",
        mime="text/plain"
    )
# =====================================
# VISUALIZATION
# =====================================

# =====================================
# VISUALIZATION
# =====================================

st.subheader("INPUT FEATURE VISUALIZATION")

features = [
    "Flow Packets/s",
    "Flow IAT Mean",
    "Packet Length Mean",
    "Average Packet Size",
    "Flow Bytes/s"
]

values = [
    flow_packets,
    flow_iat,
    packet_length,
    avg_packet,
    flow_bytes
]

fig, ax = plt.subplots(figsize=(10,5))

ax.bar(features, values)

plt.xticks(rotation=15)

plt.title("Network Traffic Features")

st.pyplot(fig)
# =====================================
# PIE CHART
# =====================================

st.subheader("FEATURE DISTRIBUTION")

fig2, ax2 = plt.subplots(figsize=(6,6))

ax2.pie(
    values,
    labels=features,
    autopct='%1.1f%%'
)

st.pyplot(fig2)

# =====================================
# LINE CHART
# =====================================

st.subheader("FEATURE TREND")

fig3, ax3 = plt.subplots(figsize=(10,5))

ax3.plot(features, values, marker='o')

plt.xticks(rotation=15)

st.pyplot(fig3)

# =========================================
# FOOTER
# =========================================

st.markdown("---")
col1, col2, col3 = st.columns(3)

col1.metric("Flow Packets/s", flow_packets)
col2.metric("Packet Length", packet_length)
col3.metric("Flow Bytes/s", flow_bytes)
st.write("Interactive Dashboard for Threat Classification")