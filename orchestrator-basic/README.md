# Basic Autonomous Business Selling Machine

This directory contains the foundational orchestrators for automated business selling.

## Overview

Two parallel implementations of the same functionality:
- **Python Orchestrator** - AI-powered business analysis
- **Node.js Orchestrator** - JavaScript automation

## Features

- Automated business listing analysis
- AI-powered scoring algorithms
- Market trend analysis
- Marketplace integration (Flippa adapter included)
- Environment-based configuration

## Python Orchestrator (`python_orchestrator/`)

### Components
- `ai_scorer.py` - AI-powered business scoring
- `market_agent.py` - Market analysis and trends
- `codegen_agent.py` - Code generation for listings
- `deploy_agent.py` - Automated deployment
- `prefect_flows.py` - Workflow orchestration
- `listing_adapters/` - Marketplace integration layer

### Setup
```bash
cd python_orchestrator
cp .env.template .env
# Edit .env with your API keys
pip install -r requirements.txt
python prefect_flows.py
```

## Node.js Orchestrator (`node_orchestrator/`)

### Components
- `scorer.js` - Business scoring logic
- `marketAgent.js` - Market analysis
- `codegen.js` - Code generation
- `deploy.js` - Deployment automation
- `adapters/flippa.js` - Flippa marketplace integration

### Setup
```bash
cd node_orchestrator
cp .env.template .env
# Edit .env with your API keys
npm install
node index.js
```

## Configuration

Both orchestrators use environment variables:
```env
MARKETPLACE_API_KEY=your_marketplace_api_key
AI_MODEL_API_KEY=your_ai_model_key
LISTING_WEBHOOK_URL=your_webhook_endpoint
```

## Usage

1. Configure your environment variables
2. Start either the Python or Node.js orchestrator
3. The system will automatically analyze businesses and generate listings
4. Monitor logs for scoring results and deployment status

## Integration

Both orchestrators provide REST APIs for integration:
- `POST /analyze` - Analyze business opportunities
- `POST /score` - Score a specific business
- `POST /generate-listing` - Create automated listing
- `POST /deploy` - Deploy to marketplace

## Next Steps

- Integrate additional marketplaces beyond Flippa
- Enhance AI scoring with custom models
- Add notification systems for scoring events
- Implement advanced workflow scheduling with Prefect