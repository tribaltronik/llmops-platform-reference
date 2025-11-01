# llmops-platform-reference
Use FastAPI and vLLM for inferencing
# llmops-platform-reference — hands-on LLM Ops

This repository is a small, hands-on reference for LLM Ops using FastAPI and vLLM. It contains a minimal inference service (FastAPI + vLLM), a Dockerfile for containerization (GPU-enabled), and manifests for Kubernetes deployment.

Audience
- Engineers and SREs learning practical LLM deployment patterns.
- Developers who want a quick, reproducible environment to test LLM inference on GPUs.

Learning objectives
- Build and run a GPU-enabled LLM inference service locally with Docker.
- Understand a minimal production layout (container, resource config, K8s manifest).
- Practice common operational tasks: build optimization, disk cleanup, scaling, and troubleshooting.

Prerequisites
- macOS/Linux/Windows with Docker Desktop (for GPU support, Docker must be configured to expose GPUs).
- NVIDIA GPU + drivers + Docker NVIDIA runtime (if you plan to run with `--gpus`).
- kubectl configured for your cluster (optional for K8s labs).

Quickstart — build and run locally (GPU)

Build the image:

```bash
docker build -t llm-service:local-test .
```

Run the container (GPU):

```bash
docker run -d \
  --name tinyllama-local \
  -p 8000:8000 \
  --gpus all \
  llm-service:local-test
```

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

Notes
- The base image `nvidia/cuda:...` is large; builds require substantial disk space. If you see "no space left on device" during build, free Docker VM space (prune) or increase Docker Desktop disk image size. See Troubleshooting below.
- If you don't have a GPU available, you can still explore the code, but inference with realistic models will be extremely slow or fail without CUDA.

Kubernetes — build & deploy

Build and push an image for your registry:

```bash
docker build -t <your-registry>/tinyllama-service:v1.0 .
docker push <your-registry>/tinyllama-service:v1.0
```

Apply the manifests in `k8s/` (edit image name as needed):

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Test (replace EXTERNAL_IP with your service IP/hostname):

```bash
curl -X POST http://<EXTERNAL_IP>/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello from the lab"}'
```

Hands-on labs / exercises
- Lab 1 — Local run: build the image, run locally, and call `/generate` and `/health`.
- Lab 2 — Docker cleanup: reproduce a "no space left on device" scenario, run the diagnostics (`docker system df`, `docker image ls`), and safely prune unused artifacts.
- Lab 3 — Optimize the Dockerfile: minimize layers, use smaller base images where possible, and pin Python deps in `app/requirements.txt`.
- Lab 4 — K8s rollout: deploy to a cluster, expose via LoadBalancer/Ingress, scale replicas, check readiness/liveness probes.
- Lab 5 — Model swap & configuration: change `MODEL_NAME` in `app/main.py`, re-build and re-deploy, observe memory/latency changes.

Troubleshooting tips
- "no space left on device" during build:
  - Run diagnostic commands on your machine: `df -h` and `docker system df -v`.
  - Free space safely: `docker container prune`, `docker image prune`, `docker builder prune`.
  - Aggressive cleanup (destructive): `docker system prune -a --volumes` (removes unused images and volumes).
  - On macOS Docker Desktop: Preferences → Resources → Disk image and increase the disk image size; apply & restart.
- GPU issues:
  - Ensure NVIDIA drivers and the Docker NVIDIA integration are installed.
  - Verify `nvidia-smi` inside the host and in containers.

Next steps and extensions
- Add metrics (Prometheus + Grafana) and instrument request latency and GPU memory usage.
- Add CI to build and push the image, and a small smoke test against a test cluster.
- Add a minimal ingress + TLS for secure external access.

Contributing
- Please open issues or PRs with proposed improvements to the labs, README or manifests.

License & Attribution
- This repository is a learning reference. Reuse code as you like, and please attribute the source when sharing.

Enjoy the labs — if you'd like, I can also add sample exercise solutions, example `kubectl` outputs, or a short troubleshooting guide for Docker Desktop on macOS.
