# 🚀 Deployment Guide - H100 GPU API

Complete guide to deploy your fine-tuned models as REST API on H100 GPU

---

## 📦 What You Have

I've created a complete API deployment solution:

1. **`api_server.py`** - FastAPI server with all model endpoints
2. **`Dockerfile`** - Docker image for H100 deployment
3. **`docker-compose.yml`** - Docker Compose configuration
4. **`kubernetes.yaml`** - Kubernetes deployment (optional)
5. **`test_api.py`** - API testing script
6. **`client_example.py`** - Python client library
7. **`requirements_api.txt`** - API dependencies

---

## 🎯 Deployment Options

### **Option 1: Local Deployment** (Testing)
### **Option 2: Docker Deployment** (Recommended)
### **Option 3: Kubernetes Deployment** (Production)

---

## 🔧 Option 1: Local Deployment

### Step 1: Install API Dependencies
```bash
pip install -r requirements_api.txt
```

### Step 2: Run the API Server
```bash
python api_server.py
```

### Step 3: Test the API
```bash
# In another terminal
python test_api.py
```

### Step 4: Access API Documentation
Open your browser: `http://localhost:8000/docs`

---

## 🐳 Option 2: Docker Deployment (H100 GPU)

### Prerequisites:
- Docker installed
- NVIDIA Docker runtime installed
- H100 GPU with drivers

### Step 1: Install NVIDIA Container Toolkit
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Step 2: Build Docker Image
```bash
docker build -t llm-api:latest .
```

### Step 3: Run with Docker Compose
```bash
docker-compose up -d
```

### Step 4: Check Logs
```bash
docker-compose logs -f
```

### Step 5: Test API
```bash
python test_api.py
```

### Step 6: Stop Service
```bash
docker-compose down
```

---

## ☸️ Option 3: Kubernetes Deployment

### Prerequisites:
- Kubernetes cluster with GPU nodes
- kubectl configured
- NVIDIA GPU Operator installed

### Step 1: Build and Push Image
```bash
# Build
docker build -t your-registry/llm-api:latest .

# Push to registry
docker push your-registry/llm-api:latest
```

### Step 2: Update kubernetes.yaml
Edit `kubernetes.yaml` and update:
- Image name
- Models volume path

### Step 3: Deploy
```bash
kubectl apply -f kubernetes.yaml
```

### Step 4: Check Status
```bash
kubectl get pods
kubectl get services
```

### Step 5: Get API URL
```bash
kubectl get service llm-api-service
```

---

## 🌐 API Endpoints

### Base URL: `http://your-server:8000`

### Available Endpoints:

#### 1. Health Check
```bash
GET /health
```

#### 2. List Models
```bash
GET /api/models
```

#### 3. HR Model
```bash
POST /api/hr
{
  "query": "How do I apply for leave?",
  "max_tokens": 200,
  "temperature": 0.7,
  "top_p": 0.9
}
```

#### 4. Finance Model
```bash
POST /api/finance
{
  "query": "What is GST rate for restaurants?",
  "max_tokens": 200
}
```

#### 5. Sales Model
```bash
POST /api/sales
{
  "query": "How to handle return request?",
  "max_tokens": 200
}
```

#### 6. Healthcare Model
```bash
POST /api/healthcare
{
  "query": "What are symptoms of dengue?",
  "max_tokens": 200
}
```

#### 7. Marketing Model
```bash
POST /api/marketing
{
  "query": "Create Diwali campaign",
  "max_tokens": 200
}
```

#### 8. Generic Endpoint (Any Model)
```bash
POST /api/infer/{model_name}
{
  "query": "Your question here",
  "max_tokens": 200
}
```

---

## 📝 Example Usage

### cURL Examples:

#### Health Check:
```bash
curl http://localhost:8000/health
```

#### HR Query:
```bash
curl -X POST http://localhost:8000/api/hr \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I apply for casual leave?",
    "max_tokens": 200,
    "temperature": 0.7
  }'
```

#### Healthcare Query:
```bash
curl -X POST http://localhost:8000/api/healthcare \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are symptoms of dengue fever?",
    "max_tokens": 150
  }'
```

### Python Client:

```python
from client_example import LLMClient

# Initialize client
client = LLMClient("http://localhost:8000")

# Query HR model
response = client.query_hr("How to apply for leave?")
print(response['response'])

# Query Healthcare model
response = client.query_healthcare("Symptoms of dengue?")
print(response['response'])
```

### JavaScript/Node.js:

