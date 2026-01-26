# agent.py
# Self-Healing Agent - Detects anomalies in system.log and performs remediation
# Runs independently from app.py and continuously monitors for issues

import time
import os
import re
from datetime import datetime

# Configuration
LOG_FILE = "data/system.log"
HEALING_LOG = "data/healed_incidents.log"
CHECK_INTERVAL = 0.5  # Seconds between file checks (avoid high CPU)
STARTUP_WAIT = 2      # Seconds to wait for log file on startup

# Remediation simulation delays (seconds)
DB_RESTART_TIME = 2
CPU_CLEANUP_TIME = 1.5


def get_timestamp():
    """
    Returns current timestamp in the required format.
    Format: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_data_directory():
    """
    Create the data directory if it doesn't exist.
    Ensures both LOG_FILE and HEALING_LOG can be accessed.
    """
    os.makedirs("data", exist_ok=True)


def wait_for_log_file():
    """
    Wait for the system.log file to exist before starting monitoring.
    This prevents crashes if the agent starts before the log generator.
    Returns True when file exists, or after timeout.
    """
    print(f"[INIT] Waiting for log file: {LOG_FILE}")
    
    wait_time = 0
    max_wait = 30  # Maximum 30 seconds wait
    
    while not os.path.exists(LOG_FILE) and wait_time < max_wait:
        time.sleep(1)
        wait_time += 1
        if wait_time % 5 == 0:
            print(f"[INIT] Still waiting... ({wait_time}s)")
    
    if os.path.exists(LOG_FILE):
        print(f"[INIT] ✅ Log file found!")
        return True
    else:
        print(f"[INIT] ⚠️  Log file not found, starting anyway...")
        return False


def tail_log_file(file_path, start_from_end=True):
    """
    Generator that yields new lines from a file as they appear.
    Similar to 'tail -f' command in Unix.
    
    Args:
        file_path (str): Path to the file to tail
        start_from_end (bool): If True, start reading from end of file
    
    Yields:
        str: New lines as they are appended to the file
    """
    # Open file and seek to position
    with open(file_path, 'r') as f:
        if start_from_end:
            # Move to end of file to ignore existing logs
            f.seek(0, 2)  # 2 = end of file
            print("[TAIL] Starting from end of file (ignoring existing logs)")
        else:
            # Start from beginning
            print("[TAIL] Starting from beginning of file")
        
        while True:
            # Read new line
            line = f.readline()
            
            if line:
                # New line available - yield it
                yield line.strip()
            else:
                # No new line - wait and check again
                time.sleep(CHECK_INTERVAL)


def detect_anomaly(log_line):
    """
    Analyze a log line and detect if it contains an anomaly.
    Uses rule-based pattern matching.
    
    Args:
        log_line (str): A single log line from system.log
    
    Returns:
        tuple: (anomaly_type, details) or (None, None) if no anomaly
        
    Anomaly types:
        - 'db_error': Database connection issues
        - 'cpu_error': High CPU usage
    """
    # Check if line is an ERROR (ignore INFO logs)
    if '| ERROR |' not in log_line:
        return None, None
    
    # Extract the error message part (everything after '| ERROR |')
    error_match = re.search(r'\| ERROR \| (.+)', log_line)
    if not error_match:
        return None, None
    
    error_message = error_match.group(1)
    
    # Rule 1: Detect Database Errors
    db_keywords = [
        'database connection',
        'connection pool',
        'connection refused',
        'failed to connect to database',
        'database authentication'
    ]
    
    for keyword in db_keywords:
        if keyword.lower() in error_message.lower():
            return 'db_error', error_message
    
    # Rule 2: Detect CPU Errors
    cpu_keywords = [
        'cpu overload',
        'high cpu usage',
        'cpu threshold exceeded',
        'cpu spike',
        'performance degraded'
    ]
    
    for keyword in cpu_keywords:
        if keyword.lower() in error_message.lower():
            return 'cpu_error', error_message
    
    # Unknown error type
    return None, None


def remediate_db_error(error_details):
    """
    Simulate database restart remediation.
    In production, this would actually restart database connections.
    
    Args:
        error_details (str): Details of the database error
    
    Returns:
        str: Success message describing the remediation
    """
    print(f"  🔧 Remediating: Database error detected")
    print(f"  ⏳ Simulating database connection pool restart...")
    
    # Simulate the time it takes to restart database connections
    time.sleep(DB_RESTART_TIME)
    
    # In production, this would:
    # - Close existing connections
    # - Recreate connection pool
    # - Verify connectivity
    # - Update monitoring metrics
    
    remediation_message = "Database connection pool restarted successfully"
    print(f"  ✅ {remediation_message}")
    
    return remediation_message


def remediate_cpu_error(error_details):
    """
    Simulate CPU overload remediation.
    In production, this would perform cleanup and scaling operations.
    
    Args:
        error_details (str): Details of the CPU error
    
    Returns:
        str: Success message describing the remediation
    """
    print(f"  🔧 Remediating: CPU overload detected")
    print(f"  ⏳ Simulating cleanup and scaling operations...")
    
    # Simulate the time it takes to perform remediation
    time.sleep(CPU_CLEANUP_TIME)
    
    # In production, this would:
    # - Kill/restart resource-heavy processes
    # - Clear temporary caches
    # - Trigger auto-scaling (add more instances)
    # - Optimize running queries
    # - Update load balancer configuration
    
    remediation_message = "Cleaned up processes and triggered auto-scaling"
    print(f"  ✅ {remediation_message}")
    
    return remediation_message


def log_healing_event(anomaly_type, remediation_message):
    """
    Write a healing event to the healed_incidents.log file.
    Format: [YYYY-MM-DD HH:MM:SS] SUCCESS: <message>
    
    Args:
        anomaly_type (str): Type of anomaly that was healed
        remediation_message (str): Description of the remediation action
    """
    timestamp = get_timestamp()
    log_entry = f"[{timestamp}] SUCCESS: {anomaly_type.upper()} - {remediation_message}"
    
    # Append to healing log file
    with open(HEALING_LOG, 'a') as f:
        f.write(log_entry + '\n')
        f.flush()
        os.fsync(f.fileno())  # Force write to disk


def main():
    """
    Main loop - continuously monitors system.log and performs healing.
    Runs indefinitely until interrupted with Ctrl+C.
    """
    print("=" * 70)
    print("SELF-HEALING AGENT STARTED")
    print("=" * 70)
    print(f"Monitoring: {LOG_FILE}")
    print(f"Healing log: {HEALING_LOG}")
    print(f"Check interval: {CHECK_INTERVAL}s")
    print("Press Ctrl+C to stop")
    print("=" * 70)
    
    # Ensure data directory exists
    ensure_data_directory()
    
    # Wait for log file to be created by app.py
    wait_for_log_file()
    
    # If log file still doesn't exist, create it empty so we can start monitoring
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'a').close()
        print(f"[INIT] Created empty log file: {LOG_FILE}")
    
    # Counter for tracking healing actions
    healing_count = 0
    lines_processed = 0
    
    print("\n[MONITOR] 👀 Watching for anomalies...\n")
    
    try:
        # Start tailing the log file
        for log_line in tail_log_file(LOG_FILE, start_from_end=True):
            lines_processed += 1
            
            # Detect if this log line contains an anomaly
            anomaly_type, error_details = detect_anomaly(log_line)
            
            if anomaly_type:
                # Anomaly detected - start remediation
                print(f"\n{'=' * 70}")
                print(f"🚨 ANOMALY DETECTED: {anomaly_type}")
                print(f"{'=' * 70}")
                print(f"  Error: {error_details}")
                
                # Perform appropriate remediation
                if anomaly_type == 'db_error':
                    remediation_message = remediate_db_error(error_details)
                elif anomaly_type == 'cpu_error':
                    remediation_message = remediate_cpu_error(error_details)
                else:
                    # Unknown anomaly type (shouldn't happen)
                    remediation_message = f"Unknown anomaly type: {anomaly_type}"
                
                # Log the healing event
                log_healing_event(anomaly_type, remediation_message)
                
                # Update counter
                healing_count += 1
                
                print(f"  📝 Healing event logged")
                print(f"  📊 Total healings: {healing_count}")
                print(f"{'=' * 70}\n")
                
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("SELF-HEALING AGENT STOPPED")
        print("=" * 70)
        print(f"Lines processed: {lines_processed}")
        print(f"Total healing actions: {healing_count}")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ ERROR: Agent encountered an exception: {e}")
        print("Agent will exit. Please check the logs and restart.")


if __name__ == "__main__":
    main()