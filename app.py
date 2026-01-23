import time
import random
from datetime import datetime

def write_log(message):
    """Write a timestamped message to system.log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open("system.log", "a") as log_file:
        log_file.write(log_entry)
    
    print(log_entry.strip())  # Also print to console

def main():
    print("Starting system logger... (Press Ctrl+C to stop)")
    
    # Track time since last error
    last_error_time = time.time()
    # Random interval between errors (10-15 seconds)
    next_error_interval = random.randint(10, 15)
    
    error_messages = [
        "ERROR: Database connection failed",
        "ERROR: High CPU usage detected"
    ]
    
    try:
        while True:
            current_time = time.time()
            time_since_error = current_time - last_error_time
            
            # Check if it's time to log an error
            if time_since_error >= next_error_interval:
                # Write a random error
                error_msg = random.choice(error_messages)
                write_log(error_msg)
                
                # Reset the timer and pick new random interval
                last_error_time = current_time
                next_error_interval = random.randint(10, 15)
            else:
                # Write normal healthy message
                write_log("INFO: System healthy")
            
            # Wait 2 seconds before next log entry
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nLogger stopped by user.")

if __name__ == "__main__":
    main()