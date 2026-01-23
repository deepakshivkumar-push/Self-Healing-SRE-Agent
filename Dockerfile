FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# The -u is the 'magic' that shows the logs in Railway
CMD ["sh", "-c", "python -u app.py & python -u agent.py"]