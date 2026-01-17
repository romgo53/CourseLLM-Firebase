FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PORT=8000
EXPOSE ${PORT}
# copy 

CMD ["python", "-m", "app.main"]
