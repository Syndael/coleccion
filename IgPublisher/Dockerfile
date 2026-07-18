FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY install_ffmpeg.py .
RUN python3 install_ffmpeg.py && rm install_ffmpeg.py

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY publisher.py .
CMD ["python", "publisher.py"]
