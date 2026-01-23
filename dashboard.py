import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="SRE Self-Healing Dashboard", layout="wide")
st.title("🛡️ SRE Agent: Real-Time Incident Monitor")

# Sidebar for stats
st.sidebar.header("System Status")
st.sidebar.success("Agent: ACTIVE")
st.sidebar.info("Model: Isolation Forest (ML)")

# Placeholder for live data
placeholder = st.empty()

while True:
    try:
        # Read the log file
        df = pd.read_csv('healed_incidents.log', names=['Timestamp', 'Event'])
        
        with placeholder.container():
            # Big Metric Counters
            col1, col2 = st.columns(2)
            db_fixes = df[df['Event'].str.contains('Database')].shape[0]
            ml_fixes = df[df['Event'].str.contains('frequency')].shape[0]
            
            col1.metric("Database Restarts", db_fixes)
            col2.metric("ML Scaling Events", ml_fixes)

            # Show the raw log table
            st.subheader("Recent Healing Events")
            st.dataframe(df.tail(10), use_container_width=True)
            
    except Exception:
        st.write("Waiting for first incident to be logged...")
    
    time.sleep(2)