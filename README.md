# llmops-platform-reference
Use FastAPI and vLLM for inferencing
Deploy it on K8s


## Steps to Build and Run Locally with Docker

´´´
docker build -t llm-service:local-test .
´´´

´´´
docker run -d \
  --name tinyllama-local \
  -p 8000:8000 \
  --gpus all \
  llm-service:local-test
´´´

Test the Health Check Endpoint
´´´
curl http://localhost:8000/health
´´´



## K8s
´´´
docker build -t user/tinyllama-service:v1.0 .
docker push user/tinyllama-service:v1.0
´´´

Deploy in k8s
´´´
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
´´´

Test
´´´
EXTERNAL_IP="<IP-ou-Hostname>"
curl -X POST http://${EXTERNAL_IP}/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Ask anything"}'
´´´