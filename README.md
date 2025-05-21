# WeatherCenter - Scalable Kubernetes Web App ☁️

**WeatherCenter** is a containerized and scalable web application that provides real-time weather forecasts for cities around the world. It is developed with Python, HTML, and JavaScript, and orchestrated using Kubernetes with automated delivery through GitLab CI/CD.

## 🌐 Demo

> Live demo: [https://weathercenter.eu](https://weathercenter.eu)  
> Background examples: sunny day, rainy weather, night mode, snowy day

---

## ⚙️ Technologies Used

- **Frontend**: HTML, CSS, JavaScript (Skycons, autocomplete, dynamic backgrounds)
- **Backend**: Python + `http.server`
- **API**: [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api)
- **Orchestration**: Kubernetes (deployment, service, HPA)
- **CI/CD**: GitLab CI/CD
- **Containerization**: Docker
- **Cloud**: DigitalOcean LoadBalancer
- **Security**: HTTPS with custom SSL certificate



## 🚀 Features

- Real-time city search with autocomplete
- Weather display with animated icons
- Background changes based on weather conditions (e.g., rain, snow, night)
- In-memory caching with TTL for performance
- Horizontal auto-scaling based on CPU load
- SSL certificate and custom domain (`weathercenter.eu`)
- Fully automated CI/CD deployment via GitLab pipelines

---

## 🐳 Docker

Build the image locally:

```bash
docker build -t weathercenter .
docker run -p 80:80 weathercenter
🔁 GitLab CI/CD Pipeline
The GitLab pipeline includes 3 stages:

build – builds and pushes Docker image

test – runs the container and performs a simple health check

deploy – applies Kubernetes configuration and restarts the deployment

---

## ☸️ Kubernetes
Useful commands:

bash
Copiază
Editează
kubectl get pods
kubectl get svc
kubectl describe hpa my-python-hpa
kubectl top nodes
Key YAML files:

my-python-deployment.yaml: defines the container and environment variables

my-python-hpa.yaml: activates autoscaling between 2–10 replicas

my-python-do-lb-service.yaml: exposes the app via a public LoadBalancer


## 🔐 Security
HTTPS enabled via a custom SSL certificate (wethercenter.crt)

Backend sets Content-Security-Policy headers

Sensitive variables stored as Kubernetes Secrets

## 📄 License
MIT License © 2025 Toma Ciobotaru

## 👨‍🎓 Author
Project developed by Toma Ciobotaru
As part of the master’s dissertation project:

“Scalability of Web Applications in Distributed Infrastructures”
Academia de Studii Economice – Faculty of Cybernetics, Statistics and Economic Informatics
Coordinator: Professor Răzvan Zota
