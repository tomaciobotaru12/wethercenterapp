FROM python:3.9.10-slim-bullseye
WORKDIR /app

# Copy source code
COPY ./src/index.html index.html
COPY ./src/forecast.html forecast.html
COPY ./src/logo.png logo.png
COPY ./src/clear.jpeg clear.jpeg
COPY ./src/night.jpeg night.jpeg
COPY ./src/rain.jpeg rain.jpeg
COPY ./src/snow.jpg snow.jpg
COPY ./src/server.py server.py

# Copy SSL certificates (if available)
COPY ./certificates/ ./certificates/

RUN apt-get update && apt-get install -y curl

# Set environment variables
ENV PORT=80
ENV CERT_FILE=/app/certificates/wethercenter.crt
ENV KEY_FILE=/app/certificates/wethercenter.key

EXPOSE 80 443
ENTRYPOINT ["python3", "server.py"]
