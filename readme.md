# AI Marketing Automation & ML Inference Platform

A high-performance, asynchronous ML inference platform designed for automated marketing content generation. This platform bridges Computer Vision (CV) and Large Language Models (LLM) to transform product images into ready-to-use social media copy.

## 🚀 Key Features

- **Automated Marketing Pipeline**: Seamlessly connects image analysis with copy generation.
- **Multimodal Context Mapping**: Converts raw CV detections (e.g., `hotel_room`) into natural language marketing keywords (e.g., `호텔 객실`).
- **Platform-Tailored Copywriting**: Generates optimized content for **Instagram, Twitter, and Blog** with specific tones (Friendly, Professional, Emotional).
- **Scalable Architecture**: Built with FastAPI, Redis, and a distributed Python Worker system.
- **Real-time Monitoring**: Integrated with Prometheus and Grafana for tracking job latency and success rates.

## 🛠 Recent Updates (March 2026)

### 1. Improved Image Recognition Simulation
- Fixed an issue where the CV engine was hardcoded to return "cat" regardless of the input.
- Added realistic detection scenarios for **Hotel Rooms, Cafes, and Lifestyle products**.
- Detection results now include `class`, `score`, and `bbox` data for more granular analysis.

### 2. Intelligent Keyword Mapping
- Implemented a dictionary-based mapping system in the worker pipeline.
- Bridges the gap between technical CV labels and consumer-friendly marketing terms.
- Ensures the generated copy feels natural and "copy-paste ready" for Korean markets.

### 3. Enhanced Marketing Logic
- **Instagram**: Focuses on emojis, trending hashtags, and visual-first language.
- **Twitter**: Optimized for brevity and high-impact "Game Changer" tags.
- **Blog**: Provides professional, link-oriented suffixes for long-form content.

## 🏗 Architecture

1.  **API Gateway (`01_api`)**: FastAPI handles job submission and job status tracking via Redis.
2.  **Message Broker (Redis)**: Orchestrates tasks using a reliable queue system.
3.  **Worker Cluster (`02_worker`)**:
    - **CV Backend**: Simulates/Integrates Computer Vision models (e.g., ResNet, ViT).
    - **LLM Backend**: Simulates/Integrates Language Models (e.g., GPT-4, Llama) for creative writing.
4.  **Web Dashboard (`05_web`)**: A modern React-based interface for monitoring and manual job entry.

## 🚦 Getting Started

### Prerequisites
- Docker and Docker Compose

### Running the Platform
```bash
cd 04_infra
docker-compose up --build
```

### Usage (Marketing Pipeline)
To generate a marketing post from an image:
```bash
curl -X POST http://localhost:8000/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "task": "marketing_pipeline",
    "params": {
      "platform": "instagram",
      "tone": "friendly",
      "language": "ko"
    },
    "input": {"image_id": "luxury_hotel_01"}
  }'
```

## 🗺 Roadmap

- [ ] **Multi-Image Support**: Allow multiple image inputs to generate a cohesive carousel post or story.
- [ ] **Advanced VLM Integration**: Replace the separate CV+LLM pipeline with a single Vision-Language Model (like GPT-4o or Llama-3-Vision) for deeper visual context.
- [ ] **Direct API Integration**: One-click posting to Instagram and Twitter business accounts.
- [ ] **A/B Testing Module**: Generate multiple versions of copy and track engagement metrics.

## 📈 Monitoring
- **Web UI**: http://localhost:5173
- **Prometheus**: http://localhost:9090
- **Worker Metrics**: http://localhost:9091