```javascript
const axios = require('axios');

async function queryModel(model, question) {
  const response = await axios.post(
    `http://localhost:8000/api/${model}`,
    {
      query: question,
      max_tokens: 200,
      temperature: 0.7
    }
  );
  return response.data;
}

// Usage
const result = await queryModel('hr', 'How to apply for leave?');
console.log(result.response);
```

---

## ⚡ H100 Optimization

The API is optimized for H100 GPU with:

### 1. Automatic GPU Detection
```python
# In api_server.py
device_map='auto'  # Automatically uses GPU
torch_dtype=torch.float16  # Half precision for speed
```

### 2. Model Caching
- Models are loaded once and cached
- Subsequent requests are instant
- No reload overhead

### 3. Batch Processing (Optional)
To enable batch processing, modify `api_server.py`:
```python
# Process multiple queries at once
# Uncomment batch processing section
```

### 4. H100-Specific Settings
```bash
# Environment variables (already in Dockerfile)
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

---

## 📊 Performance Benchmarks

Expected performance on H100 GPU:

| Model | Load Time | First Query | Subsequent Queries | Tokens/sec |
|-------|-----------|-------------|-------------------|------------|
| HR (Full) | 5-10s | 2-3s | 0.5-1s | 100-150 |
| Finance (DPO) | 5-10s | 2-3s | 0.5-1s | 100-150 |
| Sales (PEFT) | 3-5s | 1-2s | 0.3-0.5s | 150-200 |
| Healthcare (LoRA) | 3-5s | 1-2s | 0.3-0.5s | 150-200 |
| Marketing (QLoRA) | 3-5s | 1-2s | 0.3-0.5s | 150-200 |

*Benchmarks for TinyLlama-1.1B on H100*

---

## 🔒 Security Considerations

### 1. Add Authentication
```python
# In api_server.py, add:
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/api/hr")
def hr_inference(request: InferenceRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Verify token
    if credentials.credentials != "your-secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    # ... rest of code
```

### 2. Rate Limiting
```bash
pip install slowapi

# Add to api_server.py
from slowapi import Limiter, _rate_limit_exceeded_handler
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/hr")
@limiter.limit("10/minute")
def hr_inference(...):
    ...
```

### 3. HTTPS/SSL
Use reverse proxy (Nginx) with SSL certificate:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

---

## 🐛 Troubleshooting

### Issue: GPU not detected
```bash
# Check NVIDIA driver
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Issue: Out of GPU memory
```python
# In api_server.py, comment out preload_models()
# Load models on-demand instead
```

### Issue: Slow inference
```bash
# Check GPU utilization
nvidia-smi -l 1

# Enable FP16
# Already enabled in api_server.py
```

### Issue: Port already in use
```bash
# Change port in api_server.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

---

## 📈 Scaling Options

### Horizontal Scaling (Multiple Instances):
```yaml
# In kubernetes.yaml
replicas: 3  # Run 3 instances
```

### Load Balancing:
```bash
# Use Nginx as load balancer
upstream llm_backend {
    server server1:8000;
    server server2:8000;
    server server3:8000;
}
```

### Multi-GPU:
```python
# Modify api_server.py to support multiple GPUs
# Distribute models across GPUs
```

---

## 🔍 Monitoring

### 1. Health Checks
```bash
# Automated health check
watch -n 5 curl http://localhost:8000/health
```

### 2. Logging
```python
# API logs are in stdout
docker-compose logs -f llm-api
```

### 3. Metrics (Optional)
Add Prometheus metrics:
```bash
pip install prometheus-fastapi-instrumentator

# In api_server.py
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

---

## 📚 API Documentation

### Interactive Docs:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🎯 Quick Start Commands

```bash
# Local deployment
pip install -r requirements_api.txt
python api_server.py

# Docker deployment
docker-compose up -d

# Test API
python test_api.py

# Use Python client
python client_example.py

# Stop services
docker-compose down
```

---

## 🚀 Production Checklist

- [ ] Build Docker image
- [ ] Test API locally
- [ ] Configure environment variables
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable HTTPS
- [ ] Add authentication
- [ ] Set up rate limiting
- [ ] Configure monitoring
- [ ] Set up logging
- [ ] Create backup strategy
- [ ] Document API for team
- [ ] Load test with expected traffic

---

## 💡 Next Steps

1. Deploy API locally first
2. Test all endpoints
3. Deploy on H100 GPU server
4. Monitor performance
5. Scale as needed

---

**Your API is ready to deploy on H100! 🚀**
