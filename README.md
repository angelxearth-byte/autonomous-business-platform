# Autonomous Business Platform

A comprehensive autonomous business selling machine platform with orchestrators, advanced monitoring, and full-stack MVP scaffold.

## 🏗️ Platform Architecture

This platform consists of three main components:

### 1. Basic Orchestrator (`/orchestrator-basic/`)
- **Python Orchestrator**: AI-powered business scoring and market analysis
- **Node.js Orchestrator**: JavaScript implementation of business automation
- Features: Automated listing management, market analysis, AI scoring
- Marketplace integration (Flippa adapter included)

### 2. Advanced Orchestrator (`/orchestrator-advanced/`)
- **Enhanced Python Orchestrator**: Redis quota management, queued scoring, Prefect telemetry
- **Node.js Worker**: BullMQ-based job processing
- **React Dashboard**: Monitoring and control interface
- **Infrastructure**: Terraform templates for AWS deployment
- **Monitoring**: Grafana dashboard configuration
- **Deployment**: Complete deployment scripts and guides

### 3. MVP Scaffold (`/mvp-scaffold/`)
- **Frontend**: Next.js + TypeScript application
- **Backend**: FastAPI with Stripe payment integration
- **Database**: Supabase authentication and storage
- **Infrastructure**: Docker, Terraform, AWS deployment guides
- **CI/CD**: GitHub Actions workflows
- **Payments**: Complete Stripe checkout and webhook handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- AWS/GCP credentials (for cloud deployment)
- Stripe account (for payments)
- Supabase account (for auth/database)

### Option 1: Run MVP Locally (Easiest)
```bash
cd mvp-scaffold
# Frontend
cd frontend && npm install && npm run dev
# Backend (in new terminal)
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload
```

### Option 2: Docker Compose (Full Stack)
```bash
cd mvp-scaffold
docker-compose -f infra/docker-compose.yml up --build
```

### Option 3: Deploy Advanced Infrastructure
```bash
# Configure AWS credentials
export AWS_PROFILE=your-profile

# Deploy infrastructure
cd orchestrator-advanced/infra/terraform
terraform init
terraform apply -var="db_password=YourStrongPassword" -auto-approve
```

## 📁 Directory Structure

```
/
├── orchestrator-basic/          # Basic Python/Node.js orchestrators
│   ├── python_orchestrator/     # AI scoring & market analysis
│   └── node_orchestrator/       # JavaScript automation
├── orchestrator-advanced/       # Production-ready ABSM
│   ├── python_orchestrator/     # Redis, queues, telemetry
│   ├── node_orchestrator/       # BullMQ workers
│   ├── dashboard/              # React monitoring UI
│   ├── infra/                  # Terraform infrastructure
│   └── grafana_dashboard.json  # Monitoring config
├── mvp-scaffold/               # Full-stack web application
│   ├── frontend/               # Next.js app
│   ├── backend/               # FastAPI app
│   ├── infra/                 # Deployment configs
│   └── .github/workflows/      # CI/CD pipelines
└── docs/                      # Documentation
    ├── DEPLOYMENT.md          # Advanced deployment guide
    └── SECURITY_NOTES.md      # Security considerations
```

## 🛠️ Technology Stack

### Orchestrators
- **Python**: Prefect, Redis, AI/ML libraries
- **Node.js**: BullMQ, Express.js, API integrations
- **Databases**: Redis, PostgreSQL, Supabase
- **Monitoring**: Grafana, Prefect telemetry

### MVP Application
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, SQLAlchemy
- **Payments**: Stripe (checkout, webhooks)
- **Auth**: Supabase authentication
- **Infrastructure**: Docker, Terraform, AWS

## 📊 Features

### Business Automation
- Automated business listing analysis
- AI-powered scoring and valuation
- Market trend analysis
- Multi-marketplace integration
- Performance monitoring

### Web Application
- User authentication & profiles
- Product management
- Stripe payment processing
- Real-time dashboard
- API integrations

### DevOps & Infrastructure
- Containerized deployment
- Infrastructure as Code (Terraform)
- CI/CD pipelines (GitHub Actions)
- Monitoring and alerting
- Cloud deployment guides

## 🔧 Configuration

### Environment Variables

**Python Orchestrator:**
```env
REDIS_URL=redis://localhost:6379
MARKETPLACE_API_KEY=your_key
AI_MODEL_API_KEY=your_key
```

**Node.js Orchestrator:**
```env
REDIS_URL=redis://localhost:6379
MARKETPLACE_API_KEY=your_key
BULL_QUEUE_NAME=business_analysis
```

**MVP Backend:**
```env
DATABASE_URL=postgresql://user:pass@localhost/db
STRIPE_SECRET_KEY=sk_test_...
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_role_key
```

**MVP Frontend:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
```

## 📖 Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)** - Complete infrastructure deployment
- **[Security Notes](docs/SECURITY_NOTES.md)** - Security considerations
- **[Orchestrator README](orchestrator-basic/README.md)** - Basic setup guide
- **[Advanced Orchestrator](orchestrator-advanced/README.md)** - Production setup
- **[MVP Guide](mvp-scaffold/README.md)** - Full-stack application guide

## 🚦 Getting Started Steps

1. **Start with MVP**: Run the web application locally to understand the core features
2. **Explore Orchestrators**: Try the basic Python/Node.js automation scripts
3. **Scale with Advanced**: Deploy the Redis-backed, monitored version
4. **Production Deployment**: Use Terraform templates for cloud infrastructure

## 🤝 Contributing

This is a comprehensive business automation platform. Each component can be used independently or together as a complete solution.

## 📄 License

Private repository - All rights reserved

---

**Repository**: https://github.com/angelxearth-byte/autonomous-business-platform
**Created**: October 30, 2025