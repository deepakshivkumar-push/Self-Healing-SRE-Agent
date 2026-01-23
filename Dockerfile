FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# The -u is the 'magic' that shows the logs in Railway
CMD ["sh", "-c", "touch healed_incidents.log && python -u app.py & python -u agent.py & streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0"]