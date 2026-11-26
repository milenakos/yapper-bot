FROM python:3.15-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY yapper.py /app/yapper.py

# yapping.json is read and written in the working directory, so it lives in /data, which is the volume.
WORKDIR /data

# The bot connects out to Discord and listens on no port. YAPPER_TOKEN comes from the environment.
CMD ["python", "/app/yapper.py"]
