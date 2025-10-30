import os
import time
import logging
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import json
import uuid
from datetime import datetime, timedelta

import redis
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ScoringJob:
    id: str
    business_data: Dict[str, Any]
    status: str = 'pending'
    score: Optional[float] = None
    reasoning: Optional[List[str]] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # Convert datetime objects to strings for JSON serialization
        if data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        if data['completed_at']:
            data['completed_at'] = data['completed_at'].isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScoringJob':
        if 'created_at' in data and data['created_at']:
            data['created_at'] = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        if 'completed_at' in data and data['completed_at']:
            data['completed_at'] = datetime.fromisoformat(data['completed_at'].replace('Z', '+00:00'))
        return cls(**data)

class QueuedScorer:
    def __init__(self):
        # Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Configuration
        self.queue_name = os.getenv('BULL_QUEUE_NAME', 'business_scoring')
        self.max_concurrent_jobs = int(os.getenv('MAX_CONCURRENT_JOBS', '5'))
        self.job_timeout = int(os.getenv('JOB_TIMEOUT_SECONDS', '300'))
        self.retry_attempts = int(os.getenv('RETRY_ATTEMPTS', '3'))
        
        # AI Scorer (simplified version)
        self.ai_enabled = bool(os.getenv('AI_MODEL_API_KEY'))
        
        # Job processing control
        self.is_running = False
        self.worker_id = str(uuid.uuid4())
        
        logger.info(f"QueuedScorer initialized with queue: {self.queue_name}")
        logger.info(f"AI scoring enabled: {self.ai_enabled}")
    
    def submit_job(self, business_data: Dict[str, Any]) -> str:
        """Submit a new scoring job to the queue"""
        job = ScoringJob(
            id=str(uuid.uuid4()),
            business_data=business_data
        )
        
        # Store job in Redis
        job_key = f"job:{job.id}"
        self.redis_client.setex(
            job_key, 
            self.job_timeout * 2,  # Store for 2x the timeout
            json.dumps(job.to_dict())
        )
        
        # Add to queue
        queue_key = f"queue:{self.queue_name}"
        self.redis_client.lpush(queue_key, job.id)
        
        logger.info(f"Job {job.id} submitted for business: {business_data.get('name', 'Unknown')}")
        return job.id
    
    def get_job_status(self, job_id: str) -> Optional[ScoringJob]:
        """Get the status of a specific job"""
        job_key = f"job:{job_id}"
        job_data = self.redis_client.get(job_key)
        
        if job_data:
            return ScoringJob.from_dict(json.loads(job_data))
        return None
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get statistics about the current queue"""
        queue_key = f"queue:{self.queue_name}"
        pending_count = self.redis_client.llen(queue_key)
        
        # Get all job statuses
        job_pattern = "job:*"
        job_keys = self.redis_client.keys(job_pattern)
        
        stats = {
            'pending_jobs': pending_count,
            'total_jobs': len(job_keys),
            'completed_jobs': 0,
            'failed_jobs': 0,
            'processing_jobs': 0
        }
        
        for job_key in job_keys:
            job_data = json.loads(self.redis_client.get(job_key))
            status = job_data.get('status', 'unknown')
            
            if status == 'completed':
                stats['completed_jobs'] += 1
            elif status == 'failed':
                stats['failed_jobs'] += 1
            elif status == 'processing':
                stats['processing_jobs'] += 1
        
        return stats
    
    def _process_job(self, job: ScoringJob) -> None:
        """Process a single scoring job"""
        logger.info(f"Processing job {job.id}")
        
        try:
            # Update status to processing
            job.status = 'processing'
            self._update_job(job)
            
            # Perform scoring
            score_data = self._score_business(job.business_data)
            
            # Update job with results
            job.score = score_data['score']
            job.reasoning = score_data['reasoning']
            job.status = 'completed'
            job.completed_at = datetime.utcnow()
            
            logger.info(f"Job {job.id} completed with score: {job.score}")
            
        except Exception as e:
            logger.error(f"Job {job.id} failed: {str(e)}")
            job.status = 'failed'
            job.error = str(e)
            job.completed_at = datetime.utcnow()
        
        finally:
            # Update job in Redis
            self._update_job(job)
    
    def _score_business(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Score a business (simplified AI scoring)"""
        
        # Extract metrics
        monthly_revenue = business_data.get('monthly_revenue', 0)
        monthly_profit = business_data.get('monthly_profit', 0)
        growth_rate = business_data.get('growth_rate', 0)
        market_size = business_data.get('market_size', 0)
        industry = business_data.get('industry', 'General')
        years_operated = business_data.get('years_operated', 0)
        
        # Scoring algorithm (simplified)
        revenue_score = self._score_revenue(monthly_revenue, monthly_profit)
        growth_score = self._score_growth(growth_rate)
        market_score = self._score_market(market_size, industry)
        experience_score = self._score_experience(years_operated)
        
        # Calculate overall score (weighted average)
        overall_score = (
            revenue_score * 0.3 +
            growth_score * 0.25 +
            market_score * 0.25 +
            experience_score * 0.2
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            revenue_score, growth_score, market_score, experience_score, business_data
        )
        
        return {
            'score': round(overall_score, 2),
            'reasoning': reasoning
        }
    
    def _score_revenue(self, revenue: float, profit: float) -> float:
        """Score based on revenue and profitability"""
        if revenue < 1000:
            return 20
        elif revenue < 5000:
            return 40
        elif revenue < 15000:
            return 60
        elif revenue < 50000:
            return 80
        else:
            return 95
    
    def _score_growth(self, growth_rate: float) -> float:
        """Score based on growth rate"""
        if growth_rate < 0:
            return 10
        elif growth_rate < 5:
            return 30
        elif growth_rate < 15:
            return 60
        elif growth_rate < 30:
            return 80
        else:
            return 95
    
    def _score_market(self, market_size: float, industry: str) -> float:
        """Score based on market size and industry"""
        industry_multipliers = {
            'SaaS': 1.2,
            'E-commerce': 1.1,
            'Marketplace': 1.15,
            'Mobile App': 1.0,
            'Web App': 1.0,
            'Service': 0.9
        }
        
        multiplier = industry_multipliers.get(industry, 1.0)
        
        if market_size < 100000:
            return 30 * multiplier
        elif market_size < 1000000:
            return 50 * multiplier
        elif market_size < 10000000:
            return 70 * multiplier
        else:
            return 90 * multiplier
    
    def _score_experience(self, years_operated: int) -> float:
        """Score based on years operated"""
        if years_operated < 1:
            return 30
        elif years_operated < 3:
            return 50
        elif years_operated < 5:
            return 70
        else:
            return 85
    
    def _generate_reasoning(self, revenue_score: float, growth_score: float, 
                          market_score: float, experience_score: float, 
                          business_data: Dict[str, Any]) -> List[str]:
        """Generate reasoning for the scores"""
        reasoning = []
        
        if revenue_score >= 80:
            reasoning.append("Strong revenue generation with healthy profitability")
        elif revenue_score >= 60:
            reasoning.append("Moderate revenue with decent profit margins")
        else:
            reasoning.append("Revenue needs improvement for better investment appeal")
        
        if growth_score >= 80:
            reasoning.append("Excellent growth trajectory indicating market opportunity")
        elif growth_score >= 60:
            reasoning.append("Steady growth with potential for acceleration")
        else:
            reasoning.append("Growth is limited, may need strategic improvements")
        
        if market_score >= 80:
            reasoning.append("Large addressable market with favorable industry dynamics")
        elif market_score >= 60:
            reasoning.append("Decent market size with reasonable competition")
        else:
            reasoning.append("Market opportunity may be limited")
        
        if experience_score >= 80:
            reasoning.append("Proven track record with established operations")
        elif experience_score >= 60:
            reasoning.append("Some operational experience with growth potential")
        else:
            reasoning.append("Newer operation requiring additional validation")
        
        return reasoning
    
    def _update_job(self, job: ScoringJob) -> None:
        """Update job in Redis"""
        job_key = f"job:{job.id}"
        self.redis_client.setex(
            job_key,
            self.job_timeout * 2,
            json.dumps(job.to_dict())
        )
    
    def start_worker(self):
        """Start the worker to process jobs from the queue"""
        self.is_running = True
        queue_key = f"queue:{self.queue_name}"
        
        logger.info(f"Starting worker {self.worker_id} for queue {self.queue_name}")
        
        while self.is_running:
            try:
                # Get job ID from queue (blocks for up to 1 second)
                job_id = self.redis_client.brpop(queue_key, timeout=1)
                
                if job_id:
                    job_id = job_id[1]  # Get the job ID from the tuple
                    
                    # Get job details
                    job = self.get_job_status(job_id)
                    if job:
                        self._process_job(job)
                    else:
                        logger.warning(f"Job {job_id} not found")
                
                # Small delay to prevent excessive polling
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                logger.info("Worker interrupted by user")
                break
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                time.sleep(1)  # Wait before retrying
        
        logger.info(f"Worker {self.worker_id} stopped")
    
    def stop_worker(self):
        """Stop the worker"""
        self.is_running = False
        logger.info("Worker stop signal sent")
    
    def batch_submit(self, businesses: List[Dict[str, Any]]) -> List[str]:
        """Submit multiple businesses for scoring"""
        job_ids = []
        for business in businesses:
            job_id = self.submit_job(business)
            job_ids.append(job_id)
        
        logger.info(f"Submitted {len(job_ids)} jobs for batch processing")
        return job_ids

if __name__ == "__main__":
    # Example usage
    scorer = QueuedScorer()
    
    # Sample businesses
    businesses = [
        {
            'name': 'SaaS Company A',
            'monthly_revenue': 25000,
            'monthly_profit': 15000,
            'growth_rate': 25,
            'market_size': 50000000,
            'industry': 'SaaS',
            'years_operated': 3
        },
        {
            'name': 'E-commerce Business B',
            'monthly_revenue': 15000,
            'monthly_profit': 8000,
            'growth_rate': 15,
            'market_size': 30000000,
            'industry': 'E-commerce',
            'years_operated': 2
        }
    ]
    
    # Submit jobs
    job_ids = scorer.batch_submit(businesses)
    print(f"Submitted jobs: {job_ids}")
    
    # Start worker (in real application, this would run in a separate process)
    try:
        print("Starting worker (press Ctrl+C to stop)...")
        scorer.start_worker()
    except KeyboardInterrupt:
        print("\nShutting down...")
        scorer.stop_worker()