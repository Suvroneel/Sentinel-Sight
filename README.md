# SentinelSight: AI Video Analytics Platform

**MVP Implementation for Internship Assessment**  
**Sprint Duration:** 2 days  
**Author:** Suvroneel Nathak  
**Submission Date:** January 13, 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Assignment Context & Objectives](#assignment-context--objectives)
3. [System Architecture](#system-architecture)
4. [Feature Summary](#feature-summary)
5. [Tech Stack](#tech-stack)
6. [How to Run](#how-to-run)
7. [How to Add a Camera Stream](#how-to-add-a-camera-stream)
8. [How to Test the System](#how-to-test-the-system)
9. [API Endpoints](#api-endpoints)
10. [Demo Script](#demo-script)
11. [Known Limitations & Next Steps](#known-limitations--next-steps)
12. [Security, Privacy & Compliance Notes](#security-privacy--compliance-notes)
13. [Research & Best Practices Notes](#research--best-practices-notes)
14. [What I Would Build Next With More Time](#what-i-would-build-next-with-more-time)

---

## Project Overview

SentinelSight is an AI-powered video analytics platform designed to process RTSP camera streams in real-time, detect persons using YOLOv8, and trigger rule-based alerts for security events such as intrusion detection and loitering. This is an MVP implementation demonstrating end-to-end system design, working functionality, and architectural clarity within a 2-day sprint constraint.

**Core Capabilities:**
- RTSP stream ingestion with automatic reconnection
- Real-time person detection using YOLOv8 (Ultralytics)
- Rule-based event detection (intrusion zones, loitering heuristics)
- Event persistence with snapshot storage
- REST API for camera and event management
- Web-based dashboard for event monitoring

**Design Philosophy:**
- Local-first processing (no cloud dependencies for inference)
- Modular architecture with clear separation of concerns
- Event-driven internal communication via lightweight pub/sub
- Operator-friendly UX with minimal configuration
- Extensible foundation for production-grade features

---

## Assignment Context & Objectives

This project was built as part of an internship assessment to demonstrate:

1. **Working End-to-End System:** From RTSP ingestion → AI inference → rule evaluation → event storage → API exposure → UI visualization
2. **Engineering Quality:** Modular design, error handling, automatic retries, logging, and sensible defaults
3. **Product Thinking:** Operator-centric workflows, clear event schemas, and actionable alert mechanisms
4. **Performance & Stability:** Graceful handling of broken streams, FPS throttling, and queue management
5. **Security & Privacy:** Local-first architecture, data minimization, GDPR-aligned patterns
6. **Research & Best Practices:** Analysis of commercial platforms (Milestone, BriefCam, Avigilon, Frigate) and adoption of proven patterns

**Explicit Constraints:**
- 2-day implementation window
- MVP scope: demonstrate capability, not production readiness
- Focus on architectural soundness and extensibility over feature completeness

---

## System Architecture

### High-Level Data Flow

```
┌─────────────┐
│ RTSP Camera │
│   Streams   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Ingestion Service   │  ← OpenCV RTSP capture + reconnect logic
│ (Frame Extraction)  │
└──────┬──────────────┘
       │ (frames)
       ▼
┌─────────────────────┐
│ Internal Event Bus  │  ← Lightweight pub/sub (in-process)
│   (Decoupling)      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Inference Service   │  ← YOLOv8 person detection
│   (YOLOv8)          │
└──────┬──────────────┘
       │ (detections)
       ▼
┌─────────────────────┐
│ Internal Event Bus  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Rules Engine      │  ← Zone intrusion + loitering logic
│ (Analytics Rules)   │
└──────┬──────────────┘
       │ (events)
       ▼
┌─────────────────────┐
│   Event Store       │  ← SQLite (event metadata + snapshots)
│   (Persistence)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   REST API Layer    │  ← FastAPI endpoints
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Web Dashboard     │  ← HTML/JS/CSS UI with auto-refresh
└─────────────────────┘
```

### Repository Structure

```
sentinelsight/
├── backend/
│   ├── api/                  # FastAPI routes and schemas
│   ├── ingestion/            # RTSP capture + reconnect logic
│   ├── inference/            # YOLOv8 detection service
│   ├── rules/                # Rule engine (zones, loitering)
│   ├── event_bus/            # In-process pub/sub mechanism
│   ├── models/               # Database models (SQLite)
│   ├── storage/              # Event persistence layer
│   ├── config.py             # Configuration management
│   └── main.py               # Application entry point
├── ui/
│   ├── index.html            # Dashboard UI
│   ├── styles.css
│   └── app.js
├── data/
│   ├── database/             # SQLite database files
│   └── snapshots/            # Event snapshot images
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Architectural Design Decisions

**Modularity via Event Bus:**  
The internal pub/sub event bus decouples ingestion, inference, and rule evaluation. This allows independent scaling, testing, and replacement of components (e.g., swapping YOLO for a different model, adding MQTT publishers).

**Local-First Processing:**  
All inference runs locally without cloud API dependencies, ensuring low latency, data privacy, and operational cost predictability.

**Event-Driven Persistence:**  
Only trigger-worthy events are stored with associated snapshots. This minimizes storage requirements compared to continuous video recording while maintaining forensic utility.

**Extensibility Points:**
- Event bus can be replaced with Redis Streams or RabbitMQ for distributed deployments
- Rule engine designed to support custom Python rule plugins
- API layer prepared for webhook/MQTT notification integrations
- Database schema supports multi-tenancy and RBAC extensions

---

## Feature Summary

### MVP Features (Implemented)

| Feature | Description | Status |
|---------|-------------|--------|
| RTSP Ingestion | OpenCV-based frame capture with auto-reconnect | ✅ |
| Person Detection | YOLOv8 inference on ingested frames | ✅ |
| Intrusion Detection | Configurable zone-based alerts when person detected | ✅ |
| Loitering Detection | Time-in-zone heuristic (MVP threshold: 10 seconds) | ✅ |
| Event Persistence | SQLite storage with event metadata + snapshots | ✅ |
| REST API | Camera management and event retrieval endpoints | ✅ |
| Web Dashboard | Real-time event feed with auto-refresh | ✅ |
| Health Monitoring | System status endpoint | ✅ |
| Docker Deployment | Single-command container setup | ✅ |

### Optional/Future Features (Not Implemented)

- Continuous video recording (DVR functionality)
- Multi-model pipelines (face recognition, vehicle detection)
- MQTT/webhook alerting
- Role-based access control (RBAC)
- Distributed camera ingestion nodes
- Advanced analytics (crowd counting, heatmaps)
- Mobile application

---

## Tech Stack

**Backend Framework:**  
- FastAPI 0.109.0 (async REST API, automatic OpenAPI docs)

**AI/ML:**  
- Ultralytics YOLOv8n (lightweight person detection model)
- OpenCV 4.9.0 (RTSP stream processing)

**Database:**  
- SQLite 3 (embedded, zero-config persistence)

**Frontend:**  
- Vanilla HTML/CSS/JavaScript (no framework dependencies)

**Infrastructure:**  
- Docker & Docker Compose
- Python 3.11

**Key Libraries:**  
- `opencv-python`: Video stream capture
- `ultralytics`: YOLOv8 model inference
- `sqlalchemy`: Database ORM
- `pydantic`: Data validation and settings management
- `uvicorn`: ASGI server

---

## How to Run

### Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+ and pip (local development)
- RTSP camera stream URL (or use public test streams)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd sentinelsight

# Build and start services
docker-compose up --build

# Application will be available at:
# - API: http://localhost:8000
# - Dashboard: http://localhost:8000/dashboard
# - API Docs: http://localhost:8000/docs
```

**Configuration via Environment Variables:**

```bash
# Create .env file (optional)
RTSP_TIMEOUT=10
INFERENCE_FPS=5
LOG_LEVEL=INFO
```

### Option 2: Local Development

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
cd backend
python main.py

# Application starts at http://localhost:8000
```

### Verification Steps

1. **Check Health Endpoint:**
   ```bash
   curl http://localhost:8000/health
   # Expected: {"status": "healthy", "timestamp": "..."}
   ```

2. **Access API Documentation:**  
   Navigate to `http://localhost:8000/docs` for interactive Swagger UI

3. **Open Dashboard:**  
   Navigate to `http://localhost:8000/dashboard`

---

## How to Add a Camera Stream

### Via API (Recommended)

```bash
curl -X POST http://localhost:8000/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Front Entrance",
    "rtsp_url": "rtsp://username:password@192.168.1.100:554/stream1",
    "location": "Building A - Main Entrance",
    "zones": [
      {
        "name": "restricted_area",
        "coordinates": [[100, 100], [500, 100], [500, 400], [100, 400]],
        "type": "intrusion"
      }
    ]
  }'
```

**Response:**
```json
{
  "id": "cam_abc123",
  "name": "Front Entrance",
  "rtsp_url": "rtsp://...",
  "location": "Building A - Main Entrance",
  "status": "active",
  "created_at": "2026-01-13T10:30:00Z"
}
```

### Via Dashboard

1. Open `http://localhost:8000/dashboard`
2. Click "Add Camera" button
3. Fill in form fields:
   - Camera Name
   - RTSP URL
   - Location (optional)
   - Zone Coordinates (optional, format: `[[x1,y1],[x2,y2],...]`)
4. Click "Submit"

### Zone Configuration Format

Zones are defined as polygons using pixel coordinates:

```json
{
  "zones": [
    {
      "name": "restricted_lobby",
      "coordinates": [[200, 150], [600, 150], [600, 450], [200, 450]],
      "type": "intrusion"
    },
    {
      "name": "waiting_area",
      "coordinates": [[50, 50], [150, 50], [150, 150], [50, 150]],
      "type": "loitering",
      "threshold_seconds": 15
    }
  ]
}
```

### Public Test Streams

If you don't have an RTSP camera, use these public streams:

```
rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4
```

---

## How to Test the System

### Manual Testing Workflow

**1. Add Test Camera:**
```bash
curl -X POST http://localhost:8000/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Camera",
    "rtsp_url": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
    "location": "Test Zone"
  }'
```

**2. Verify Camera Status:**
```bash
curl http://localhost:8000/cameras
```

**3. Monitor Events:**
```bash
# Poll for new events
curl http://localhost:8000/events

# Watch dashboard in browser
# Open: http://localhost:8000/dashboard
# Events will appear automatically when person detected
```

**4. Retrieve Specific Event:**
```bash
curl http://localhost:8000/events/{event_id}
```

### Expected Behavior

- **Intrusion Event:** When person enters defined restricted zone
- **Loitering Event:** When person remains in zone > threshold (default: 10s)
- **Event Data:** Each event includes:
  - Timestamp
  - Camera ID and name
  - Detection confidence score
  - Rule type triggered
  - Snapshot image path
  - Bounding box coordinates

### Logs & Debugging

```bash
# View application logs (Docker)
docker-compose logs -f

# Check ingestion status
# Logs will show: "Camera {name} connected successfully"
# Or: "Camera {name} connection failed, retrying..."

# Check inference pipeline
# Logs will show: "Person detected with confidence 0.87"

# Check rule evaluation
# Logs will show: "Event triggered: intrusion in zone restricted_area"
```

### Automated Testing (Future)

Current MVP includes manual testing. Production system would include:
- Unit tests for rule engine logic
- Integration tests for API endpoints
- Mock RTSP streams for CI/CD
- Performance benchmarks (FPS, latency)

---

## API Endpoints

### Camera Management

**GET /cameras**  
Retrieve all registered cameras

```bash
curl http://localhost:8000/cameras
```

Response:
```json
[
  {
    "id": "cam_abc123",
    "name": "Front Entrance",
    "rtsp_url": "rtsp://...",
    "location": "Building A",
    "status": "active",
    "created_at": "2026-01-13T10:30:00Z"
  }
]
```

**POST /cameras**  
Register new camera stream

```bash
curl -X POST http://localhost:8000/cameras \
  -H "Content-Type: application/json" \
  -d '{"name": "...", "rtsp_url": "...", "location": "...", "zones": [...]}'
```

### Event Retrieval

**GET /events**  
Retrieve events with optional filters

Query Parameters:
- `camera_id` (optional): Filter by camera
- `rule_type` (optional): Filter by rule (intrusion, loitering)
- `start_time` (optional): ISO 8601 timestamp
- `end_time` (optional): ISO 8601 timestamp
- `limit` (optional): Max results (default: 100)

```bash
curl "http://localhost:8000/events?camera_id=cam_abc123&limit=50"
```

Response:
```json
[
  {
    "id": "evt_xyz789",
    "camera_id": "cam_abc123",
    "camera_name": "Front Entrance",
    "timestamp": "2026-01-13T14:22:35Z",
    "rule_type": "intrusion",
    "zone_name": "restricted_area",
    "confidence": 0.92,
    "snapshot_path": "/data/snapshots/evt_xyz789.jpg",
    "metadata": {
      "bbox": [120, 200, 350, 580],
      "person_count": 1
    }
  }
]
```

**GET /events/{event_id}**  
Retrieve specific event details

```bash
curl http://localhost:8000/events/evt_xyz789
```

### System Health

**GET /health**  
Check system status

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-13T15:00:00Z",
  "active_cameras": 3,
  "inference_fps": 5.2
}
```

### API Documentation

Interactive Swagger UI available at: `http://localhost:8000/docs`

---

## Demo Script

**Duration:** 3-5 minutes  
**Objective:** Demonstrate end-to-end functionality and architectural decisions

### Script

**[0:00 - 0:30] Introduction & Context**
- "This is SentinelSight, an AI video analytics platform MVP built in 2 days"
- "Architecture: RTSP ingestion → YOLOv8 inference → rule engine → event persistence → REST API → web dashboard"
- "Key design: local-first processing, event-driven decoupling, operator-friendly UX"

**[0:30 - 1:30] System Architecture Walkthrough**
- Show README architecture diagram
- "Internal event bus decouples components for independent scaling and testing"
- "Event-driven persistence: we store triggered events with snapshots, not continuous video"
- "Repository structure maps directly to architectural modules"

**[1:30 - 2:30] Live Demonstration**
- Open dashboard at `http://localhost:8000/dashboard`
- Show existing cameras and event feed
- Add new camera via API: `curl -X POST ...` (prepared command)
- "Camera connects automatically, starts frame extraction"
- Show event appearing in dashboard when person detected in restricted zone
- Click event to view snapshot and metadata

**[2:30 - 3:30] Engineering Quality Highlights**
- Show logs demonstrating automatic reconnection when stream drops
- "Error handling: exponential backoff, circuit breaker pattern"
- "FPS throttling prevents CPU overload on inference"
- Show API documentation: `http://localhost:8000/docs`
- "OpenAPI schema auto-generated, production-ready contract"

**[3:30 - 4:30] Research & Product Thinking**
- "Studied Milestone, BriefCam, Avigilon, Frigate"
- "Adopted: zone-based detection (Milestone), event-centric storage (BriefCam), local-first (Frigate)"
- "Product decisions: minimal operator configuration, clear event schema for downstream integrations"
- "GDPR-aligned: local processing, data minimization, no PII in base system"

**[4:30 - 5:00] Next Steps & Extensibility**
- "With more time: MQTT alerts, RBAC, distributed ingestion, advanced analytics"
- "Architecture prepared for these extensions via event bus abstraction and modular design"
- "Thank you for reviewing. Questions welcome."

---

## Known Limitations & Next Steps

### Current MVP Limitations

**1. Single-Node Deployment**
- All components run in single process
- No horizontal scaling for high camera counts
- **Next Step:** Distribute ingestion workers across nodes, centralize event bus via Redis Streams

**2. Basic Rule Engine**
- Intrusion detection uses simple point-in-polygon checks
- Loitering uses naive time-in-zone threshold (10 seconds)
- No configurable rule parameters via UI
- **Next Step:** Python-based rule plugin system, UI-based rule builder

**3. Person Detection Only**
- YOLOv8 configured for person class exclusively
- No vehicle, animal, or object detection
- **Next Step:** Multi-model pipeline with configurable detection classes per camera

**4. No Real-Time Alerting**
- Events stored but no push notifications
- Operators must poll dashboard or API
- **Next Step:** MQTT publishing, webhook integration, email/SMS alerts via configurable channels

**5. Limited Authentication**
- No user authentication or authorization
- Open API access
- **Next Step:** JWT-based auth, role-based access control (admin/operator/viewer roles)

**6. Storage Constraints**
- SQLite not suitable for high-throughput production
- No automatic snapshot cleanup policy
- **Next Step:** PostgreSQL migration, retention policies, S3-compatible snapshot storage

**7. Inference Performance**
- YOLOv8n prioritizes speed over accuracy
- Fixed 5 FPS inference rate
- No GPU acceleration in Docker config
- **Next Step:** YOLOv8m/l models, dynamic FPS adjustment, NVIDIA Docker runtime

**8. Network Resilience**
- RTSP reconnect logic works but introduces gaps during reconnection
- No frame buffering during temporary disconnections
- **Next Step:** Frame buffer queue, seamless failover to backup streams

### Technical Debt

- Unit test coverage: 0% (manual testing only)
- No structured logging (using print statements)
- Configuration via hardcoded constants (not externalized)
- No observability stack (metrics, traces)

### Production Readiness Checklist

- [ ] Comprehensive test suite (unit, integration, E2E)
- [ ] Structured logging with correlation IDs
- [ ] Prometheus metrics and Grafana dashboards
- [ ] PostgreSQL with connection pooling
- [ ] Redis-based event bus for distributed processing
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline with automated testing
- [ ] Security audit (dependency scanning, SAST/DAST)
- [ ] Load testing and performance benchmarks
- [ ] Documentation site (user guides, API reference)

---

## Security, Privacy & Compliance Notes

### Data Privacy by Design

**Local-First Architecture:**  
All video processing occurs on-premises. No frames or video data transmitted to external services. This eliminates third-party data processor risks and reduces attack surface.

**Data Minimization:**  
System stores only event metadata and single-frame snapshots, not continuous video. Retention policies can be configured to auto-delete events after configurable period (e.g., 30 days).

**No PII Collection:**  
Base system does not collect personally identifiable information. Person detection generates bounding boxes and confidence scores only—no facial recognition, biometric data, or identity tracking.

**GDPR Alignment:**
- **Lawful Basis:** Security monitoring falls under legitimate interest (Article 6(1)(f))
- **Data Subject Rights:** Event deletion API supports right to erasure
- **Data Protection Impact Assessment (DPIA):** Recommended before production deployment
- **Notice Requirements:** Operators should display visible signage indicating surveillance

### Security Hardening (Production Roadmap)

**Authentication & Authorization:**
- JWT-based API authentication
- Role-based access control (RBAC): admin, operator, viewer
- API key rotation policies

**Network Security:**
- TLS/SSL for all API endpoints
- VPN/ZeroTrust network access for camera streams
- Firewall rules restricting RTSP port exposure

**Data Security:**
- Encrypted database at rest (SQLCipher)
- Encrypted snapshots in S3-compatible storage
- Audit logging for all API access

**Dependency Management:**
- Automated vulnerability scanning (Snyk, Dependabot)
- Regular security patch updates
- Software Bill of Materials (SBOM) generation

### Compliance Considerations

**Industry-Specific:**
- **Healthcare (HIPAA):** Additional PHI safeguards required if deployed in medical facilities
- **Finance (PCI-DSS):** Segregation required if monitoring payment processing areas
- **Government (FedRAMP):** Continuous monitoring and compliance attestation needed

**Recommended Practices:**
- Annual security audits and penetration testing
- Incident response plan with breach notification procedures
- Data retention policies aligned with legal requirements
- Operator training on privacy-preserving monitoring practices

---

## Research & Best Practices Notes

### Platforms Studied

#### 1. Milestone XProtect (Enterprise VMS)

**Features Analyzed:**
- Zone-based analytics configuration
- Multi-tier architecture (recording servers, management servers, clients)
- Integration ecosystem with 10,000+ camera/device partners
- Rule-based event management with automated responses

**Adopted Patterns:**
- **Zone-based detection abstraction:** Polygon coordinates for flexible area monitoring
- **Modular architecture:** Separation of ingestion, processing, and presentation layers
- **Event-first design:** Events as primary data model rather than continuous video

**Implementation in SentinelSight:**
- Zones defined as JSON polygon arrays in camera configuration
- Intrusion detection triggers when person bounding box intersects zone polygon
- Modular service separation (ingestion, inference, rules, API) mirrors Milestone's architecture

**Rationale:**  
Zone-based detection provides operator flexibility without requiring code changes. Milestone's proven multi-tier architecture demonstrates how to scale from single-server to distributed deployments.

---

#### 2. BriefCam (Video Synopsis & Analytics)

**Features Analyzed:**
- Event-centric storage model (not video-centric)
- Structured metadata extraction from video
- Search and filter by event attributes
- Forensic review workflows optimized for post-event investigation

**Adopted Patterns:**
- **Event persistence over continuous recording:** Store only actionable events with snapshots
- **Structured event schema:** Consistent metadata format (timestamp, camera, rule, confidence, bbox)
- **Query-optimized storage:** SQLite schema designed for time-range and camera-based queries

**Implementation in SentinelSight:**
- Events stored with rich metadata: `{camera_id, timestamp, rule_type, confidence, snapshot_path, bbox}`
- No continuous video recording, reducing storage by ~95% compared to traditional DVR
- REST API supports filtering by camera, time range, rule type for forensic searches

**Rationale:**  
For security monitoring, most footage is uneventful. BriefCam's approach of storing only events dramatically reduces storage costs while maintaining forensic utility. Their query-first design influenced our API endpoint structure.

---

#### 3. Avigilon (AI-Powered Security)

**Features Analyzed:**
- Self-learning video analytics
- Unusual motion detection and anomaly scoring
- Focus + Review workflow (highlight unusual events for human review)
- Confidence scoring on detections

**Adopted Patterns:**
- **Confidence thresholds:** Include detection confidence in event metadata
- **Operator review workflow:** Dashboard presents events chronologically for review
- **Quality-over-quantity alerts:** Rules designed to minimize false positives

**Implementation in SentinelSight:**
- YOLOv8 confidence scores stored with each event (0.0-1.0 range)
- Event dashboard sorted by timestamp, allows operators to review chronologically
- Intrusion rules require person detection (not just motion) to reduce false alerts

**Rationale:**  
Avigilon's Focus workflow demonstrates importance of operator efficiency. By pre-filtering events via AI confidence scores and zone rules, we reduce alert fatigue. Future enhancement: add unusual motion detection using anomaly scoring.

---

#### 4. Frigate NVR (Open Source)

**Features Analyzed:**
- Local-first processing (no cloud dependencies)
- MQTT event publishing for home automation integration
- Docker-native deployment
- Configurable object detection zones via YAML

**Adopted Patterns:**
- **Local inference:** All processing on-premises, no external API calls
- **Lightweight deployment:** Docker Compose single-command setup
- **Event bus architecture:** Publish/subscribe pattern for extensibility

**Implementation in SentinelSight:**
- YOLOv8 runs locally, no cloud AI service dependencies
- Internal event bus enables future MQTT publishing without refactoring
- Docker Compose deployment matches Frigate's operator-friendly setup

**Rationale:**  
Frigate proves that local-first AI analytics is viable for resource-constrained environments. Their MQTT integration pattern influenced our event bus design, preparing for webhook/notification integrations. Docker-native approach reduces deployment friction.

---

### Cross-Platform Insights

**Storage Strategy Comparison:**

| Platform | Storage Model | Adopted |
|----------|---------------|---------|
| Milestone | Continuous video + event markers | ❌ |
| BriefCam | Event metadata + synopsis | ✅ |
| Avigilon | Continuous + AI-tagged moments | Partial |
| Frigate | Continuous + clips on events | ❌ |

**Decision:** Event-only storage (BriefCam model) chosen for MVP due to storage efficiency and GDPR data minimization alignment.

**Analytics Architecture Comparison:**

| Platform | Processing Model | Adopted |
|----------|------------------|---------|
| Milestone | Plugin-based analytics | Future |
| BriefCam | Server-side batch processing | ❌ |
| Avigilon | Real-time edge AI | ✅ |
| Frigate | Real-time with MQTT events | ✅ |

**Decision:** Real-time processing (Avigilon/Frigate model) chosen for immediate event detection. Batch processing deferred to future multi-camera correlation features.

---

### Features to Add Next & Why

**Priority 1: MQTT/Webhook Event Publishing**
- **Why:** Enables integration with existing security systems (alarm panels, access control)
- **Inspired by:** Frigate's MQTT events, Milestone's webhook actions
- **Implementation:** Publish events to MQTT broker or HTTP endpoints via event bus subscribers
- **Business Value:** Makes SentinelSight a data source for enterprise security orchestration platforms

**Priority 2: Rule Engine Plugin System**
- **Why:** Allows custom analytics without modifying core codebase
- **Inspired by:** Milestone's MIP SDK plugin architecture
- **Implementation:** Python-based rule plugins loaded dynamically, subscribe to detection events
- **Business Value:** Enables customer-specific analytics (e.g., retail occupancy counting, industrial PPE detection)

**Priority 3: Multi-Model Pipeline**
- **Why:** Extend beyond person detection to vehicles, PPE, license plates
- **Inspired by:** Avigilon's multi-class detection, BriefCam's attribute extraction
- **Implementation:** Configurable model selection per camera, parallel inference pipelines
- **Business Value:** Addresses broader market segments (parking, industrial safety, retail)

**Priority 4: Advanced Loitering Detection**
- **Why:** Current time-in-zone heuristic is MVP-level, prone to false positives
- **Inspired by:** Avigilon's unusual motion detection
- **Implementation:** Track person trajectories, distinguish loitering from normal transit
- **Business Value:** Reduces false alerts, improves operator trust in system

**Priority 5: Distributed Ingestion Nodes**
- **Why:** Single-node ingestion bottlenecks at ~20-30 cameras
- **Inspired by:** Milestone's distributed recording server architecture
- **Implementation:** Redis-based event bus, ingestion workers on separate nodes
- **Business Value:** Enables enterprise-scale deployments (100+ cameras)

**Priority 6: Forensic Search Interface**
- **Why:** Current API-only event access is not operator-friendly
- **Inspired by:** BriefCam's video synopsis search UI
- **Implementation:** Web UI with time-range selector, camera filter, thumbnail previews
- **Business Value:** Reduces investigation time from hours to minutes

---

### Implementation Rationale Summary

This MVP prioritized patterns that demonstrate architectural maturity within the 2-day constraint:

1. **Event bus decoupling** (Frigate/Milestone) enables future distributed deployment
2. **Event-only storage** (BriefCam) demonstrates understanding of GDPR and cost optimization
3. **Zone-based rules** (Milestone) shows product thinking around operator usability
4. **Local-first AI** (Frigate/Avigilon) proves technical capability without cloud vendor lock-in
5. **Confidence scoring** (Avigilon) reduces false positives, foundation for self-learning systems

The architecture is deliberately over-engineered for the MVP scope to demonstrate extensibility thinking required for production systems.

---

## What I Would Build Next With More Time

### 6-Month Roadmap (Post-MVP)

**Month 1-2: Production Hardening**
- Comprehensive test suite (unit, integration, E2E)
- Structured logging with ELK stack integration
- Prometheus metrics + Grafana dashboards
- PostgreSQL migration with connection pool
