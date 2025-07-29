FROM python:3.11-slim

RUN apt-get update && apt-get install -y bash git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./scripts/*.sh

# starting bots
CMD ["bash", "./scripts/start.sh"]
