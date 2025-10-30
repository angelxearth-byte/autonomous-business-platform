# MVP Scaffold - Full-Stack Business Platform

Production-ready full-stack application with payments, authentication, and deployment infrastructure.

## Overview

Complete Next.js + FastAPI application featuring:
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Stripe integration
- **Authentication**: Supabase auth and session management
- **Payments**: Complete Stripe checkout and webhook handling
- **Infrastructure**: Docker, Terraform, CI/CD pipelines

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Next.js       │────│   FastAPI        │────│   Supabase      │
│   Frontend      │    │   Backend        │    │   Database      │
│   (TypeScript)  │    │   (Python)       │    │   & Auth        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌──────────────────┐              │
         └──────────────│   Stripe         │──────────────┘
                        │   Payments       │
                        └──────────────────┘
```

## Quick Start

### Option 1: Local Development
```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend (in new terminal)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Option 2: Docker Compose
```bash
cd infra
docker-compose up --build
```

## Project Structure

```
mvp-scaffold/
├── frontend/                 # Next.js application
│   ├── pages/               # Next.js pages
│   ├── components/          # React components
│   ├── lib/                # Utilities
│   ├── styles/             # CSS styles
│   └── public/             # Static assets
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── db/             # Database models
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── infra/                  # Infrastructure
│   ├── docker-compose.yml # Local development
│   ├── terraform/         # Cloud infrastructure
│   ├── aws/              # AWS deployment
│   └── vercel_deploy_instructions.md
└── .github/workflows/     # CI/CD pipelines
    ├── frontend-ci.yml    # Frontend testing
    ├── backend-ci.yml     # Backend testing
    └── frontend-ghcr.yml  # Container registry
```

## Features

### Frontend (Next.js)
- **Authentication**: Supabase Auth integration
- **Product Management**: CRUD operations
- **Stripe Checkout**: Payment processing
- **Dashboard**: User dashboard with analytics
- **Responsive Design**: Tailwind CSS styling
- **TypeScript**: Full type safety

### Backend (FastAPI)
- **REST API**: FastAPI with automatic documentation
- **Stripe Integration**: Checkout and webhook handling
- **Supabase Auth**: Session verification
- **Database Models**: SQLAlchemy ORM
- **Security**: JWT tokens and session management
- **API Documentation**: Auto-generated OpenAPI docs

### Infrastructure
- **Containerization**: Docker for all services
- **Database**: PostgreSQL via Supabase
- **Authentication**: Supabase Auth
- **Payments**: Stripe processing
- **Deployment**: Multiple platform support (Vercel, AWS, etc.)
- **CI/CD**: GitHub Actions workflows

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/user` - Get current user

### Products
- `GET /api/products` - List products
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Create product (auth required)
- `PUT /api/products/:id` - Update product (auth required)
- `DELETE /api/products/:id` - Delete product (auth required)

### Payments
- `POST /stripe/create-session` - Create Stripe checkout session
- `POST /stripe/webhook` - Handle Stripe webhooks
- `POST /supabase-auth` - Verify Supabase session

## Configuration

### Frontend Environment Variables
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_STRIPE_PRICE_ID=price_...
```

### Backend Environment Variables
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
JWT_SECRET_KEY=your_jwt_secret
```

## Deployment

### Vercel (Frontend)
1. Connect GitHub repository to Vercel
2. Set environment variables
3. Deploy automatically on push

### AWS (Backend)
```bash
# Deploy using Terraform
cd infra/terraform
terraform init
terraform apply
```

### Docker (Local/Production)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Database Schema

### Products Table
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    user_id UUID REFERENCES auth.users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Stripe Integration

### Checkout Flow
1. User clicks "Buy" on product page
2. Frontend calls `/stripe/create-session`
3. Backend creates Stripe checkout session
4. Frontend redirects to Stripe Checkout
5. On success, Stripe calls webhook
6. Backend processes payment and updates database

### Webhook Handling
- Secure webhook signature verification
- Payment success/failure processing
- Database updates
- Order management

## Security Features

- **Authentication**: Supabase JWT tokens
- **Session Management**: Secure session handling
- **API Security**: Rate limiting and validation
- **Payment Security**: Stripe webhook verification
- **Database Security**: Row-level security policies

## Testing

### Frontend Testing
```bash
cd frontend
npm test
npm run test:coverage
```

### Backend Testing
```bash
cd backend
pytest
pytest --cov=app
```

## Monitoring

- **Application Logs**: Structured logging
- **Performance Monitoring**: Response time tracking
- **Error Tracking**: Error reporting and alerts
- **Database Monitoring**: Query performance
- **Payment Monitoring**: Transaction tracking

## Performance Optimization

- **Frontend**: Next.js optimization, lazy loading
- **Backend**: Database indexing, caching
- **Database**: Connection pooling, query optimization
- **Payments**: Efficient webhook processing

## Contributing

1. Set up local development environment
2. Create feature branch
3. Implement changes with tests
4. Submit pull request
5. CI/CD will run tests automatically

## Troubleshooting

### Common Issues
- **CORS Errors**: Check frontend API URL configuration
- **Stripe Errors**: Verify API keys and webhook configuration
- **Supabase Auth**: Check auth provider settings
- **Database Connection**: Verify connection string and credentials

### Debug Mode
```bash
# Frontend
npm run dev

# Backend
uvicorn app.main:app --reload --log-level debug
```

## Next Steps

- Add email notifications
- Implement advanced analytics
- Add multi-tenancy support
- Enhance security features
- Add mobile app support