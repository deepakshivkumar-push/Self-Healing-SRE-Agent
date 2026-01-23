import time
import os
from datetime import datetime
from collections import deque
from sklearn.ensemble import IsolationForest
import numpy as np

# ANSI color codes for terminal output
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Global variables for anomaly detection
log_timestamps = deque(maxlen=100)  # Keep last 100 log timestamps
model = IsolationForest(contamination=0.1, random_state=42)
is_model_trained = False

def fix_database():
    """
    Execute database remediation steps
    """
    print("🔧 ACTION: Restarting Database Service...")
    time.sleep(1)  # Simulate action taking time
    
    # Log the successful remediation
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] SUCCESS: Database service restarted and connection restored\n"
    
    print("DEBUG: Writing to healed_incidents.log now...")
    with open('healed_incidents.log', 'a') as f:
        f.write(log_entry)
        f.flush()  # Ensure data is written immediately
    print("DEBUG: Write complete!")
    
def fix_cpu():
    """
    Execute CPU remediation steps
    """
    print("🔧 ACTION: Clearing temporary files and scaling resources...")
    time.sleep(1)  # Simulate action taking time
    
    # Log the successful remediation
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] SUCCESS: Temporary files cleared and resources scaled to handle load\n"
    
    print("DEBUG: Writing to healed_incidents.log now...")
    with open('healed_incidents.log', 'a') as f:
        f.write(log_entry)
        f.flush()  # Ensure data is written immediately
    print("DEBUG: Write complete!")

def handle_frequency_anomaly():
    """
    Handle anomalies detected by frequency analysis
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] SUCCESS: Frequency anomaly detected - scaling infrastructure to handle spike\n"
    
    print("🔧 ACTION: Unusual log frequency detected - scaling infrastructure...")
    time.sleep(1)
    
    print("DEBUG: Writing to healed_incidents.log now...")
    with open('healed_incidents.log', 'a') as f:
        f.write(log_entry)
        f.flush()
    print("DEBUG: Write complete!")

def calculate_log_frequency():
    """
    Calculate logs per second over the last few seconds
    """
    if len(log_timestamps) < 2:
        return 0.0
    
    # Calculate frequency over last 10 logs
    recent_logs = list(log_timestamps)[-10:]
    if len(recent_logs) < 2:
        return 0.0
    
    time_span = recent_logs[-1] - recent_logs[0]
    if time_span == 0:
        return 0.0
    
    frequency = len(recent_logs) / time_span
    return frequency

def detect_frequency_anomaly():
    """
    Use Isolation Forest to detect anomalous log frequencies
    """
    global is_model_trained
    
    # Need at least 20 data points to train
    if len(log_timestamps) < 20:
        return False
    
    # Calculate current frequency
    current_freq = calculate_log_frequency()
    
    # Get historical frequencies
    frequencies = []
    timestamps_list = list(log_timestamps)
    
    for i in range(10, len(timestamps_list)):
        window = timestamps_list[i-10:i]
        if len(window) >= 2:
            time_span = window[-1] - window[0]
            if time_span > 0:
                freq = len(window) / time_span
                frequencies.append(freq)
    
    if len(frequencies) < 10:
        return False
    
    # Train the model if not trained yet or retrain periodically
    if not is_model_trained or len(frequencies) % 50 == 0:
        X_train = np.array(frequencies).reshape(-1, 1)
        model.fit(X_train)
        is_model_trained = True
    
    # Predict if current frequency is an anomaly
    X_current = np.array([[current_freq]])
    prediction = model.predict(X_current)
    
    # -1 indicates anomaly
    return prediction[0] == -1

def tail_log_file(filename):
    """
    Continuously monitor a log file for new lines (like 'tail -f')
    """
    print(f"🔍 Agent is now watching {filename}...")
    print("🤖 ML Model: Isolation Forest initialized for frequency analysis")
    print("Press Ctrl+C to stop\n")
    
    # Wait for file to exist
    while not os.path.exists(filename):
        print(f"Waiting for {filename} to be created...")
        time.sleep(1)
    
    with open(filename, 'r') as log_file:
        # Move to the end of the file
        log_file.seek(0, os.SEEK_END)
        
        try:
            while True:
                # Read new line
                line = log_file.readline()
                
                if line:
                    # Record timestamp for frequency analysis
                    log_timestamps.append(time.time())
                    
                    # Process the new line
                    process_log_line(line.strip())
                    
                    # Check for frequency anomalies
                    if detect_frequency_anomaly():
                        print(f"{YELLOW}⚠️  ML ANOMALY: Unusual log frequency detected!{RESET}")
                        print(f"   Current frequency: {calculate_log_frequency():.2f} logs/sec\n")
                        handle_frequency_anomaly()
                        print("✅ Recovery action executed successfully. Checking system health...\n")
                else:
                    # No new line yet, wait a bit
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n\n⛔ Monitoring stopped by user.")

def process_log_line(line):
    """
    Analyze each log line for errors and take action
    """
    if 'ERROR' in line:
        # Alert in bright red
        print(f"{RED}🚨 ANOMALY DETECTED: {line}{RESET}")
        
        # Brain: Determine the appropriate action based on error type
        take_action(line)
    else:
        # Regular healthy line
        print("Searching...")

def take_action(error_line):
    """
    Decide what action to take based on the error message
    """
    print()  # Blank line for readability
    
    if 'Database' in error_line:
        fix_database()
        print("✅ Recovery action executed successfully. Checking system health...\n")
        
    elif 'CPU' in error_line:
        fix_cpu()
        print("✅ Recovery action executed successfully. Checking system health...\n")
        
    else:
        print("⚠️  ACTION: Alerting human on-call SRE.")
        print("📧 Alert sent to on-call engineer.\n")

def main():
    log_filename = "system.log"
    print("=" * 60)
    print("🤖 Self-Healing SRE Agent - Starting Up...")
    print("🧠 Enhanced with Machine Learning (Isolation Forest)")
    print("=" * 60)
    tail_log_file(log_filename)

if __name__ == "__main__":
    main()