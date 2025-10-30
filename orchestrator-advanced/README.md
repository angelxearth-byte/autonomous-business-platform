# Advanced ABSM (Autonomous Business Selling Machine)

Production-ready ABSM with enhanced scalability, monitoring, and infrastructure.

## Overview

This advanced version includes:
- Redis-based quota management
- Queued scoring system with worker processing
- Prefect telemetry and monitoring
- React-based monitoring dashboard
- Terraform infrastructure templates
- Grafana dashboard configuration
- Complete deployment automation

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │────│  Redis Queue     │────│  Worker Pool    │
│   (Express.js)  │    │  (BullMQ)        │    │  (Node.js)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌──────────────────┐              │
         └──────────────│   Scoring Engine │──────────────┘
                        │   (Python)       │
                        └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Grafana        │
                       │   Dashboard      │
                       └──────────────────┘
```

## Components

### Python Orchestrator (`python_orchestrator/`)
- **Redis Quota Management** (`redis_quota.py`) - Rate limiting and resource control
- **Queued Scorer** (`queued_scorer.py`) - Asynchronous scoring with queue processing
- **Prefect Telemetry** (`prefect_telemetry.py`) - Workflow monitoring and metrics

### Node.js Worker (`node_orchestrator/`)
- **BullMQ Integration** - Job queue management
- **Worker API** - REST endpoints for job management
- **Real-time Processing** - Background job processing

### Monitoring Dashboard (`dashboard/`)
- **React Interface** - Real-time monitoring UI
- **Grafana Integration** - Advanced metrics visualization
- **Job Status Tracking** - Queue and worker monitoring

### Infrastructure (`infra/terraform/`)
- **AWS Resources** - RDS, ECS, S3, CloudFormation
- **Container Orchestration** - ECS task definitions
- **Database Setup** - PostgreSQL with proper configuration

## Quick Start

### Local Development
```bash
# Start Redis
redis-server

# Start Python orchestrator
cd python_orchestrator
python queued_scorer.py

# Start Node.js worker
cd node_orchestrator
npm install && npm start

# Start dashboard
cd dashboard
npm install && npm run dev
```

### Production Deployment
See `DEPLOYMENT.md` for complete cloud deployment instructions.

## API Endpoints

### Worker API
- `GET /health` - Health check
- `POST /jobs` - Submit scoring job
- `GET /jobs/:id` - Get job status
- `GET /jobs` - List all jobs
- `DELETE /jobs/:id` - Cancel job

### Dashboard API
- `GET /stats` - Queue statistics
- `GET /workers` - Worker status
- `GET /metrics` - Performance metrics

## Configuration

### Environment Variables
```env
# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your_redis_password

# Queue Settings
BULL_QUEUE_NAME=business_scoring
MAX_QUEUE_SIZE=1000
WORKER_CONCURRENCY=5

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Prefect
PREFECT_API_URL=http://localhost:4200
PREFECT_API_KEY=your_prefect_key

# Monitoring
GRAFANA_URL=http://localhost:3000
GRAFANA_API_KEY=your_grafana_key
```

## Monitoring

### Grafana Dashboard
Import `grafana_dashboard.json` for:
- Queue depth monitoring
- Worker performance metrics
- Scoring latency tracking
- Error rate monitoring
- Resource utilization

### Prefect Monitoring
- Workflow execution tracking
- Flow run metrics
- Task-level performance analysis
- Automated alerting

## Scaling

### Horizontal Scaling
- Multiple worker instances
- Redis cluster for high availability
- Load balancer for API gateway

### Performance Optimization
- Queue prioritization
- Worker auto-scaling
- Caching strategies
- Database optimization

## Security

- Redis authentication
- API rate limiting
- Worker authorization
- Secure credential management
- Network isolation

## Deployment

1. **Infrastructure**: Use Terraform templates for AWS setup
2. **Containerization**: Docker images for all components
3. **Orchestration**: ECS or Kubernetes deployment
4. **Monitoring**: Grafana + Prefect integration
5. **CI/CD**: Automated deployment pipelines

## Next Steps

- Multi-region deployment
- Advanced ML models
- Real-time notifications
- API rate limiting
- Advanced security features