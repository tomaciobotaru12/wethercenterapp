FROM python:3.9.10-slim-bullseye
WORKDIR /app

# Copy source code
COPY ./src/index.html index.html
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
