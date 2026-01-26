# app.py
# Log Generator - Simulates system logs with normal operations and anomalies
# This script runs continuously and appends logs to system.log

import time
import random
from datetime import datetime
import os

# Configuration
LOG_FILE = "data/system.log"
LOG_INTERVAL_MIN = 1  # Minimum seconds between logs
LOG_INTERVAL_MAX = 2  # Maximum seconds between logs

# Anomaly probabilities (percentage chance per log entry)
PROB_DB_ERROR = 5      # 5% chance of database connection failure
PROB_CPU_ERROR = 3     # 3% chance of CPU overload
PROB_NORMAL = 92       # 92% chance of normal operation


def ensure_data_directory():
    """
    Create the data directory if it doesn't exist.
    This ensures LOG_FILE can be written to.
    """
    os.makedirs("data", exist_ok=True)
    print(f"[INIT] Data directory ready")


def get_timestamp():
    """
    Returns current timestamp in a consistent format.
    Format: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_normal_log():
    """
    Generate a normal INFO log entry with randomized system metrics.
    Simulates healthy system operation.
    """
    cpu_usage = random.randint(10, 60)  # Normal CPU: 10-60%
    mem_usage = random.randint(30, 70)  # Normal memory: 30-70%
    disk_usage = random.randint(20, 60) # Normal disk: 20-60%
    
    messages = [
        f"Service healthy | cpu={cpu_usage}% mem={mem_usage}% disk={disk_usage}%",
        f"Request processed successfully | cpu={cpu_usage}% mem={mem_usage}%",
        f"Health check passed | cpu={cpu_usage}% mem={mem_usage}% disk={disk_usage}%",
        f"Background job completed | cpu={cpu_usage}% mem={mem_usage}%",
        f"API endpoint responded | latency={random.randint(50, 200)}ms cpu={cpu_usage}%"
    ]
    
    timestamp = get_timestamp()
    message = random.choice(messages)
    return f"{timestamp} | INFO | {message}"


def generate_db_error():
    """
    Generate a database connection failure ERROR log.
    Simulates database connectivity issues that need remediation.
    """
    timestamp = get_timestamp()
    error_types = [
        "Database connection timeout | host=db.example.com port=5432",
        "Connection pool exhausted | active_connections=100 max_connections=100",
        "Database connection refused | host=db.example.com error=ECONNREFUSED",
        "Failed to connect to database | host=db.example.com retries=3",
        "Database authentication failed | user=app_user error=invalid_credentials"
    ]
    
    error_message = random.choice(error_types)
    return f"{timestamp} | ERROR | {error_message}"


def generate_cpu_error():
    """
    Generate a CPU overload ERROR log.
    Simulates high CPU usage that requires intervention.
    """
    timestamp = get_timestamp()
    cpu_usage = random.randint(85, 99)  # Critical CPU: 85-99%
    mem_usage = random.randint(60, 90)  # Often accompanied by high memory
    
    error_types = [
        f"CPU overload detected | cpu={cpu_usage}% mem={mem_usage}% threshold=80%",
        f"High CPU usage warning | cpu={cpu_usage}% process=api_server mem={mem_usage}%",
        f"CPU threshold exceeded | cpu={cpu_usage}% duration=30s mem={mem_usage}%",
        f"System performance degraded | cpu={cpu_usage}% load_avg={random.uniform(4.0, 8.0):.2f}",
        f"CPU spike detected | cpu={cpu_usage}% mem={mem_usage}% cause=heavy_processing"
    ]
    
    error_message = random.choice(error_types)
    return f"{timestamp} | ERROR | {error_message}"


def select_log_type():
    """
    Randomly select which type of log to generate based on probabilities.
    Returns: 'normal', 'db_error', or 'cpu_error'
    """
    rand = random.randint(1, 100)
    
    if rand <= PROB_CPU_ERROR:
        return 'cpu_error'
    elif rand <= PROB_CPU_ERROR + PROB_DB_ERROR:
        return 'db_error'
    else:
        return 'normal'


def append_log(log_entry):
    """
    Safely append a log entry to the log file.
    Uses append mode ('a') to ensure we never overwrite existing logs.
    Flushes immediately to ensure the log is visible to other processes.
    
    Args:
        log_entry (str): The log line to append
    """
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '\n')
        f.flush()  # Ensure the write is immediately visible to readers
        os.fsync(f.fileno())  # Force write to disk (important for reliability)


def main():
    """
    Main loop - continuously generates and appends logs.
    Runs indefinitely until interrupted with Ctrl+C.
    """
    print("=" * 60)
    print("LOG GENERATOR STARTED")
    print("=" * 60)
    print(f"Log file: {LOG_FILE}")
    print(f"Log interval: {LOG_INTERVAL_MIN}-{LOG_INTERVAL_MAX} seconds")
    print(f"Anomaly rates: DB={PROB_DB_ERROR}% CPU={PROB_CPU_ERROR}%")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Ensure the data directory exists
    ensure_data_directory()
    
    # Log counter for status updates
    log_count = 0
    
    try:
        while True:
            # Determine what type of log to generate
            log_type = select_log_type()
            
            # Generate the appropriate log entry
            if log_type == 'cpu_error':
                log_entry = generate_cpu_error()
                print(f"[{log_count}] 🔴 CPU ERROR")
            elif log_type == 'db_error':
                log_entry = generate_db_error()
                print(f"[{log_count}] 🔴 DB ERROR")
            else:
                log_entry = generate_normal_log()
                print(f"[{log_count}] ✅ INFO")
            
            # Append to file
            append_log(log_entry)
            
            # Increment counter
            log_count += 1
            
            # Wait before generating next log
            sleep_duration = random.uniform(LOG_INTERVAL_MIN, LOG_INTERVAL_MAX)
            time.sleep(sleep_duration)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print(f"LOG GENERATOR STOPPED")
        print(f"Total logs generated: {log_count}")
        print("=" * 60)


if __name__ == "__main__":
    main()