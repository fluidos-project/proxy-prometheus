# Prometheus Proxy HTTP

This project implements a **custom HTTP proxy** in Python that receives metric data in Prometheus `remote_write` format and forwards it to the real server configured via environment variables.

---

## 🎯 Why a custom proxy?

While Prometheus can send metrics directly, this proxy allows:

- Injecting custom logic before forwarding
- Inspecting, logging, or transforming metrics on the fly
- Adding a security or access control layer if needed

---

## 🧠 Architecture

```txt
[ Prometheus Remote Write Client ]
              |
              v
   [ Prometheus HTTP Proxy (Python) ]
              |
              v
[ Real Prometheus in Kubernetes (monitoring namespace) ]
```

---

## 🚀 Running Locally

### Requirements

- Python 3.9+
- `pip install -r requirements.txt`

### Environment variables (`.env`)

The proxy uses the following environment variables for configuration:

| Variable                 | Default Value                                                                                 | Description                                        |
| ------------------------ | --------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `REAL_PROM_REMOTE_WRITE` | `http://prometheus-operator-kube-p-prometheus.monitoring.svc.cluster.local:9090/api/v1/write` | URL of the real Prometheus `remote_write` endpoint |
| `PROXY_PORT`             | `8080`                                                                                        | Port where the proxy listens                       |

---

## 🐳 Docker

```bash
docker build -t proxy-prometheus .
docker run -p 8080:8080 --env-file .env proxy-prometheus
```

---

## ☸️ Kubernetes Deployment

Kubernetes manifests are provided in the `k8s/` directory to deploy the proxy as a service.

### Relevant files

- `k8s/deployment.yaml`: Deployment configuration with necessary environment variables
- `k8s/service.yaml`: `NodePort` service exposing port 8080

### Exposed Ports

| Service                 | Protocol | Container Port | NodePort | Description                            |
| ----------------------- | -------- | -------------- | -------- | -------------------------------------- |
| `otel-prometheus-proxy` | HTTP     | `8080`         | `30080`  | Endpoint for Prometheus `remote_write` |

---

## 🧪 Example Usage

The proxy listens for POST requests at:

```http
POST http://<host>:8080/write
Content-Type: application/x-protobuf
```

> Compatible with clients sending data in Prometheus `remote_write` format.