import time
import os
from datetime import datetime

# ANSI color codes for terminal output
RED = '\033[91m'
RESET = '\033[0m'

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

def tail_log_file(filename):
    """
    Continuously monitor a log file for new lines (like 'tail -f')
    """
    print(f"🔍 Agent is now watching {filename}...")
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
                    # Process the new line
                    process_log_line(line.strip())
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
    print("=" * 60)
    tail_log_file(log_filename)

if __name__ == "__main__":
    main()