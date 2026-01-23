import os
from datetime import datetime

def generate_report():
    """
    Generate a professional SRE incident summary report
    """
    log_filename = "healed_incidents.log"
    
    # Check if the log file exists
    if not os.path.exists(log_filename):
        print("\n" + "=" * 60)
        print("🟢 SRE DAILY INCIDENT SUMMARY")
        print("=" * 60)
        print("System was 100% stable today.")
        print("=" * 60 + "\n")
        return
    
    # Read and analyze the log file
    database_fixes = 0
    cpu_fixes = 0
    
    with open(log_filename, 'r') as f:
        lines = f.readlines()
    
    # If file is empty
    if not lines:
        print("\n" + "=" * 60)
        print("🟢 SRE DAILY INCIDENT SUMMARY")
        print("=" * 60)
        print("System was 100% stable today.")
        print("=" * 60 + "\n")
        return
    
    # Count incidents by type
    for line in lines:
        if 'Database' in line:
            database_fixes += 1
        elif 'CPU' in line or 'Temporary files' in line:
            cpu_fixes += 1
    
    # Calculate totals
    total_incidents = database_fixes + cpu_fixes
    
    # Print the report
    print("\n" + "=" * 60)
    print("📊 SRE DAILY INCIDENT SUMMARY")
    print("=" * 60)
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    print(f"Total Incidents Resolved: {total_incidents}")
    print()
    print("Breakdown by Type:")
    print(f"  🗄️  Database Issues:        {database_fixes}")
    print(f"  💻 CPU/Resource Issues:    {cpu_fixes}")
    print("-" * 60)
    
    # Add status message
    if total_incidents == 0:
        print("Status: 🟢 System was 100% stable today.")
    elif total_incidents <= 5:
        print("Status: 🟡 Minor incidents detected and resolved automatically.")
    else:
        print("Status: 🔴 Multiple incidents detected - system required attention.")
    
    print("=" * 60 + "\n")
    
    # Optional: Show last few incidents
    if total_incidents > 0:
        print("Recent Healing Actions:")
        print("-" * 60)
        # Show last 5 incidents
        for line in lines[-5:]:
            print(f"  {line.strip()}")
        print()

def main():
    generate_report()

if __name__ == "__main__":
    main()