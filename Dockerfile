FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY . /app
ENTRYPOINT ["python3", "-W", "ignore", "main.py", "--project"]