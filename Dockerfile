# 1. Use an official Python image
FROM python:3.10-slim

# 2. Set the folder inside the container where our code will live
WORKDIR /app

# 3. Copy our files from your computer into the container
COPY . .

# 4. Install any requirements (even if empty)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Start the "Patient" and "Agent" at the same time
# We use a shell command to run app.py in the background and agent.py in the foreground
CMD ["sh", "-c", "python -u app.py & python -u agent.py"]