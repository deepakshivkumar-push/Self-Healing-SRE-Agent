import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------
# Page Configuration (MUST be first Streamlit command)
# -----------------------------
st.set_page_config(
    page_title="SRE Self-Healing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Auto Refresh (Streamlit-safe)
# -----------------------------
REFRESH_DEFAULT = 2
st.autorefresh(interval=REFRESH_DEFAULT * 1000, key="auto_refresh")

# -----------------------------
# Custom CSS (Dark Mode)
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.stMetric {
    background-color: #262730;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #2e3039;
}
h1 {
    color: #00ff88;
    font-weight: 700;
    text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
}
.status-active {
    background-color: #00ff88;
    color: #000;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: bold;
}
.status-healing {
    background-color: #ffaa00;
    color: #000;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("# 🛡️ SRE SELF-HEALING DASHBOARD")
st.markdown("### Real-Time Intelligent Monitoring System")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    st.markdown("---")

    status_placeholder = st.empty()
    status_placeholder.markdown("<span class='status-active'>🟢 ACTIVE</span>", unsafe_allow_html=True)

    st.markdown("### 🧠 ML Model")
    st.info("Isolation Forest\nUnsupervised Anomaly Detection")

    st.markdown("---")

    filter_option = st.radio(
        "Log Filter",
        ["All Events", "ML Anomalies Only", "Database Errors Only", "CPU Issues Only"],
        index=0
    )

    st.markdown("---")
    refresh_rate = st.slider("Refresh Rate (seconds)", 1, 10, REFRESH_DEFAULT)

# -----------------------------
# Session State
# -----------------------------
if "last_incident_count" not in st.session_state:
    st.session_state.last_incident_count = 0

# -----------------------------
# Main Logic
# -----------------------------
placeholder = st.empty()

LOG_FILE = "healed_incidents.log"

with placeholder.container():

    if not os.path.exists(LOG_FILE):
        st.warning("⏳ Waiting for incidents...")
        st.info("The self-healing agent will log events here.")
    else:
        try:
            df = pd.read_csv(
                LOG_FILE,
                sep=",",
                names=["Timestamp", "Event"],
                engine="python"
            )

            df["Timestamp"] = pd.to_datetime(
                df["Timestamp"].str.strip("[]"),
                errors="coerce"
            )
            df.dropna(subset=["Timestamp"], inplace=True)
            df["Event"] = df["Event"].astype(str)

            # -----------------------------
            # Filtering
            # -----------------------------
            filtered_df = df.copy()

            if filter_option == "ML Anomalies Only":
                filtered_df = df[df["Event"].str.contains("scaling|frequency", case=False, na=False)]
            elif filter_option == "Database Errors Only":
                filtered_df = df[df["Event"].str.contains("database", case=False, na=False)]
            elif filter_option == "CPU Issues Only":
                filtered_df = df[df["Event"].str.contains("cpu|temporary", case=False, na=False)]

            # -----------------------------
            # Status Update
            # -----------------------------
            if len(df) > st.session_state.last_incident_count:
                st.toast("🚨 Incident detected and auto-healed!", icon="✅")
                status_placeholder.markdown(
                    "<span class='status-healing'>🟡 HEALING</span>",
                    unsafe_allow_html=True
                )
                st.session_state.last_incident_count = len(df)
            else:
                status_placeholder.markdown(
                    "<span class='status-active'>🟢 ACTIVE</span>",
                    unsafe_allow_html=True
                )

            # -----------------------------
            # Metrics
            # -----------------------------
            col1, col2, col3, col4 = st.columns(4)

            db_fixes = df[df["Event"].str.contains("database", case=False, na=False)].shape[0]
            cpu_fixes = df[df["Event"].str.contains("cpu|temporary", case=False, na=False)].shape[0]
            ml_fixes = df[df["Event"].str.contains("scaling|frequency", case=False, na=False)].shape[0]
            total = len(df)

            with col1:
                st.metric("🗄️ Database Heals", db_fixes)
            with col2:
                st.metric("💻 CPU Optimizations", cpu_fixes)
            with col3:
                st.metric("🧠 ML Detections", ml_fixes)
            with col4:
                st.metric("🟢 System Health", "100%", "Optimal")

            st.markdown("---")

            # -----------------------------
            # Chart
            # -----------------------------
            st.markdown("### 📈 Incident Frequency")
            if not filtered_df.empty:
                chart_df = filtered_df.copy()
                chart_df["Minute"] = chart_df["Timestamp"].dt.floor("min")
                counts = chart_df.groupby("Minute").size()
                st.line_chart(counts)
            else:
                st.info("No incidents for selected filter.")

            st.markdown("---")

            # -----------------------------
            # Table
            # -----------------------------
            st.markdown("### 📋 Recent Healing Events")

            if not filtered_df.empty:
                table_df = filtered_df.tail(15).copy()
                table_df["Timestamp"] = table_df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
                table_df["Status"] = "✅ Resolved"

                st.dataframe(
                    table_df[["Timestamp", "Event", "Status"]],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No events to display.")

            # -----------------------------
            # Footer
            # -----------------------------
            st.markdown("---")
            st.caption(f"🕒 Last Updated: {datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            st.error(f"⚠️ Dashboard error: {e}")
            st.info("Check healed_incidents.log formatting.")
