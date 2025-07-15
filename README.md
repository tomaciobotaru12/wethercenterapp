# WeatherCenter - Scalable Kubernetes Web App ☁️

**WeatherCenter** is a containerized and scalable web application that provides real-time weather forecasts for cities around the world. It is developed with Python, HTML, and JavaScript, and orchestrated using Kubernetes with automated delivery through GitLab CI/CD.

## 🖼️ Application Preview

⚠️ The live demo is currently unavailable due to maintenance and deployment costs of the cloud infrastructure.
In the meantime, below is a preview of the autoscaling behavior of the application, monitored via Grafana.

This screenshot captures a live Grafana dashboard powered by Prometheus, showcasing real-time Kubernetes cluster metrics. During a simulated load test using K6, the application scaled up from 2 to 14 pods in response to increased CPU usage.

![Kubernetes Autoscaling Dashboard](https://github.com/user-attachments/assets/14cae324-15a9-4b76-9d22-c3f000ed9a59)


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
- SSL certificate and custom domain (`wethercenter.eu`)
- Fully automated CI/CD deployment via GitLab pipelines

---

## 🐳 Docker

Build the image locally:


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

Sensitive variables stored as Kubernetes Secrets and CI/CD variables



## 👨‍🎓 Author
Project developed by Toma Ciobotaru



