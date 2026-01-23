import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import os

# Professional dark mode configuration
st.set_page_config(
    page_title="SRE Self-Healing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode professional aesthetic
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
    .metric-success {
        color: #00ff88;
    }
    .metric-warning {
        color: #ffaa00;
    }
    .metric-danger {
        color: #ff4444;
    }
    h1 {
        color: #00ff88;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    .status-badge {
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .status-active {
        background-color: #00ff88;
        color: #000;
    }
    .status-scanning {
        background-color: #ffaa00;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🛡️ SRE SELF-HEALING DASHBOARD")
st.markdown("### Real-Time Intelligent Monitoring System")

# Sidebar - Professional Status Panel
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    st.markdown("---")
    
    # Agent Status
    st.markdown("### Agent Status")
    status_placeholder = st.empty()
    status_placeholder.success("🟢 **ACTIVE** - Monitoring in Progress")
    
    st.markdown("### ML Model")
    st.info("🧠 **Isolation Forest**\nUnsupervised Anomaly Detection")
    
    st.markdown("---")
    
    # Filter Options
    st.markdown("### 📊 Log Filters")
    filter_option = st.radio(
        "Select View:",
        ["All Events", "ML Anomalies Only", "Database Errors Only", "CPU Issues Only"],
        index=0
    )
    
    st.markdown("---")
    
    # Refresh Rate
    refresh_rate = st.slider("Refresh Rate (seconds)", 1, 10, 2)
    
    st.markdown("---")
    st.caption("🚀 Powered by ML & Python")

# Main Dashboard
placeholder = st.empty()

# Initialize session state for tracking
if 'last_incident_count' not in st.session_state:
    st.session_state.last_incident_count = 0

# Create a container for the dashboard content
main_container = st.empty()

# Use a fragment or a standard loop with a stop condition check
while True:
    try:
        # Check if log file exists
        if not os.path.exists('healed_incidents.log'):
            with main_container.container():
                st.warning("⏳ Waiting for first incident to be logged...")
            time.sleep(refresh_rate)
            continue
            
        # READ DATA
       # Read the log file with explicit string types
        df = pd.read_csv(
            'healed_incidents.log', 
            names=['Timestamp', 'Event'], 
            on_bad_lines='skip',
            dtype={'Timestamp': str, 'Event': str}  # Forces columns to be strings
        )
        
        # Ensure there's actually data before processing
        if df.empty:
            with placeholder.container():
                st.warning("⏳ Log file is empty. Waiting for the Agent to detect the first incident...")
            time.sleep(refresh_rate)
            continue

        # Parse timestamps only after confirming the data isn't empty
        df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.strip('[]'), errors='coerce')
    except Exception as e:
        # Silently handle transient session errors
        if "SessionInfo" not in str(e):
            st.error(f"Dashboard Error: {e}")
            
    time.sleep(refresh_rate)