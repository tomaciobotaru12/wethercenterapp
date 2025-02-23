FROM python:3.9.10-slim-bullseye
WORKDIR /app
ADD ./src/index.html index.html
ADD ./src/server.py server.py
ADD ./src/server.py server_https.py
#ADD ./certificates/wethercenter.crt wethercenter.crt
#ADD ./certificates/wethercenter.key wethercenter.key
 
RUN apt-get update && apt-get install -y curl
EXPOSE 80
ENTRYPOINT ["python3", "server.py"]
#ENTRYPOINT ["python3", "server_https.py"]