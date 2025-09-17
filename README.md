# Kubernetes Deployment Guide

## Prerequisites

* Minikube installed
* Docker installed
* kubectl configured

## Deployment Steps

### 1. Start Minikube Cluster

```bash
minikube start --driver=docker
```

### 2. Use Minikube's Docker Environment

```bash
eval $(minikube docker-env)
```

### 3. Build FastAPI Image Inside Minikube

```bash
docker build -t restro_fastapi:latest .
```

### 4. Deploy MySQL to Kubernetes

```bash
kubectl apply -f mysql.yml
```

### 5. Run Alembic Migrations

```bash
kubectl apply -f migrate.yml
```

### 6. Deploy FastAPI Application

```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

### 7. Access FastAPI Service

#### Option 1: Using Minikube Service

```bash
minikube service restro-fastapi-service
```

#### Option 2: Using Port Forwarding

```bash
kubectl port-forward service/restro-fastapi-service 8080:80
```

## Notes

* Ensure all YAML files (mysql.yml, migrate.yml, deployment.yml, service.yml) are present in your project directory
* **Option 1** : The minikube service command will automatically open the service in your default browser
* **Option 2** : Port forwarding makes the service available at `http://localhost:8080`
* Use Ctrl+C to stop the port forwarding when done
