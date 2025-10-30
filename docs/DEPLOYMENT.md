ABSM Deployment Guide (Manual steps and commands)

IMPORTANT: This environment cannot perform cloud deployments. The steps below are exact commands you should run from your machine with proper AWS/GCP credentials configured.

1) Terraform bootstrap (AWS)
- Install Terraform (v1.5+)
- Edit infra/terraform/variables.tf with secure values or provide via -var
- Commands:
  export AWS_PROFILE=your-profile
  cd infra/terraform
  terraform init
  terraform apply -var="db_password=StrongPassword123" -auto-approve
- Outputs: S3 bucket name, DB endpoint

2) Grafana setup
- Install Grafana locally or via Docker
- Import grafana_dashboard.json for monitoring dashboard
- Configure data sources (Prometheus, etc.)

3) Redis setup
- Install Redis server
- Configure authentication
- Set up persistent storage

4) Prefect setup
- Install Prefect Orion
- Configure Prefect API
- Set up agent for workflow execution

5) Node.js workers
- Build and push Docker images
- Deploy workers to ECS or Kubernetes
- Configure load balancer

6) Python orchestrator
- Deploy to ECS or Kubernetes
- Configure environment variables
- Set up monitoring and logging

7) Dashboard deployment
- Build React dashboard
- Deploy to static hosting (S3 + CloudFront)
- Configure CORS for API access

Environment Variables Required:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
- DATABASE_URL
- REDIS_URL
- PREFECT_API_URL
- GRAFANA_API_KEY

Security Considerations:
- Use IAM roles instead of access keys where possible
- Enable VPC and security groups
- Use Secrets Manager for sensitive data
- Enable encryption at rest and in transit
- Configure proper network access controls