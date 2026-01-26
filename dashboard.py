# dashboard.py
# Streamlit Dashboard - Visualizes self-healing events in real-time
# Reads from healed_incidents.log and displays statistics

import streamlit as st
import os
import time
from datetime import datetime
import re
from collections import Counter

# Configuration
HEALING_LOG = "data/healed_incidents.log"
REFRESH_INTERVAL = 2  # Seconds between auto-refresh


def parse_healing_log_line(line):
    """
    Parse a single line from healed_incidents.log.
    Expected format: [YYYY-MM-DD HH:MM:SS] SUCCESS: <ANOMALY_TYPE> - <message>
    
    Args:
        line (str): A single log line
    
    Returns:
        dict: Parsed event with timestamp, anomaly_type, and message
        None: If line cannot be parsed
    """
    # Regex to extract: [timestamp] SUCCESS: ANOMALY_TYPE - message
    pattern = r'\[(.+?)\] SUCCESS: ([A-Z_]+) - (.+)'
    match = re.match(pattern, line.strip())
    
    if match:
        timestamp_str = match.group(1)
        anomaly_type = match.group(2)
        message = match.group(3)
        
        try:
            # Parse timestamp
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            
            return {
                'timestamp': timestamp,
                'anomaly_type': anomaly_type,
                'message': message,
                'timestamp_str': timestamp_str
            }
        except ValueError:
            # Invalid timestamp format
            return None
    
    return None


def read_healing_events():
    """
    Read and parse all healing events from the log file.
    Handles missing files and I/O errors gracefully.
    
    Returns:
        list: List of parsed event dictionaries (newest first)
        str: Error message if file cannot be read, or None if successful
    """
    # Check if file exists
    if not os.path.exists(HEALING_LOG):
        return [], "Log file not found. Waiting for healing events..."
    
    # Check if file is empty
    if os.path.getsize(HEALING_LOG) == 0:
        return [], "Log file is empty. Waiting for healing events..."
    
    events = []
    
    try:
        with open(HEALING_LOG, 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                if line.strip():  # Skip empty lines
                    parsed = parse_healing_log_line(line)
                    if parsed:
                        events.append(parsed)
        
        # Return events in reverse chronological order (newest first)
        events.reverse()
        
        return events, None
        
    except IOError as e:
        return [], f"Error reading log file: {str(e)}"
    except Exception as e:
        return [], f"Unexpected error: {str(e)}"


def calculate_statistics(events):
    """
    Calculate statistics from healing events.
    
    Args:
        events (list): List of parsed event dictionaries
    
    Returns:
        dict: Statistics including total count, type breakdown, and recent activity
    """
    if not events:
        return {
            'total': 0,
            'db_errors': 0,
            'cpu_errors': 0,
            'other_errors': 0,
            'last_healing': None
        }
    
    # Count anomaly types
    anomaly_types = [event['anomaly_type'] for event in events]
    type_counts = Counter(anomaly_types)
    
    # Calculate statistics
    stats = {
        'total': len(events),
        'db_errors': type_counts.get('DB_ERROR', 0),
        'cpu_errors': type_counts.get('CPU_ERROR', 0),
        'other_errors': sum(count for atype, count in type_counts.items() 
                           if atype not in ['DB_ERROR', 'CPU_ERROR']),
        'last_healing': events[0]['timestamp_str'] if events else None
    }
    
    return stats


def main():
    """
    Main Streamlit dashboard application.
    Displays self-healing statistics and recent events.
    """
    # Page configuration
    st.set_page_config(
        page_title="Self-Healing SRE Dashboard",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for dark mode styling
    st.markdown("""
        <style>
        /* Main container styling */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: bold;
        }
        
        /* Success message styling */
        .success-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: rgba(0, 255, 0, 0.1);
            border-left: 4px solid #00ff00;
            margin: 1rem 0;
        }
        
        /* Error message styling */
        .error-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: rgba(255, 0, 0, 0.1);
            border-left: 4px solid #ff0000;
            margin: 1rem 0;
        }
        
        /* Table styling */
        .dataframe {
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🏥 Self-Healing SRE Dashboard")
    st.markdown("**Real-time monitoring of automated incident remediation**")
    
    # Add a separator
    st.markdown("---")
    
    # Read healing events
    events, error_message = read_healing_events()
    
    # Display error if file cannot be read
    if error_message:
        st.warning(f"⚠️ {error_message}")
        st.info("💡 **Instructions:**\n"
                "1. Start the log generator: `python app.py`\n"
                "2. Start the healing agent: `python agent.py`\n"
                "3. Wait for anomalies to be detected and healed")
        
        # Show empty state
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Incidents Healed", 0)
        with col2:
            st.metric("Database Errors", 0)
        with col3:
            st.metric("CPU Errors", 0)
        
        # Auto-refresh message
        st.caption(f"⟳ Auto-refreshing every {REFRESH_INTERVAL} seconds...")
        time.sleep(REFRESH_INTERVAL)
        st.rerun()
        return
    
    # Calculate statistics
    stats = calculate_statistics(events)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Incidents Healed",
            value=stats['total'],
            delta=f"Active" if stats['total'] > 0 else "Waiting"
        )
    
    with col2:
        st.metric(
            label="🗄️ Database Errors",
            value=stats['db_errors'],
            delta=f"{stats['db_errors']/stats['total']*100:.0f}%" if stats['total'] > 0 else "0%"
        )
    
    with col3:
        st.metric(
            label="⚡ CPU Errors",
            value=stats['cpu_errors'],
            delta=f"{stats['cpu_errors']/stats['total']*100:.0f}%" if stats['total'] > 0 else "0%"
        )
    
    with col4:
        st.metric(
            label="🔧 Other Errors",
            value=stats['other_errors'],
            delta=f"{stats['other_errors']/stats['total']*100:.0f}%" if stats['total'] > 0 else "0%"
        )
    
    # Show last healing time
    if stats['last_healing']:
        st.success(f"✅ Last healing: **{stats['last_healing']}**")
    
    # Add separator
    st.markdown("---")
    
    # Display recent healing events
    st.subheader("📋 Recent Healing Events")
    
    if events:
        # Prepare data for table display
        table_data = []
        for event in events[:20]:  # Show last 20 events
            table_data.append({
                'Timestamp': event['timestamp_str'],
                'Type': event['anomaly_type'].replace('_', ' ').title(),
                'Action': event['message']
            })
        
        # Display as dataframe
        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )
        
        # Show count if more than 20 events
        if len(events) > 20:
            st.caption(f"Showing 20 most recent events (total: {len(events)})")
    else:
        st.info("No healing events yet. The dashboard will update automatically when incidents are detected and healed.")
    
    # Footer with refresh info
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.caption(f"📂 Reading from: `{HEALING_LOG}`")
    
    with col2:
        st.caption(f"⟳ Auto-refresh: {REFRESH_INTERVAL}s")
    
    # Auto-refresh by sleeping and rerunning
    time.sleep(REFRESH_INTERVAL)
    st.rerun()


if __name__ == "__main__":
    main()