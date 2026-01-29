# 🏥 Self-Healing SRE Agent

A rule-based self-healing system that automatically detects and remediates infrastructure anomalies in real-time. Built for demonstrating SRE automation principles.


## 🎯 What It Does

- **Detects** database connection failures and CPU overload events from system logs
- **Heals** automatically by restarting services and triggering auto-scaling
- **Visualizes** healing events through a real-time Streamlit dashboard

## 🏗️ Architecture
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Log Generator  │─────▶│  Healing Agent   │─────▶│    Dashboard    │
│    (app.py)     │      │    (agent.py)    │      │ (dashboard.py)  │
└─────────────────┘      └──────────────────┘      └─────────────────┘
        │                         │                          │
        ▼                         ▼                          ▼
   system.log            healed_incidents.log          Streamlit UI
```

**Components:**
1. **Log Generator** - Simulates system logs with anomalies (DB errors, CPU spikes)
2. **Healing Agent** - Monitors logs, detects issues, performs remediation
3. **Dashboard** - Real-time visualization of healing events

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone the repository
git clone https://github.com/deepakshivkumar-push/self-healing-sre-agent.git
cd self-healing-sre-agent

# Install dependencies
pip install -r requirements.txt
```

### Running the System

**Terminal 1** - Start log generator:
```bash
python app.py
```

**Terminal 2** - Start healing agent:
```bash
python agent.py
```

**Terminal 3** - Start dashboard:
```bash
streamlit run dashboard.py
```

Open your browser to `http://localhost:8501` to view the dashboard.

## 📊 Demo

### Dashboard Features
- **Real-time metrics**: Total incidents healed, breakdown by type
- **Event timeline**: Recent healing actions with timestamps
- **Auto-refresh**: Updates every 2 seconds

### Example Healing Flow
1. Log generator produces: `ERROR | CPU overload detected | cpu=94%`
2. Agent detects anomaly using pattern matching
3. Agent simulates remediation (cleanup + auto-scaling)
4. Dashboard displays: `SUCCESS: CPU_ERROR - Cleaned up processes and triggered auto-scaling`

## 🛠️ Technical Details

### Detection Rules (Rule-Based)
- **Database Errors**: Connection timeouts, pool exhaustion, authentication failures
- **CPU Errors**: Usage above 80% threshold, performance degradation

### Tech Stack
- **Python 3.x** - Core language
- **Streamlit** - Dashboard framework
- **File-based IPC** - Simple, reliable communication
- **Regex patterns** - Anomaly detection

### Project Structure
```
self-healing-sre-agent/
├── app.py                 # Log generator
├── agent.py               # Self-healing logic
├── dashboard.py           # Streamlit dashboard
├── requirements.txt       # Dependencies
├── README.md             # This file
├── docs/                 # Documentation and screenshots
│   └── dashboard-screenshot.png
└── data/                 # Generated at runtime
    ├── system.log
    └── healed_incidents.log
```

## 🔮 Future Enhancements

- [ ] ML-based anomaly detection (LSTM/Isolation Forest)
- [ ] Prometheus metrics integration
- [ ] Docker Compose deployment
- [ ] Slack/PagerDuty notifications
- [ ] Historical trend analysis
- [ ] Multi-service orchestration

## 🎓 What I Learned

- Designing resilient inter-process communication
- File-based log tailing patterns (similar to `tail -f`)
- Building production-ready monitoring dashboards
- SRE principles: observability, automation, self-healing

## 📝 License

MIT License - feel free to use for learning or demonstrations.

## 👤 Author

Deepak Shiv Kumar

---

- GitHub: https://github.com/deepakshivkumar-push
- LinkedIn: https://www.linkedin.com/in/deepak-shiv-kumar-a88a892bb/

---

⭐ **Star this repo if you found it helpful!**
