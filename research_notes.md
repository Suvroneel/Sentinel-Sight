# Research & Best Practices Notes — SentinelSight

## 1. Studied Platforms
- **Milestone**: Multi-site VMS and centralized camera management.
- **BriefCam**: Post-incident search, analytics modules for review/respond/research.
- **Avigilon**: AI-driven attention alerts, accelerated review experiences.
- **Frigate**: Local-first event processing, MQTT/event messaging, privacy-focused design.

## 2. Features Adopted in SentinelSight
- **Real-time video ingestion** from RTSP streams, supporting multi-camera scaling.
- **Object detection with YOLO** for people/vehicle recognition.
- **Rule-based analytics engine** for intrusion and loitering detection.
- **Web dashboard** displaying camera status, live/periodic frames, and event feeds.
- **Event persistence** in SQLite with snapshot storage only (privacy-first).
- **Modular architecture** (ingestion, inference, rules-engine, API, UI) for scalability.
- **Docker support** for simplified deployment and environment isolation.

## 3. Alignment with Role (Full-Stack AI Software Developer)
- **AI/ML Integration:** YOLO pipeline + inference-service → matches JD’s AI/ML requirement.
- **Full-Stack Development:** FastAPI backend + dashboard → demonstrates web integration.
- **Real-Time Video Analytics:** Multi-camera ingestion + rule engine → aligns with real-time processing and edge integration.
- **Security & Privacy:** Snapshot-based event storage → GDPR-aware, local-first design.
- **Scalable Architecture:** Modular services → production-style mindset.
- **Optional Enhancements:** Event metrics, Dockerization, planned multi-model support → shows initiative and roadmap thinking.

## 4. Next Steps / Roadmap
- Add **multi-model AI support** for varied detection tasks.
- Implement **cloud deployment** (AWS/Azure) for scalability.
- Enable **role-based access control and multi-tenant support**.
- Improve **dashboard analytics** (trend charts, heatmaps, event clip export).
- Expand **integration with external messaging** (MQTT/Webhooks) for enterprise deployment.

