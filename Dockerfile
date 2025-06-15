FROM python:3.10-slim

# Install dependencies and fix Tkinter issues (if removed)
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fix for webtech
RUN mkdir -p /root/.local/share/webtech

COPY . .

ENTRYPOINT ["python", "main.py"]
