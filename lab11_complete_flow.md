# Lab 11: Containerization and Kubernetes Deployment Flow

## 1. Local Containerization (Docker)
Build the container image:
```bash
docker build -t car-price-prediction-api:v1.0.0 .
```

Run container locally with mapped port:
```bash
docker run -d --name car-api -p 8000:8000 car-price-prediction-api:v1.0.0
```

Verify health status:
```bash
curl http://localhost:8000/health
```

Perform sample prediction:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"symboling": 3, "carbrand": "alfa-romero", "fueltype": "gas", "aspiration": "std", "doornumber": "two", "carbody": "convertible", "drivewheel": "rwd", "enginelocation": "front", "wheelbase": 88.6, "carlength": 168.8, "carwidth": 64.1, "carheight": 48.8, "curbweight": 2548, "enginetype": "dohc", "cylindernumber": "four", "enginesize": 130, "fuelsystem": "mpfi", "boreratio": 3.47, "stroke": 2.68, "compressionratio": 9.0, "horsepower": 111, "peakrpm": 5000, "citympg": 21, "highwaympg": 27}'
```

## 2. Kubernetes Orchestration (k8s)
Deploy to local cluster (Minikube / Kind / K3s):
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check rollout status and pod health:
```bash
kubectl rollout status deployment/car-price-api-deployment
kubectl get pods -l app=car-price-api
kubectl get svc car-price-api-service
```
